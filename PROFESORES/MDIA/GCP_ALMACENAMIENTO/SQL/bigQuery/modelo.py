"""Catálogo valenciano, destinos y contrato de datos de Terra Taronja."""

from dataclasses import dataclass
from datetime import date


ORIGIN_REGION = "Comunitat Valenciana"
FIRST_MONTH = date(2023, 1, 1)
LAST_DAY = date(2025, 12, 31)
MONTHS = tuple(date(year, month, 1) for year in range(2023, 2026) for month in range(1, 13))
DEFAULT_ORDERS = 1_200_000
SMALL_ORDERS = 320
DEFAULT_SEED = 27182


@dataclass(frozen=True)
class Destination:
    province: str
    region: str
    weight: int
    base_shipping: int
    cadence: float
    response: float
    program: str = "regular"
    launch: date = FIRST_MONTH
    coverage: int = 100


DESTINATIONS = (
    Destination("Valencia", ORIGIN_REGION, 66, 380, .48, .085),
    Destination("Alicante", ORIGIN_REGION, 29, 415, .29, .072),
    Destination("Castellón", ORIGIN_REGION, 20, 390, .47, .071),
    Destination("Madrid", "Comunidad de Madrid", 36, 510, .19, .076),
    Destination("Barcelona", "Cataluña", 30, 535, .21, .077),
    Destination("Murcia", "Región de Murcia", 15, 470, .32, .068),
    Destination("Sevilla", "Andalucía", 15, 615, .15, .061),
    Destination("Málaga", "Andalucía", 11, 620, .16, .061),
    Destination("Bizkaia", "País Vasco", 12, 620, .18, .070),
    Destination("Zaragoza", "Aragón", 10, 510, .29, .065, "parcial", coverage=65),
    Destination("Albacete", "Castilla-La Mancha", 7, 460, .24, .060, "parcial", coverage=72),
    Destination("Valladolid", "Castilla y León", 7, 580, .19, .058, "parcial", coverage=62),
    Destination("A Coruña", "Galicia", 10, 565, .34, .083, "piloto", date(2025, 1, 1), 47),
    Destination("Pontevedra", "Galicia", 9, 565, .45, .092, "piloto", date(2025, 1, 1), 45),
    Destination("Lugo", "Galicia", 4, 635, .28, .076, "piloto", date(2025, 3, 1), 36),
    Destination("Ourense", "Galicia", 4, 660, .23, .073, "piloto", date(2025, 3, 1), 33),
    Destination("Las Palmas", "Canarias", 7, 1085, .29, .079, "piloto", date(2025, 2, 1), 37),
    Destination("Santa Cruz de Tenerife", "Canarias", 7, 1180, .28, .074, "piloto", date(2025, 2, 1), 36),
    Destination("Girona", "Cataluña", 6, 635, .11, .090, "piloto", date(2025, 1, 1), 39),
    Destination("Cantabria", "Cantabria", 5, 665, .28, .057, "piloto", date(2025, 2, 1), 38),
    Destination("Granada", "Andalucía", 5, 665, .12, .063, "piloto", date(2025, 1, 1), 44),
    Destination("Illes Balears", "Illes Balears", 5, 970, .20, .062, "piloto", date(2025, 2, 1), 44),
)


@dataclass(frozen=True)
class Supplier:
    supplier_id: int
    supplier_name: str
    province: str
    fill_rate: float
    late_rate: float
    cost_factor: float


