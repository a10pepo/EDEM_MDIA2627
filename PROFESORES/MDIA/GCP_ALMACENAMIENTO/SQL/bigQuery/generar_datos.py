"""Genera CSV deterministas en streaming. Solo usa la biblioteca estándar."""

import argparse
import csv
from calendar import monthrange
from collections import Counter
from contextlib import ExitStack
from datetime import timedelta
from functools import lru_cache
from pathlib import Path
from random import Random

from modelo import (
    CUSTOMER_GIVEN_NAMES, CUSTOMER_SURNAMES,
    DEFAULT_ORDERS, DEFAULT_SEED, DESTINATIONS, FIRST_MONTH, LAST_DAY, MONTHS,
    ORIGIN_REGION, PRODUCT_BY_ID, SCHEMAS, SMALL_ORDERS, SMALL_SALES,
    SUPPLIER_BY_ID, SUPPLIERS,
)


@lru_cache(maxsize=None)
def month_distribution(launch):
    eligible = tuple(month for month in MONTHS if month >= launch)
    weights = tuple(
        (1 + .13 * (month.year - FIRST_MONTH.year))
        * (1.32 if month.month in (11, 12) else .84 if month.month in (7, 8) else 1)
        for month in eligible
    )
    return eligible, weights


def customer_orders(rng, destination, customer_type):
    months, weights = month_distribution(destination.launch)
    month = rng.choices(months, weights)[0]
    first = month.replace(day=rng.randint(1, monthrange(month.year, month.month)[1]))
    scheduled = rng.random() < destination.cadence

    if customer_type == "restaurante":
        count, interval = rng.randint(5, 13), rng.choice((7, 14, 21))
        scheduled = rng.random() < .81
    elif customer_type == "gran_empresa":
        count, interval = rng.randint(1, 5), rng.choice((14, 28))
        scheduled = rng.random() < .24
    elif scheduled:
        count, interval = rng.randint(4, 10), rng.choice((14, 28))
    else:
        count, interval = rng.choices((1, 2, 3, 4, 5), (48, 24, 15, 9, 4))[0], 0

    dates = [first]
    for _ in range(count - 1):
        gap = interval + rng.randint(-2, 2) if scheduled else rng.randint(4, 120)
        following = dates[-1] + timedelta(days=gap)
        if following > LAST_DAY:
            break
        dates.append(following)
    return dates, scheduled


@lru_cache(maxsize=None)
def product_distribution(month, customer_type):
    eligible = []
    weights = []
    for product_id, product in PRODUCT_BY_ID.items():
        if product.catalog_since > month:
            continue
        weight = product.weight
        if product.season:
            weight *= 1.8 if month.month in product.season else .65
        if customer_type == "restaurante" and product.category in ("Despensa", "Conservas vegetales"):
            weight *= 1.55
        eligible.append(product_id)
        weights.append(weight)
    return eligible, weights


def basket(rng, month, customer_type, favorites):
    size = rng.choices((2, 3, 4, 5), (28, 45, 23, 4))[0]
    eligible, weights = product_distribution(month, customer_type)
    ids = [product_id for product_id in favorites if rng.random() < .86][:size]
    while len(ids) < size:
        product_id = rng.choices(eligible, weights)[0]
        if product_id not in ids:
            ids.append(product_id)
    return ids


