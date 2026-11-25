"""Comprueba CSV y consultas docentes mediante SQLite, sin credenciales ni dependencias."""

import argparse
import csv
import filecmp
import json
import re
import sqlite3
import sys
import tempfile
import unittest
from collections import defaultdict
from datetime import date
from pathlib import Path

BIGQUERY = Path(__file__).resolve().parent
SOLUTIONS = BIGQUERY / "ejercicio_final" / "solucion"

from generar_datos import generate
from modelo import DEFAULT_SEED, ORIGIN_REGION, SCHEMAS, SMALL_ORDERS, SMALL_SALES

KEYS = {
    "customers": ("customer_id",),
    "orders": ("order_id",),
    "order_items": ("order_id", "line_number"),
    "products": ("product_id",),
    "suppliers": ("supplier_id",),
    "supplier_monthly": ("month_start", "product_id", "supplier_id"),
    "territory_monthly": ("month_start", "province"),
}
TYPES = {"INT64": "INTEGER", "BOOL": "TEXT", "STRING": "TEXT", "DATE": "TEXT"}
PROVINCES = {"Valencia", "Alicante", "Castellón"}
REPORT = False
CSV_DIR = None
ORDER_COUNT = 60_000
SEED = DEFAULT_SEED
TEACHER_EXTENSION = "\n-- Ampliación para la puesta en común.\n"
OPTIONAL_SECTION = "-- ¿Qué podéis mirar si os queda tiempo?"


def register_date_functions(db):
    db.create_function(
        "days_between", 2,
        lambda end, start: (date.fromisoformat(end) - date.fromisoformat(start)).days
        if end is not None and start is not None else None,
    )
    db.create_function("month_start", 1, lambda value: value[:7] + "-01" if value is not None else None)


def build_database(db, source):
    db.row_factory = sqlite3.Row
    register_date_functions(db)
    with db:
        for table, fields in SCHEMAS.items():
            declaration = ", ".join(f"{name} {TYPES[kind]} NOT NULL" for name, kind in fields)
            key = ", ".join(KEYS[table])
            db.execute(f"CREATE TABLE {table} ({declaration}, PRIMARY KEY ({key})) WITHOUT ROWID")
            with (source / f"{table}.csv").open(encoding="utf-8", newline="") as file:
                rows = csv.reader(file)
                if next(rows) != [name for name, _ in fields]:
                    raise ValueError(f"Cabecera inesperada en {table}.csv")
                placeholders = ", ".join("?" for _ in fields)
                db.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
        db.execute("CREATE INDEX orders_customer ON orders (customer_id, order_date, order_id)")
        db.execute("ANALYZE")


