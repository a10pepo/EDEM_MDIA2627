"""Genera datos sintéticos de la clase de BigLake sin acceder a Google Cloud."""

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from random import Random

import pyarrow as pa
import pyarrow.parquet as pq


HERE = Path(__file__).resolve().parent
SOURCE_CATALOG = HERE.parent / "bigQuery" / "lab01" / "datos" / "products.csv"
DEFAULT_SEED = 27182
SNAPSHOT_DATE = date(2026, 4, 30)
FIRST_DELIVERY_ORDER = date(2026, 1, 5)
DELIVERIES_PER_SUPPLIER = 24

SALES_UNITS = {
    1: "bolsa de 1 kg", 2: "bolsa de 1 kg", 3: "bolsa de 1 kg",
    4: "caja de 3 kg", 5: "paquete de 1 kg", 6: "bolsa de 250 g",
    7: "paquete de 200 g", 8: "bolsa de 500 g", 9: "botella de 1 L",
    10: "botella de 1 L", 11: "botella de 750 mL", 12: "botella de 750 mL",
    13: "tarro de 350 g", 14: "tarro de 350 g", 15: "tarro de 300 g",
    16: "tarro de 250 g", 17: "tarro de 180 g", 18: "tableta de 300 g",
    19: "tarro de 240 g", 20: "caja de 6 piezas",
}

A_FIELDS = ("supplier_sku", "product_name", "price_eur", "available_units")
B_FIELDS = ("product_code", "description", "price_cents", "stock")
C_SCHEMA = pa.schema([
    pa.field("article_ref", pa.string(), nullable=False),
    pa.field("label", pa.string(), nullable=False),
    pa.field("unit_price_eur", pa.decimal128(10, 2), nullable=False),
    pa.field("units_on_hand", pa.int64(), nullable=False),
])
MAP_FIELDS = ("supplier_id", "supplier_sku", "product_id")
DELIVERY_FIELDS = (
    "delivery_id", "supplier_id", "supplier_sku", "ordered_date", "expected_date",
    "delivered_date", "ordered_units", "received_units",
)


@dataclass(frozen=True)
class Supplier:
    code: str
    product_ids: tuple[int, ...]
    price_percent: tuple[int, int]
    availability: tuple[int, int]
    late_percent: int
    partial_percent: int


SUPPLIERS = (
    Supplier("A", (1, 5, 9, 2, 7, 12, 3, 4, 6, 8, 10, 11, 13, 15, 17, 19),
             (62, 76), (24, 180), 25, 15),
    Supplier("B", (2, 11, 5, 9, 1, 6, 12, 3, 8, 10, 14, 15, 16, 17, 18, 20),
             (54, 68), (12, 125), 45, 30),
    Supplier("C", (9, 5, 1, 12, 2, 13, 4, 6, 7, 11, 14, 15, 17, 18, 19, 20),
             (68, 84), (50, 250), 10, 8),
)
# Las tres ofertas de naranja permiten comparar precio y stock con un caso estable.
ORANGE_OFFERS = {"A": (365, 128), "B": (320, 0), "C": (405, 210)}
OUT_OF_STOCK = {("A", 11), ("A", 19), ("B", 18)}


@dataclass(frozen=True)
class Offer:
    supplier_id: str
    sku: str
    product_id: int
    price_cents: int
    available_units: int

    @property
    def price_eur(self):
        return Decimal(self.price_cents).scaleb(-2)


def read_catalog():
    products = {}
    with SOURCE_CATALOG.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            product_id = int(row["product_id"])
            if product_id not in SALES_UNITS:
                continue
            if product_id in products or row["origin_region"] != "Comunitat Valenciana":
                raise ValueError(f"Producto repetido o de origen inesperado: {product_id}")
            products[product_id] = {**row, "sales_unit": SALES_UNITS[product_id]}
    if products.keys() != SALES_UNITS.keys():
        raise ValueError("Faltan identificadores del catálogo de BigQuery.")
    return products