# Razones sociales de ficción. Las tasas se usan al simular, no se exportan.
SUPPLIERS = (
    Supplier(1, "Horta i Camp", "Valencia", .86, .20, .98),
    Supplier(2, "Cooperativa del Xúquer", "Valencia", .97, .07, 1.04),
    Supplier(3, "Obrador del Túria", "Valencia", .94, .10, 1.00),
    Supplier(4, "Camp del Sénia", "Castellón", .88, .16, .97),
    Supplier(5, "Cooperativa de la Plana", "Castellón", .97, .06, 1.03),
    Supplier(6, "Terres del Maestrat", "Castellón", .92, .14, 1.01),
    Supplier(7, "Collita de la Marina", "Alicante", .89, .16, .97),
    Supplier(8, "Obrador del Vinalopó", "Alicante", .96, .07, 1.03),
    Supplier(9, "Cooperativa del Serpis", "Valencia", .95, .08, 1.02),
    Supplier(10, "Camp del Montgó", "Alicante", .93, .11, .99),
)
SUPPLIER_BY_ID = {vendor.supplier_id: vendor for vendor in SUPPLIERS}


@dataclass(frozen=True)
class Product:
    product_name: str
    category: str
    origin_province: str
    origin_locality: str
    list_price_cents: int
    supplier_ids: tuple[int, int]
    weight: int
    cost_share: float
    return_rate: float
    season: tuple[int, ...] = ()
    catalog_since: date = FIRST_MONTH


PRODUCTS = (
    Product("Naranja de Carcaixent", "Cítricos", "Valencia", "Carcaixent", 550, (1, 2), 15, .56, .024, (11, 12, 1, 2, 3)),
    Product("Mandarina de Nules", "Cítricos", "Castellón", "Nules", 640, (4, 5), 12, .59, .025, (10, 11, 12, 1, 2)),
    Product("Limón de Orihuela", "Cítricos", "Alicante", "Orihuela", 460, (7, 8), 8, .56, .019, (1, 2, 3, 4)),
    Product("Caja de cítricos de la Ribera", "Cítricos", "Valencia", "Alzira", 1490, (1, 2), 9, .63, .028, (11, 12, 1, 2)),
    Product("Arroz bomba de Sueca", "Despensa", "Valencia", "Sueca", 615, (2, 9), 13, .54, .010),
    Product("Almendra tostada de Xixona", "Despensa", "Alicante", "Xixona", 720, (8, 10), 8, .58, .013),
    Product("Rosquilletas de València", "Despensa", "Valencia", "València", 375, (3, 9), 7, .53, .012),
    Product("Garrofón de Cullera", "Despensa", "Valencia", "Cullera", 510, (2, 9), 6, .55, .010),
    Product("Horchata de Alboraya", "Bebidas", "Valencia", "Alboraia", 590, (3, 1), 13, .60, .032, (5, 6, 7, 8, 9)),
    Product("Zumo de naranja de Carcaixent", "Bebidas", "Valencia", "Carcaixent", 390, (1, 3), 10, .57, .020),
    Product("Zumo de granada de Elche", "Bebidas", "Alicante", "Elche", 465, (7, 8), 6, .57, .017, (9, 10, 11, 12)),
    Product("Aceite de oliva de Viver", "Aceites y miel", "Castellón", "Viver", 1290, (5, 6), 8, .64, .014),
    Product("Miel de la Vall d'Alba", "Aceites y miel", "Castellón", "la Vall d’Alba", 790, (6, 5), 7, .55, .012),
    Product("Miel de la Marina", "Aceites y miel", "Alicante", "Teulada", 890, (10, 8), 6, .56, .013),
    Product("Alcachofa en conserva de Benicarló", "Conservas vegetales", "Castellón", "Benicarló", 690, (4, 6), 9, .69, .088, (1, 2, 3), date(2025, 4, 1)),
    Product("Pimiento asado de Guardamar", "Conservas vegetales", "Alicante", "Guardamar del Segura", 590, (7, 8), 8, .66, .074, (), date(2025, 4, 1)),
    Product("Salmorreta de El Campello", "Conservas vegetales", "Alicante", "El Campello", 555, (8, 10), 7, .60, .053, (), date(2025, 4, 1)),
    Product("Turrón blando de Xixona", "Dulces artesanos", "Alicante", "Xixona", 1050, (8, 10), 6, .49, .020, (10, 11, 12), date(2025, 9, 1)),
    Product("Mermelada de naranja de Gandia", "Dulces artesanos", "Valencia", "Gandia", 545, (9, 3), 5, .53, .017, (11, 12), date(2025, 9, 1)),
    Product("Coca dulce de la Vall d’Uixó", "Dulces artesanos", "Castellón", "la Vall d’Uixó", 720, (5, 6), 4, .52, .035, (11, 12), date(2025, 9, 1)),
)
PRODUCT_BY_ID = dict(enumerate(PRODUCTS, 1))


