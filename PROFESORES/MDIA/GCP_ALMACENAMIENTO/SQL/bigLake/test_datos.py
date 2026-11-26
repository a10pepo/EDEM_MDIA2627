"""Verifica los datos publicados y las consultas del Lab 01 en local."""

import csv
import json
import re
import sqlite3
import tempfile
import unittest
from collections import Counter, defaultdict
from contextlib import closing
from datetime import date
from decimal import Decimal
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from generar_datos import (
    A_FIELDS,
    B_FIELDS,
    DELIVERY_FIELDS,
    MAP_FIELDS,
    SNAPSHOT_DATE,
    SOURCE_CATALOG,
    generate,
)


HERE = Path(__file__).resolve().parent
DATA = HERE / "datos"
STUDENT_README = HERE / "lab01" / "README.md"
SOLUTIONS = HERE / "lab01" / "solucion"


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


class BigLakeDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read_csv(DATA / "proveedor_a.csv")
        with (DATA / "proveedor_b.ndjson").open(encoding="utf-8") as file:
            cls.b = [json.loads(line) for line in file]
        cls.c = pq.read_table(DATA / "proveedor_c.parquet")
        cls.mapping = read_csv(DATA / "product_supplier_map.csv")
        cls.products = read_csv(DATA / "products.csv")
        cls.deliveries = read_csv(DATA / "deliveries.csv")

    def test_formats_and_schema(self):
        self.assertEqual((len(self.a), len(self.b), self.c.num_rows), (16, 16, 16))
        self.assertTrue(all(tuple(row) == A_FIELDS for row in self.a))
        self.assertTrue(all(re.fullmatch(r"\d+\.\d{2}", row["price_eur"]) for row in self.a))
        self.assertTrue(all(re.fullmatch(r"\d+", row["available_units"]) for row in self.a))
        for row in self.b:
            self.assertEqual(tuple(row), B_FIELDS)
            self.assertIs(type(row["price_cents"]), int)
            self.assertIs(type(row["stock"]), int)
            self.assertIs(type(row["product_code"]), str)
            self.assertIs(type(row["description"]), str)
        self.assertEqual(
            self.c.schema,
            pa.schema([
                pa.field("article_ref", pa.string(), nullable=False),
                pa.field("label", pa.string(), nullable=False),
                pa.field("unit_price_eur", pa.decimal128(10, 2), nullable=False),
                pa.field("units_on_hand", pa.int64(), nullable=False),
            ]),
        )

        readme = STUDENT_README.read_text(encoding="utf-8")
        schema_text, = re.findall(r"^\x60{3}json\n(.*?)\n\x60{3}$", readme, re.M | re.S)
        schema = json.loads(schema_text)
        self.assertEqual(tuple(column["name"] for column in schema), A_FIELDS)
        self.assertEqual([column["type"] for column in schema], ["STRING", "STRING", "NUMERIC", "INTEGER"])

    def test_crosswalk_and_comparable_offers(self):
        original = read_csv(SOURCE_CATALOG)
        self.assertEqual([{k: v for k, v in row.items() if k != "sales_unit"} for row in self.products], original)
        self.assertTrue(all(row["sales_unit"] for row in self.products))
        self.assertEqual({row["origin_region"] for row in self.products}, {"Comunitat Valenciana"})
        catalog = {int(row["product_id"]): row for row in self.products}
        self.assertEqual(len(catalog), 20)

        self.assertTrue(all(tuple(row) == MAP_FIELDS for row in self.mapping))
        crosswalk = {(row["supplier_id"], row["supplier_sku"]): int(row["product_id"]) for row in self.mapping}
        self.assertEqual(len(crosswalk), len(self.mapping))
        offers = (
            [("A", row["supplier_sku"], row["product_name"], Decimal(row["price_eur"]), int(row["available_units"]))
             for row in self.a]
            + [("B", row["product_code"], row["description"], Decimal(row["price_cents"]).scaleb(-2), row["stock"])
               for row in self.b]
            + [("C", row["article_ref"], row["label"], row["unit_price_eur"], row["units_on_hand"])
               for row in self.c.to_pylist()]
        )
        offer_keys = {(supplier, sku) for supplier, sku, *_ in offers}
        self.assertEqual(len(offer_keys), len(offers))
        self.assertEqual(offer_keys, set(crosswalk))
        self.assertEqual(set(crosswalk.values()), set(catalog))
        self.assertEqual(len({(s, product_id) for (s, _), product_id in crosswalk.items()}), len(crosswalk))

        by_product = defaultdict(dict)
        for supplier, sku, label, price, stock in offers:
            product = catalog[crosswalk[supplier, sku]]
            self.assertIn(product["product_name"].casefold(), label.casefold())
            self.assertGreater(price, 0)
            self.assertLess(price, Decimal(product["list_price_cents"]).scaleb(-2))
            self.assertGreaterEqual(stock, 0)
            by_product[int(product["product_id"])][supplier] = (price, stock)
        self.assertEqual(sum(len(supplier_offers) > 1 for supplier_offers in by_product.values()), 19)
        self.assertEqual(by_product[1], {
            "A": (Decimal("3.65"), 128), "B": (Decimal("3.20"), 0), "C": (Decimal("4.05"), 210),
        })

    def test_delivery_history(self):
        known_skus = {(row["supplier_id"], row["supplier_sku"]) for row in self.mapping}
        observed_skus = {(row["supplier_id"], row["supplier_sku"]) for row in self.deliveries}
        self.assertTrue(observed_skus < known_skus)
        self.assertEqual(len({row["delivery_id"] for row in self.deliveries}), 72)
        self.assertEqual(Counter(row["supplier_id"] for row in self.deliveries), {"A": 24, "B": 24, "C": 24})
        on_time = Counter()
        complete = Counter()
        for row in self.deliveries:
            self.assertEqual(tuple(row), DELIVERY_FIELDS)
            ordered, expected, delivered = (
                date.fromisoformat(row[key]) for key in ("ordered_date", "expected_date", "delivered_date")
            )
            self.assertLessEqual(ordered, min(expected, delivered))
            self.assertLessEqual(max(expected, delivered), SNAPSHOT_DATE)
            requested = int(row["ordered_units"])
            received = int(row["received_units"])
            self.assertTrue(0 < received <= requested)
            on_time[row["supplier_id"]] += delivered <= expected
            complete[row["supplier_id"]] += received == requested
        self.assertEqual(on_time, {"A": 16, "B": 18, "C": 22})
        self.assertEqual(complete, {"A": 22, "B": 16, "C": 23})

    def test_default_seed_reproduces_published_data(self):
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary)
            generate(copy / "a")
            generate(copy / "b")
            names = {file.name for file in DATA.iterdir() if file.is_file()}
            self.assertEqual(names, {file.name for file in (copy / "a").iterdir()})
            self.assertEqual(len(names), 6)
            for name in names:
                self.assertEqual((copy / "a" / name).read_bytes(), (copy / "b" / name).read_bytes(), name)
                if name.endswith(".parquet"):
                    self.assertTrue(pq.read_table(copy / "a" / name).equals(self.c))
                else:
                    self.assertEqual((copy / "a" / name).read_text(encoding="utf-8"),
                                     (DATA / name).read_text(encoding="utf-8"), name)

    def test_lab01_queries_including_challenge(self):
        statements = [path.read_text(encoding="utf-8").strip() for path in sorted(SOLUTIONS.glob("*.sql"))]
        self.assertEqual(len(statements), 4)
        examples = re.findall(
            r"^\x60{3}sql\n(.*?)\n\x60{3}$", STUDENT_README.read_text(encoding="utf-8"), re.M | re.S
        )
        self.assertEqual(examples, statements[:3])
        external_table = chr(96) + "PROJECT_ID.terra_taronja_biglake.proveedor_a_ext" + chr(96)
        with closing(sqlite3.connect(":memory:")) as db:
            db.execute("""
                CREATE TABLE proveedor_a_ext (
                    supplier_sku TEXT, product_name TEXT, price_eur NUMERIC, available_units INTEGER
                )
            """)
            db.executemany("INSERT INTO proveedor_a_ext VALUES (?, ?, ?, ?)",
                           (tuple(row[field] for field in A_FIELDS) for row in self.a))
            results = [db.execute(query.replace(external_table, "proveedor_a_ext")).fetchall() for query in statements]
        self.assertEqual(len(results[0]), 5)
        self.assertEqual(results[0][0], ("A-0107", "Naranja de Carcaixent", 3.65, 128))
        self.assertEqual(results[1], [(16,)])
        self.assertEqual(results[2], [
            ("A-0184", "Zumo de granada de Elche"), ("A-0212", "Mermelada de naranja de Gandia"),
        ])
        self.assertEqual(results[3], [
            ("A-0149", "Limón de Orihuela", 3.4, 159),
            ("A-0107", "Naranja de Carcaixent", 3.65, 128),
            ("A-0114", "Arroz bomba de Sueca", 3.81, 128),
        ])


if __name__ == "__main__":
    unittest.main(verbosity=2)