def item(rng, order_id, line, product_id, customer_type, campaign, contract, sold_on):
    product = PRODUCT_BY_ID[product_id]
    # La asignación cambia con la estación y los lotes. Hay contratos secundarios.
    primary_share = .77 + (.07 if sold_on.month in product.season else 0) - (.11 if sold_on.month in (4, 8) else 0)
    supplier_id = product.supplier_ids[0 if rng.random() < primary_share else 1]
    supplier = SUPPLIER_BY_ID[supplier_id]
    if customer_type == "gran_empresa":
        quantity = rng.randint(9, 44)
        rate = rng.uniform(.08, .16) if contract else rng.uniform(.21, .37)
    elif customer_type == "restaurante":
        quantity = rng.randint(2, 8)
        rate = rng.uniform(.03, .11)
    else:
        quantity = rng.choices((1, 2, 3, 4), (50, 33, 13, 4))[0]
        rate = rng.uniform(.03, .15) if campaign != "sin_campana" else 0

    if product.category == "Conservas vegetales" and campaign != "sin_campana":
        rate += rng.uniform(.08, .18)
    price = round(product.list_price_cents * rng.uniform(.94, 1.08))
    unit_cost = round(product.list_price_cents * product.cost_share * supplier.cost_factor * rng.uniform(.94, 1.07))
    gross = quantity * price
    discount = round(gross * rate)
    returned = rng.randint(1, max(1, quantity // 2)) if rng.random() < product.return_rate else 0
    refund = (gross - discount) * returned // quantity
    return (order_id, line, product_id, supplier_id, quantity, price, unit_cost, discount, returned, refund)


def logistics(rng, destination, customer_type, units, net, returned, sold_on, contract):
    island = destination.region in ("Canarias", "Illes Balears")
    incident = rng.random() < (.14 if island else .065) + (.05 if sold_on.month == 12 else 0)
    lead = rng.randint(4, 7) if island else rng.randint(1, 4)
    if incident:
        lead += rng.randint(1, 5)
    shipping_cost = max(150, destination.base_shipping + 17 * units + rng.randint(-105, 150) + 150 * incident)
    if customer_type == "gran_empresa":
        shipping_paid, service = (650 if contract else 0), rng.randint(300, 750) if contract else rng.randint(1350, 4000)
    elif customer_type == "restaurante":
        shipping_paid, service = (490 if net < 12000 else 0), rng.randint(75, 260)
    else:
        shipping_paid = (890 if net < 8200 else 430) if island else (495 if net < 5800 else 0)
        service = rng.randint(35, 110)
    return sold_on + timedelta(days=lead), incident, shipping_paid, shipping_cost, service + 140 * incident + 90 * returned


def campaign_for(rng, sold_on, destination, first_order):
    if sold_on.month in (11, 12) and rng.random() < .33:
        return "navidad"
    if first_order and rng.random() < .29:
        return "bienvenida"
    if destination.program != "regular" and rng.random() < .22:
        return "campana_local"
    return "temporada" if rng.random() < .13 else "sin_campana"


def write_monthly(writers, rng, sold_units, first_purchases):
    for month in MONTHS:
        days = monthrange(month.year, month.month)[1]
        for product_id, product in PRODUCT_BY_ID.items():
            if product.catalog_since > month:
                continue
            for supplier_id in product.supplier_ids:
                supplier = SUPPLIER_BY_ID[supplier_id]
                fulfilled = sold_units[month, product_id, supplier_id]
                pressure = .045 if month.month in product.season else 0
                fill = min(.995, max(.6, supplier.fill_rate - pressure + rng.uniform(-.075, .065)))
                unmet = max(.01, (1 - fill) * rng.uniform(.4, 1.0))
                requested = round(fulfilled / (1 - unmet))
                received = fulfilled + round(fulfilled * rng.uniform(.02, .12))
                planned = round(received / fill)
                shipments = (planned + 179) // 180
                late_rate = max(0, supplier.late_rate - (fill - supplier.fill_rate) / 2 + rng.uniform(-.04, .06))
                late = min(shipments, round(shipments * late_rate))
                stockout_days = min(days, max(0, round((1 - fill) * 40 + rng.gauss(-1.9, 2.0)))) if fulfilled else 0
                writers["supplier_monthly"].writerow(
                    (month, product_id, supplier_id, requested, fulfilled, planned, received,
                     shipments, late, stockout_days)
                )
        for destination in DESTINATIONS:
            if destination.launch > month:
                continue
            buyers = first_purchases[month, destination.province]
            season = 1.09 if month.month in (11, 12) else 1
            response = destination.response * season * rng.uniform(.77, 1.24)
            contacts = round(buyers / response)
            coverage = destination.coverage if destination.program == "regular" else (
                destination.coverage + rng.randint(-5, 5)
            )
            writers["territory_monthly"].writerow(
                (month, destination.province, destination.region, destination.program, coverage, contacts)
            )


def products_rows():
    for product_id, product in PRODUCT_BY_ID.items():
        yield (product_id, product.product_name, product.category, ORIGIN_REGION, product.origin_province,
               product.origin_locality, product.list_price_cents, product.catalog_since)


def generate(output, order_count, seed, small=False):
    if order_count < 1:
        raise ValueError("El número de pedidos debe ser positivo.")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    rng = Random(seed)
    # Los nombres usan su propia secuencia para conservar el histórico de cada semilla.
    contact_rng = Random(f"customers:{seed}")
    sold_units, first_purchases = Counter(), Counter()
    destination_weights = [destination.weight for destination in DESTINATIONS]
    schemas = {"ventas": SMALL_SALES, "products": SCHEMAS["products"]} if small else SCHEMAS

    with ExitStack() as stack:
        writers = {}
        for table, fields in schemas.items():
            file = stack.enter_context((output / f"{table}.csv").open("w", encoding="utf-8", newline=""))
            writers[table] = csv.writer(file, lineterminator="\n")
            writers[table].writerow(name for name, _ in fields)
        writers["products"].writerows(products_rows())
        if not small:
            writers["suppliers"].writerows(
                (vendor.supplier_id, vendor.supplier_name, ORIGIN_REGION, vendor.province)
                for vendor in SUPPLIERS
            )

        order_id = customer_id = lines = 0
        while order_id < order_count:
            customer_id += 1
            destination = rng.choices(DESTINATIONS, destination_weights)[0]
            customer_type = rng.choices(("particular", "restaurante", "gran_empresa"), (87, 11, 2))[0]
            contract = customer_type == "gran_empresa" and rng.random() < .24
            dates, scheduled = customer_orders(rng, destination, customer_type)
            dates = dates[:order_count - order_id]
            registered = dates[0] - timedelta(days=rng.randint(0, 75))
            first_month = dates[0].replace(day=1)
            first_purchases[first_month, destination.province] += 1
            if not small:
                given_name = contact_rng.choice(CUSTOMER_GIVEN_NAMES)
                surnames = contact_rng.choices(CUSTOMER_SURNAMES, k=2)
                customer_name = " ".join([given_name, *surnames])
                email = f"cliente{customer_id}@example.com"
                writers["customers"].writerow(
                    (customer_id, customer_type, destination.province, destination.region, registered, dates[0],
                     customer_name, email)
                )
            favorites = basket(rng, first_month, customer_type, ())[:rng.randint(2, 3)] if scheduled else ()
            for sold_on in dates:
                order_id += 1
                month = sold_on.replace(day=1)
                campaign = campaign_for(rng, sold_on, destination, sold_on == dates[0])
                items = [item(rng, order_id, line, product_id, customer_type, campaign, contract, sold_on)
                         for line, product_id in enumerate(basket(rng, month, customer_type, favorites), 1)]
                lines += len(items)
                gross = discount = refund = cost = units = returned = 0
                for row in items:
                    _, _, product_id, supplier_id, qty, price, unit_cost, saving, back, money_back = row
                    gross += qty * price
                    discount += saving
                    refund += money_back
                    cost += qty * unit_cost
                    units += qty
                    returned += back
                    sold_units[month, product_id, supplier_id] += qty
                    if small:
                        product = PRODUCT_BY_ID[product_id]
                        writers["ventas"].writerow(
                            (order_id, sold_on, destination.province, product.product_name, product.category,
                             product.origin_province, qty, price, qty * price - saving - money_back)
                        )
                    else:
                        writers["order_items"].writerow(row)
                net = gross - discount - refund
                delivered, incident, shipping_paid, shipping_cost, service = logistics(
                    rng, destination, customer_type, units, net, returned, sold_on, contract
                )
                if not small:
                    writers["orders"].writerow(
                        (order_id, sold_on, customer_id, customer_type, destination.province, destination.region,
                         campaign, delivered, str(incident).lower(), gross, discount, refund, cost,
                         shipping_paid, shipping_cost, service, net, net + shipping_paid - cost - shipping_cost - service)
                    )
        if not small:
            write_monthly(writers, rng, sold_units, first_purchases)
    return order_id, lines, customer_id


def main():
    parser = argparse.ArgumentParser(description="Genera datos de Terra Taronja sin acceder a GCP.")
    parser.add_argument("--small", action="store_true", help="Genera ventas.csv y products.csv del Lab 1.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    scale = parser.add_mutually_exclusive_group()
    scale.add_argument("--scale", type=float, help=f"Multiplicador de {DEFAULT_ORDERS} pedidos, o {SMALL_ORDERS} con --small.")
    scale.add_argument("--orders", type=int, help="Número exacto de pedidos.")
    args = parser.parse_args()
    base = SMALL_ORDERS if args.small else DEFAULT_ORDERS
    try:
        count = args.orders if args.orders is not None else round(base * (args.scale if args.scale is not None else 1))
        orders, lines, customers = generate(args.output, count, args.seed, small=args.small)
    except (ValueError, OverflowError) as error:
        parser.error(str(error))
    print(f"{orders:,} pedidos, {lines:,} líneas y {customers:,} clientes en {args.output}")


if __name__ == "__main__":
    main()