CUSTOMER_GIVEN_NAMES = (
    "Adrià", "Alba", "Alejandro", "Ana", "Ariadna", "Ausiàs", "Carmen", "Clara",
    "Cristina", "Daniel", "Elena", "Enric", "Eva", "Ferran", "Hugo", "Isabel",
    "Jaume", "Júlia", "Laura", "Lucía", "Marc", "María", "Marta", "Miquel",
    "Nerea", "Núria", "Pau", "Pilar", "Raquel", "Sergio", "Teresa", "Vicent",
)
CUSTOMER_SURNAMES = (
    "Aguilar", "Alberola", "Alonso", "Beltrán", "Benavent", "Blasco", "Calatayud",
    "Campos", "Casanova", "Cerdà", "Coll", "Cortés", "Doménech", "Ferrer", "Fuster",
    "García", "Giménez", "Gómez", "Herrero", "Ibáñez", "Jordà", "Llorens", "López",
    "Martí", "Martínez", "Molina", "Navarro", "Ortiz", "Pastor", "Pérez", "Ramírez",
    "Romero", "Ruiz", "Sanchis", "Santos", "Soler", "Torres", "Vidal",
)


def schema(fields):
    return tuple(tuple(field.split(":")) for field in fields.split())


SCHEMAS = {
    "customers": schema(
        "customer_id:INT64 customer_type:STRING province:STRING region:STRING "
        "registered_date:DATE first_order_date:DATE customer_name:STRING email:STRING"
    ),
    "orders": schema(
        "order_id:INT64 order_date:DATE customer_id:INT64 customer_type:STRING province:STRING region:STRING "
        "campaign:STRING delivery_date:DATE delivery_incident:BOOL "
        "gross_cents:INT64 discount_cents:INT64 refund_cents:INT64 product_cost_cents:INT64 "
        "shipping_paid_cents:INT64 shipping_cost_cents:INT64 service_cost_cents:INT64 "
        "net_cents:INT64 contribution_cents:INT64"
    ),
    "order_items": schema(
        "order_id:INT64 line_number:INT64 product_id:INT64 supplier_id:INT64 quantity:INT64 "
        "unit_price_cents:INT64 unit_cost_cents:INT64 discount_cents:INT64 returned_quantity:INT64 refund_cents:INT64"
    ),
    "products": schema(
        "product_id:INT64 product_name:STRING category:STRING origin_region:STRING origin_province:STRING "
        "origin_locality:STRING list_price_cents:INT64 catalog_since:DATE"
    ),
    "suppliers": schema("supplier_id:INT64 supplier_name:STRING origin_region:STRING province:STRING"),
    "supplier_monthly": schema(
        "month_start:DATE product_id:INT64 supplier_id:INT64 requested_units:INT64 fulfilled_units:INT64 "
        "planned_units:INT64 received_units:INT64 shipments:INT64 late_shipments:INT64 stockout_days:INT64"
    ),
    "territory_monthly": schema(
        "month_start:DATE province:STRING region:STRING sales_program:STRING coverage_pct:INT64 qualified_contacts:INT64"
    ),
}

SMALL_SALES = schema(
    "order_id:INT64 order_date:DATE province:STRING product_name:STRING category:STRING "
    "origin_province:STRING quantity:INT64 unit_price_cents:INT64 line_net_cents:INT64"
)