def supplier_offers(supplier, products, rng):
    for position, product_id in enumerate(supplier.product_ids, 1):
        list_price = int(products[product_id]["list_price_cents"])
        price = (list_price * rng.randint(*supplier.price_percent) + 50) // 100
        stock = rng.randint(*supplier.availability)
        if product_id == 1:
            price, stock = ORANGE_OFFERS[supplier.code]
        elif (supplier.code, product_id) in OUT_OF_STOCK:
            stock = 0
        yield Offer(supplier.code, f"{supplier.code}-{100 + 7 * position:04d}", product_id, price, stock)


def supplier_deliveries(supplier, offers, rng):
    sku_by_product = {offer.product_id: offer.sku for offer in offers}
    history_products = (1, 2, 5, 9, 12, supplier.product_ids[-1])
    for position in range(DELIVERIES_PER_SUPPLIER):
        product_id = history_products[position % len(history_products)]
        ordered_date = FIRST_DELIVERY_ORDER + timedelta(days=4 * position + rng.randint(0, 2))
        expected_date = ordered_date + timedelta(days=rng.randint(3, 6))
        if rng.randrange(100) < supplier.late_percent:
            days_from_expected = rng.randint(1, 4)
        else:
            days_from_expected = rng.randint(-2, 0)
        delivered_date = expected_date + timedelta(days=days_from_expected)
        ordered_units = rng.randrange(24, 121, 6)
        received_units = ordered_units
        if rng.randrange(100) < supplier.partial_percent:
            received_units -= max(1, ordered_units * rng.randint(10, 30) // 100)
        yield (f"{supplier.code}-E{position + 1:03d}", supplier.code, sku_by_product[product_id],
               ordered_date, expected_date, delivered_date, ordered_units, received_units)


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(rows)


def generate(output, seed=DEFAULT_SEED):
    products = read_catalog()
    rng = Random(seed)
    offers = {supplier.code: list(supplier_offers(supplier, products, rng)) for supplier in SUPPLIERS}
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)

    product_rows = list(products.values())
    write_csv(output / "products.csv", product_rows[0].keys(), (row.values() for row in product_rows))
    write_csv(
        output / "proveedor_a.csv", A_FIELDS,
        ((offer.sku, products[offer.product_id]["product_name"], offer.price_eur, offer.available_units)
         for offer in offers["A"]),
    )
    with (output / "proveedor_b.ndjson").open("w", encoding="utf-8", newline="\n") as file:
        for offer in offers["B"]:
            product = products[offer.product_id]
            values = (offer.sku, f'{product["product_name"]} ({product["sales_unit"]})',
                      offer.price_cents, offer.available_units)
            file.write(json.dumps(dict(zip(B_FIELDS, values)), ensure_ascii=False) + "\n")

    parquet_rows = [
        {
            "article_ref": offer.sku,
            "label": products[offer.product_id]["product_name"].upper(),
            "unit_price_eur": offer.price_eur,
            "units_on_hand": offer.available_units,
        }
        for offer in offers["C"]
    ]
    pq.write_table(pa.Table.from_pylist(parquet_rows, schema=C_SCHEMA), output / "proveedor_c.parquet",
                   compression="snappy", version="1.0")
    write_csv(
        output / "product_supplier_map.csv", MAP_FIELDS,
        ((offer.supplier_id, offer.sku, offer.product_id) for rows in offers.values() for offer in rows),
    )
    write_csv(
        output / "deliveries.csv", DELIVERY_FIELDS,
        (row for supplier in SUPPLIERS for row in supplier_deliveries(supplier, offers[supplier.code], rng)),
    )
    return {code: len(rows) for code, rows in offers.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output", type=Path, default=HERE / "datos")
    args = parser.parse_args()
    counts = generate(args.output, args.seed)
    print(", ".join(f"Proveedor {code}: {count} ofertas" for code, count in counts.items()))
    print(f"{len(SUPPLIERS) * DELIVERIES_PER_SUPPLIER} entregas y catálogo en {args.output}")


if __name__ == "__main__":
    main()
