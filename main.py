from pygments import highlight, lexers, formatters
import xmlrpc.client
import json
from tabulate import tabulate
import sys

url = "xxx.odoo.com"
db = "xxx"
username = "xx@xx.com"
password = "xxxx"
common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))


def main():
    try:
        while True:
            product_name, total_quantity = get_product()
            print()
            print(tabulate(get_quantity(product_name), headers="keys", tablefmt="github"))
            print()
            print(" " * 60, f"Total: {total_quantity:.0f}")
    except KeyboardInterrupt:
        print()
        sys.exit("Bye! ")


def get_quantity(product_name):
    results = models.execute_kw(
        db,
        uid,
        password,
        "stock.quant",
        "search_read",
        [[["product_id", "=", product_name]]],
        {"fields": ["product_id", "quantity", "location_id"]},
    )
    table = []
    finals = [
        result
        for result in sorted(results, key=lambda x: x["location_id"])
        if "Stock" in result["location_id"][1]
    ]

    for final in finals:
        table.append(
            {
                "product_name": final["product_id"][1],
                "warehouse": final["location_id"][1],
                "quantity": final["quantity"],
            }
        )
    return table


def get_product():
    barcode = input("Barcode: ").strip()
    if not barcode:
        sys.exit("Please input Valid Barcode !")
    results = models.execute_kw(
        db,
        uid,
        password,
        "product.template",
        "search_read",
        [[["barcode", "=", barcode]]],
        {"fields": ["name", "qty_available"]},
    )
    return results[0]["name"], results[0]["qty_available"]


if __name__ == "__main__":
    main()