def sqlite_select(query):
    query = re.sub(r"`PROJECT_ID\.terra_taronja_raw\.(\w+)`", r"\1", query)
    query = re.sub(r"\bDATE ('\d{4}-\d{2}-\d{2}')", r"\1", query)
    query = re.sub(r"\bDATE_TRUNC\(([\w.]+), MONTH\)", r"month_start(\1)", query)
    return re.sub(r"\bDATE_DIFF\(([\w.]+), ([\w.]+), DAY\)", r"days_between(\1, \2)", query)


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temp = tempfile.TemporaryDirectory(prefix="terra-bq-tests-")
        cls.addClassCleanup(temp.cleanup)
        source = CSV_DIR or Path(temp.name) / "csv"
        if CSV_DIR is None:
            generate(source, ORDER_COUNT, SEED)
        db = sqlite3.connect(Path(temp.name) / "test.sqlite")
        cls.addClassCleanup(db.close)
        build_database(db, source)
        cls.db = db

    def query(self, sql, *params):
        return self.db.execute(sql, params).fetchall()

    def scalar(self, sql, *params):
        return self.query(sql, *params)[0][0]

    def test_customer_contacts(self):
        self.assertEqual(self.scalar("""
            SELECT COUNT(*) FROM customers
            WHERE TRIM(customer_name) = '' OR email <> 'cliente' || customer_id || '@example.com'
        """), 0)
        self.assertEqual(self.scalar("SELECT COUNT(DISTINCT email) FROM customers"),
                         self.scalar("SELECT COUNT(*) FROM customers"))
        self.assertGreater(self.scalar("SELECT COUNT(DISTINCT customer_name) FROM customers"), 1)

    def dashboard(self, team):
        sql, = SOLUTIONS.glob(f"equipo_{team}_*/consultas.sql")
        _, extension = sql.read_text(encoding="utf-8").split(TEACHER_EXTENSION, 1)
        _, blocks = extension.split("-- Consulta avanzada de referencia.\n", 1)
        return self.query(sqlite_select(blocks.split(";", 1)[0]))

    def test_final_exercise_alignment(self):
        exercise = BIGQUERY / "ejercicio_final"
        files = sorted(exercise.glob("equipo_*/consultas.sql"))
        self.assertEqual(len(files), 5)
        for student in files:
            with self.subTest(team=student.parent.name):
                teacher = SOLUTIONS / student.relative_to(exercise)
                self.assertEqual(list(teacher.parent.glob("*.sql")), [teacher])
                questions = [line for line in student.read_text(encoding="utf-8").splitlines() if line.strip()]
                solution, separator, extension = teacher.read_text(encoding="utf-8").partition(TEACHER_EXTENSION)
                self.assertTrue(separator)
                self.assertEqual(extension.count("-- Consulta avanzada de referencia."), 1)
                parts = re.split(r"^(-- ¿.+\?)$", solution, flags=re.M)
                solution_questions = [question for question in parts[1::2] if question != OPTIONAL_SECTION]
                self.assertEqual(solution_questions, questions)
                executed = 0
                for question, block in zip(parts[1::2], parts[2::2], strict=True):
                    if question == OPTIONAL_SECTION:
                        continue
                    self.assertIn("\n-- Resultado esperado. ", block)
                    self.assertIn("\n-- Por qué. ", block)
                    query = "\n".join(line for line in block.splitlines() if not line.startswith("--")).strip()
                    if query:
                        self.assertTrue(self.query(sqlite_select(query)), question)
                        executed += 1
                self.assertGreaterEqual(executed, 2)

    def test_b_only_orders_from_pilot_months(self):
        sql = SOLUTIONS / "equipo_2_territorios/consultas.sql"
        basic = sql.read_text(encoding="utf-8").split(TEACHER_EXTENSION, 1)[0]
        code = "\n".join(line for line in basic.splitlines() if not line.startswith("--"))
        orders_query = next(query for query in code.split(";") if "AS pedidos_por_mes" in query)
        delivery_query = next(query for query in code.split(";") if "AS plazo_medio_dias" in query)

        db = sqlite3.connect(":memory:")
        self.addCleanup(db.close)
        register_date_functions(db)
        db.executescript("""
            CREATE TABLE territory_monthly (province TEXT, month_start TEXT, sales_program TEXT);
            CREATE TABLE orders (
                order_id INTEGER, province TEXT, order_date TEXT,
                delivery_date TEXT, shipping_cost_cents INTEGER
            );
            INSERT INTO territory_monthly VALUES
                ('A Coruña', '2025-01-01', 'piloto'),
                ('A Coruña', '2025-02-01', 'regular'),
                ('A Coruña', '2025-03-01', 'piloto'),
                ('A Coruña', '2026-01-01', 'piloto'),
                ('Santa Cruz de Tenerife', '2025-02-01', 'piloto');
            INSERT INTO orders VALUES
                (1, 'A Coruña', '2025-01-31', '2025-02-02', 500),
                (2, 'A Coruña', '2025-02-03', '2025-02-15', 9900),
                (3, 'A Coruña', '2026-01-01', '2026-01-11', 9000),
                (4, 'Santa Cruz de Tenerife', '2025-02-03', '2025-02-08', 1500);
        """)

        self.assertCountEqual(db.execute(sqlite_select(orders_query)).fetchall(), [
            ("A Coruña", 2, 1, 0.5, 5.0),
            ("Santa Cruz de Tenerife", 1, 1, 1.0, 15.0),
        ])
        self.assertCountEqual(db.execute(sqlite_select(delivery_query)).fetchall(), [
            ("A Coruña", 2.0),
            ("Santa Cruz de Tenerife", 5.0),
        ])

    def test_c_counts_distinct_orders_and_catalogue(self):
        sql = SOLUTIONS / "equipo_3_categorias/consultas.sql"
        basic = sql.read_text(encoding="utf-8").split(TEACHER_EXTENSION, 1)[0]
        code = "\n".join(line for line in basic.splitlines() if not line.startswith("--"))
        statements = code.split(";")
        orders_query = next(query for query in statements if "AS pedidos" in query and "DATE_TRUNC" not in query)
        monthly_query = next(query for query in statements if "AS pedidos" in query and "DATE_TRUNC" in query)
        catalog_query = next(query for query in statements if "AS productos_en_catalogo" in query)

        db = sqlite3.connect(":memory:")
        self.addCleanup(db.close)
        register_date_functions(db)
        db.executescript("""
            CREATE TABLE products (product_id INTEGER, category TEXT, catalog_since TEXT);
            CREATE TABLE orders (order_id INTEGER, order_date TEXT);
            CREATE TABLE order_items (order_id INTEGER, product_id INTEGER);
            INSERT INTO products VALUES
                (1, 'Dulces artesanos', '2025-09-01'),
                (2, 'Dulces artesanos', '2025-09-01'),
                (3, 'Dulces artesanos', '2025-11-01'),
                (4, 'Dulces artesanos', '2026-01-01'),
                (5, 'Despensa', '2023-01-01'),
                (6, 'Despensa', '2023-01-01');
            INSERT INTO orders VALUES
                (1, '2025-09-01'), (2, '2025-12-01'), (3, '2025-08-31'), (4, '2026-01-01');
            INSERT INTO order_items VALUES
                (1, 1), (1, 2), (1, 5), (2, 5), (3, 5), (4, 4);
        """)

        self.assertCountEqual(db.execute(sqlite_select(orders_query)).fetchall(), [
            ("Despensa", 2), ("Dulces artesanos", 1),
        ])
        self.assertCountEqual(db.execute(sqlite_select(monthly_query)).fetchall(), [
            ("2025-09-01", "Despensa", 1),
            ("2025-09-01", "Dulces artesanos", 1),
            ("2025-12-01", "Despensa", 1),
        ])
        self.assertCountEqual(db.execute(sqlite_select(catalog_query)).fetchall(), [
            ("Despensa", 2), ("Dulces artesanos", 3),
        ])

    def test_references_and_dates(self):
        self.assertEqual(self.scalar("SELECT COUNT(*) FROM orders"), ORDER_COUNT)
        self.assertEqual(self.scalar("SELECT MAX(order_id) FROM orders"), ORDER_COUNT)
        self.assertEqual(self.scalar("""
            SELECT COUNT(*) FROM orders o
            LEFT JOIN customers c USING (customer_id)
            LEFT JOIN territory_monthly t ON t.province = o.province AND t.month_start = month_start(o.order_date)
            WHERE c.customer_id IS NULL OR t.province IS NULL OR o.province <> c.province
               OR o.region <> c.region OR o.region <> t.region OR o.customer_type <> c.customer_type
               OR c.registered_date > c.first_order_date OR o.order_date < c.first_order_date
               OR o.order_date NOT BETWEEN '2023-01-01' AND '2025-12-31'
               OR NOT days_between(o.delivery_date, o.order_date) BETWEEN 1 AND 12
               OR o.delivery_incident NOT IN ('true', 'false')
        """), 0)
        self.assertEqual(self.scalar("""
            WITH first_orders AS (
              SELECT customer_id, MIN(order_date) AS first_order_date FROM orders GROUP BY customer_id
            )
            SELECT COUNT(*) FROM customers c LEFT JOIN first_orders f USING (customer_id)
            WHERE f.customer_id IS NULL OR f.first_order_date <> c.first_order_date
        """), 0)
        self.assertEqual(self.scalar("""
            SELECT COUNT(*) FROM order_items i
            LEFT JOIN orders o USING (order_id)
            LEFT JOIN products p USING (product_id)
            LEFT JOIN suppliers s USING (supplier_id)
            LEFT JOIN supplier_monthly m
              ON m.product_id = i.product_id AND m.supplier_id = i.supplier_id
             AND m.month_start = month_start(o.order_date)
            WHERE o.order_id IS NULL OR p.product_id IS NULL OR s.supplier_id IS NULL
               OR m.supplier_id IS NULL OR p.origin_province <> s.province OR o.order_date < p.catalog_since
               OR i.quantity <= 0 OR i.unit_price_cents <= 0 OR i.unit_cost_cents <= 0
               OR i.returned_quantity NOT BETWEEN 0 AND i.quantity
               OR i.discount_cents NOT BETWEEN 0 AND i.quantity * i.unit_price_cents
               OR i.refund_cents <> (i.quantity * i.unit_price_cents - i.discount_cents) * i.returned_quantity / i.quantity
        """), 0)
        for table, province in (("products", "origin_province"), ("suppliers", "province")):
            origins = self.query(f"SELECT DISTINCT origin_region, {province} FROM {table}")
            self.assertEqual({tuple(row) for row in origins}, {(ORIGIN_REGION, name) for name in PROVINCES})
        self.assertEqual(
            {row[0] for row in self.query("SELECT DISTINCT province FROM customers WHERE region = 'Galicia'")},
            {"A Coruña", "Pontevedra", "Lugo", "Ourense"},
        )
        self.assertEqual(
            {row[0] for row in self.query("SELECT DISTINCT province FROM customers WHERE region = 'Canarias'")},
            {"Las Palmas", "Santa Cruz de Tenerife"},
        )

    def test_finances_reconcile(self):
        self.assertEqual(self.scalar("""
            WITH totals AS (
              SELECT order_id, COUNT(*) AS lines, COUNT(DISTINCT product_id) AS products,
                     MIN(line_number) AS first_line, MAX(line_number) AS last_line,
                     SUM(quantity * unit_price_cents) AS gross, SUM(discount_cents) AS discount,
                     SUM(refund_cents) AS refund, SUM(quantity * unit_cost_cents) AS cost
              FROM order_items GROUP BY order_id
            )
            SELECT COUNT(*) FROM orders o LEFT JOIN totals t USING (order_id)
            WHERE t.order_id IS NULL OR t.lines <> t.products OR t.lines NOT BETWEEN 2 AND 5
               OR t.first_line <> 1 OR t.last_line <> t.lines
               OR gross <> gross_cents OR discount <> discount_cents OR refund <> refund_cents
               OR cost <> product_cost_cents OR net_cents <> gross - discount - refund OR net_cents < 0
               OR shipping_paid_cents < 0 OR shipping_cost_cents < 0 OR service_cost_cents < 0
               OR contribution_cents <> net_cents + shipping_paid_cents
                                         - product_cost_cents - shipping_cost_cents - service_cost_cents
        """), 0)
        self.assertEqual(self.scalar("""
            WITH sales AS (
              SELECT month_start(o.order_date) AS month_start, i.product_id, i.supplier_id,
                     SUM(i.quantity) AS units
              FROM orders o JOIN order_items i USING (order_id)
              GROUP BY 1, 2, 3
            )
            SELECT COUNT(*) FROM supplier_monthly m
            LEFT JOIN sales s USING (month_start, product_id, supplier_id)
            WHERE fulfilled_units <> COALESCE(s.units, 0) OR requested_units < fulfilled_units
               OR planned_units < received_units OR received_units < fulfilled_units
               OR late_shipments NOT BETWEEN 0 AND shipments OR stockout_days NOT BETWEEN 0 AND 31
        """), 0)

    def test_a_providers(self):
        rows = self.dashboard(1)
        self.assertGreaterEqual(len(rows), 35)
        self.assertTrue(any(r["sales_share"] > .72 and r["unserved_share"] > .075
                            and r["late_share"] > .13 and r["months_with_stockouts"] >= 5 for r in rows))
        self.assertTrue(any(r["fill_rate"] > .94 and r["late_share"] < .09 for r in rows))
        self.assertTrue(any(r["max_stockout_days"] - r["min_stockout_days"] >= 3 for r in rows))
        if REPORT:
            print("\nA. Filas con más unidades sin servir", [dict(r) for r in rows[:4]])

    def test_b_pilots(self):
        rows = self.dashboard(2)
        regions = {r["territory"]: r for r in rows if r["level"] == "comunidad"}
        gal, can = regions["Galicia"], regions["Canarias"]
        if REPORT:
            print("\nB. Pilotos por comunidad", [dict(r) for r in regions.values()])
        self.assertGreater(gal["repeat_90d"], can["repeat_90d"])
        self.assertGreater(gal["contribution_rate"] - can["contribution_rate"], .035)
        self.assertGreater(can["contribution_rate"], .02)
        self.assertGreater(can["shipping_eur_per_order"] - gal["shipping_eur_per_order"], 3)
        self.assertGreater(can["delivery_days_per_order"] - gal["delivery_days_per_order"], 2)
        self.assertTrue(any(r["first_orders_per_contact"] > gal["first_orders_per_contact"]
                            and r["repeat_90d"] < gal["repeat_90d"] for r in regions.values()))
        self.assertGreater(min(gal["eligible"], can["eligible"]), 200)
        for region in ("Galicia", "Canarias"):
            provinces = [r for r in rows if r["region"] == region and r["level"] == "provincia"]
            self.assertEqual(len(provinces), 4 if region == "Galicia" else 2)
            self.assertEqual(regions[region]["orders"], sum(p["orders"] for p in provinces))

    def test_c_categories(self):
        by_category = defaultdict(list)
        for row in self.dashboard(3):
            by_category[row["category"]].append(row)
        sweets = by_category["Dulces artesanos"]
        preserves = by_category["Conservas vegetales"]
        pantry = by_category["Despensa"]
        self.assertEqual(len(sweets), 4)
        self.assertGreater(sweets[-1]["orders"], 1.35 * sweets[0]["orders"])
        self.assertLess(sum(r["orders"] for r in sweets), sum(r["orders"] for r in pantry))
        self.assertGreater(sweets[-1]["product_margin"], preserves[-1]["product_margin"] + .055)
        self.assertTrue(all(r["return_share"] > p["return_share"] and r["discount_share"] > p["discount_share"]
                            for r, p in zip(preserves, pantry)))
        if REPORT:
            print("\nC. Categorías en septiembre y diciembre",
                  [dict(r) for group in (sweets, preserves, pantry) for r in (group[0], group[-1])])

    def test_d_b2b(self):
        groups = {r["customer_type"]: r for r in self.dashboard(4)}
        consumer, restaurant, company = (groups[k] for k in ("particular", "restaurante", "gran_empresa"))
        self.assertGreater(restaurant["orders_90d"], 1.4 * consumer["orders_90d"])
        self.assertGreater(restaurant["contribution_rate"], .15)
        self.assertGreater(company["basket_eur"], 2 * restaurant["basket_eur"])
        self.assertGreater(company["service_eur"], 3 * restaurant["service_eur"])
        self.assertGreater(restaurant["contribution_rate"] - company["contribution_rate"], .09)
        self.assertGreater(company["customer_share_over_20"], .05)
        if REPORT:
            print("\nD. Segmentos", [dict(r) for r in groups.values()])

    def test_e_counts_customers_in_different_months(self):
        sql = SOLUTIONS / "equipo_5_suscripcion/consultas.sql"
        basic = sql.read_text(encoding="utf-8").split(TEACHER_EXTENSION, 1)[0]
        code = "\n".join(line for line in basic.splitlines() if not line.startswith("--"))
        query = next(statement for statement in code.split(";") if "AS clientes_en_varios_meses" in statement)

        db = sqlite3.connect(":memory:")
        self.addCleanup(db.close)
        register_date_functions(db)
        db.executescript("""
            CREATE TABLE orders (
                province TEXT, customer_id INTEGER, order_date TEXT, customer_type TEXT
            );
            INSERT INTO orders VALUES
                ('Valencia', 1, '2025-01-02', 'particular'),
                ('Valencia', 1, '2025-01-20', 'particular'),
                ('Valencia', 2, '2025-01-31', 'particular'),
                ('Valencia', 2, '2025-02-01', 'particular'),
                ('Valencia', 3, '2025-12-31', 'particular'),
                ('Valencia', 3, '2026-01-01', 'particular'),
                ('Valencia', 4, '2025-02-01', 'restaurante'),
                ('Valencia', 4, '2025-04-01', 'restaurante'),
                ('Girona', 5, '2025-01-01', 'particular'),
                ('Girona', 5, '2025-03-01', 'particular'),
                ('Girona', 6, '2025-04-01', 'particular'),
                ('Alicante', 7, '2025-01-01', 'particular'),
                ('Alicante', 7, '2025-12-01', 'particular');
        """)

        self.assertCountEqual(db.execute(sqlite_select(query)).fetchall(), [
            ("Valencia", 3, 1, 33.33),
            ("Girona", 2, 1, 50.0),
        ])

    def test_e_subscription(self):
        provinces = {r["province"]: r for r in self.dashboard(5)}
        val, cas, gir = (provinces[p] for p in ("Valencia", "Castellón", "Girona"))
        self.assertGreater(val["regular_basket_share"], gir["regular_basket_share"] + .08)
        self.assertGreater(cas["regular_basket_share"], gir["regular_basket_share"] + .06)
        self.assertGreater(val["basket_overlap_among_repeat_buyers"], gir["basket_overlap_among_repeat_buyers"])
        self.assertGreater(val["repeat_90d"], gir["repeat_90d"])
        self.assertLess(max(r["regular_basket_share"] for r in provinces.values()), .50)
        if REPORT:
            print("\nE. Tres provincias", [dict(r) for r in (val, cas, gir)])


class ReproducibilityTests(unittest.TestCase):
    def test_bigquery_schemas_match_csvs(self):
        sql_dir = BIGQUERY / "lab02" / "sql"
        for filename in ("01_crear_raw.sql", "02_cargar_gcs.sql"):
            sql = (sql_dir / filename).read_text(encoding="utf-8")
            tables = re.findall(r"terra_taronja_raw\.(\w+)` \(\n(.*?)\n\)", sql, re.S)
            self.assertEqual(len(tables), len(SCHEMAS))
            for table, columns in tables:
                self.assertEqual(tuple(re.findall(r"^  (\w+) (\w+)(?: NOT NULL)?,?$", columns, re.M)), SCHEMAS[table])
        small_schema = json.loads((BIGQUERY / "lab01" / "datos" / "ventas.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(tuple((col["name"], "INT64" if col["type"] == "INTEGER" else col["type"])
                               for col in small_schema), SMALL_SALES)

    def test_small_files_and_seed(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            generate(base / "a", SMALL_ORDERS, DEFAULT_SEED, small=True)
            generate(base / "b", SMALL_ORDERS, DEFAULT_SEED + 1, small=True)
            provided = BIGQUERY / "lab01" / "datos"
            for name in ("ventas.csv", "products.csv"):
                self.assertEqual((base / "a" / name).read_text(encoding="utf-8"),
                                 (provided / name).read_text(encoding="utf-8"), name)
            self.assertFalse(filecmp.cmp(base / "a" / "ventas.csv", base / "b" / "ventas.csv", shallow=False))
            with (provided / "ventas.csv").open(encoding="utf-8", newline="") as file:
                data = csv.DictReader(file)
                self.assertEqual(data.fieldnames, [name for name, _ in SMALL_SALES])
                rows = list(data)
            self.assertEqual(len({row["order_id"] for row in rows}), SMALL_ORDERS)
            self.assertEqual(len(rows), 980)
            self.assertTrue({row["origin_province"] for row in rows} == PROVINCES)

    def test_all_large_csvs_reproduce(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            generate(base / "a", 650, DEFAULT_SEED)
            generate(base / "b", 650, DEFAULT_SEED)
            for table in SCHEMAS:
                self.assertTrue(filecmp.cmp(base / "a" / f"{table}.csv", base / "b" / f"{table}.csv", shallow=False),
                                table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv-dir", type=Path, help="Valida CSV ya generados en vez de crear datos temporales.")
    parser.add_argument("--orders", type=int, default=ORDER_COUNT, help="Filas de orders esperadas o a generar.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Semilla al generar el conjunto temporal.")
    parser.add_argument("--report", action="store_true", help="Imprime métricas para el profesor.")
    args = parser.parse_args()
    CSV_DIR, ORDER_COUNT, SEED, REPORT = args.csv_dir, args.orders, args.seed, args.report
    unittest.main(argv=[sys.argv[0]], verbosity=2)
