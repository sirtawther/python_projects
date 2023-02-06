import xmlrpc.client
import sys
import os
import time
from pyfiglet import Figlet
import re
import csv
import getpass

# Authenication For Odoo according to the Odoo XML RPC Protocol

url = ""
db = ""
username = ""
password = ""
common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))


def main():
    while True:
        f = Figlet(font="slant")
        print(f.renderText("Welcome"))
        print("1. Subscriber Program")
        print("2. Loyalty Points Editor")
        print("3. Customer & Account Association")
        print("4. Admin Tools")
        print()
        try:
            choice: int = int(input("Choice: ").strip())

            if choice == 1:
                clear_output(1.5)

                while True:
                    f = Figlet(font="small")
                    print(f.renderText("Subscriber Program"))
                    global member_id
                    try:
                        member_id = int(input("Enter Customer ID: ").strip())

                        global customer_results
                        global get_customer
                        customer_results = get_customer(member_id)

                        if len(customer_results) == 1:
                            print()
                            customer_print(customer_results)
                            if (
                                input(
                                    f"Add {customer_results[0]['name']} to Subscriber Program? (Y/N): "
                                ).lower()
                                == "y"
                            ):

                                models.execute_kw(
                                    db,
                                    uid,
                                    password,
                                    "res.partner",
                                    "write",
                                    [[member_id], {"customer_level": "Subscriber"}],
                                )
                                models.execute_kw(
                                    db,
                                    uid,
                                    password,
                                    "res.partner",
                                    "write",
                                    [[member_id], {"category_id": [1]}],
                                )

                                results = rule_partners_domain()
                                if (
                                    "|" in results and "]]" in results
                                ) and f'["id","=",{member_id}]' not in results:
                                    new = results.replace('["|",', '["|","|",')
                                    new = new.replace(
                                        "]]", f'],["id","=",{member_id}]]'
                                    )

                                    models.execute_kw(
                                        db,
                                        uid,
                                        password,
                                        "coupon.program",
                                        "write",
                                        [[16], {"rule_partners_domain": f"{new}"}],
                                    )
                                    print()
                                    print(
                                        f"{customer_results[0]['name']} has been added to Subscriber List Successfully !"
                                    )
                                    models.execute_kw(
                                        db,
                                        uid,
                                        password,
                                        "mail.message",
                                        "create",
                                        [
                                            {
                                                "body": "Subscriber Added by IT Team.",
                                                "model": "res.partner",
                                                "message_type": "comment",
                                                "res_id": member_id,
                                                "author_id": 3,
                                            }
                                        ],
                                    )
                                    print()
                                    clear_output(2.5)

                                else:
                                    print()
                                    print(
                                        f"{customer_results[0]['name']} is already Subscriber !"
                                    )
                                    clear_output(2.5)
                            else:
                                print("Operation Cancelled")
                                clear_output(2.5)
                        else:
                            print()
                            print("Customer Not Found! Wrong ID? ")
                            clear_output(2.5)

                    except (ValueError, OverflowError, KeyboardInterrupt):
                        print()
                        print("Wrong Member ID,please try again?")
                        clear_output(2.5)
                        break

            elif choice == 2:
                clear_output(1.5)

                while True:
                    try:
                        f = Figlet(font="small")
                        print(f.renderText("Loyalty Points"))
                        member_id = int(input("Enter Customer ID: ").strip())
                        print()
                        customer_results = get_customer(member_id)
                        if len(customer_results) == 0:
                            print("Customer Not Found")
                            clear_output(2.5)
                        else:
                            customer_print(customer_results)
                            try:
                                old_points = customer_results[0]["loyalty_points"]
                                new_points = int(input("Set Loyalty Points: ").strip())
                                print()
                                if old_points < new_points:
                                    models.execute_kw(
                                        db,
                                        uid,
                                        password,
                                        "mail.message",
                                        "create",
                                        [
                                            {
                                                "body": f"Previous points: {old_points}, added {new_points-old_points}, new points: {new_points} (IT Team).",
                                                "model": "res.partner",
                                                "message_type": "comment",
                                                "res_id": member_id,
                                                "author_id": 3,
                                            }
                                        ],
                                    )
                                    models.execute_kw(
                                        db,
                                        uid,
                                        password,
                                        "all.loyalty.history",
                                        "create",
                                        [
                                            {
                                                "partner_id": member_id,
                                                "transaction_type": "credit",
                                                "points": new_points-old_points,
                                                "state": "done",
                                                "company_id": 1,
                                            }
                                        ],
                                    )
                                    print(
                                        f"Adding {new_points-old_points} loyalty points........"
                                    )
                                elif old_points == new_points:
                                    print("Same loyalt points, no need to upate! ")
                                else:
                                    models.execute_kw(
                                        db,
                                        uid,
                                        password,
                                        "mail.message",
                                        "create",
                                        [
                                            {
                                                "body": f"Previous points: {old_points}, subtracted {old_points-new_points}, new points: {new_points} (IT Team).",
                                                "model": "res.partner",
                                                "message_type": "comment",
                                                "res_id": member_id,
                                                "author_id": 3,
                                            }
                                        ],
                                    )
                                    models.execute_kw(
                                        db,
                                        uid,
                                        password,
                                        "all.loyalty.history",
                                        "create",
                                        [
                                            {
                                                "partner_id": member_id,
                                                "transaction_type": "debit",
                                                "points": old_points - new_points,
                                                "state": "done",
                                                "company_id": 1,
                                            }
                                        ],
                                    )
                                    print(
                                        f"Subtracting {old_points - new_points} loyalty points from customer........ "
                                    )
                                time.sleep(2.5)
                                models.execute_kw(
                                    db,
                                    uid,
                                    password,
                                    "res.partner",
                                    "write",
                                    [[member_id], {"loyalty_points": new_points}],
                                )

                                time.sleep(1.5)
                                print()
                                print(f"New Loyalty Points: {new_points}")
                                clear_output(4.5)
                            except (ValueError,OverflowError):
                                print()
                                print("Invalid Loyalty Amount")
                                clear_output(2)

                    except (ValueError, OverflowError,KeyboardInterrupt):
                        print()
                        print("Invalid Customer ID")
                        clear_output(2.5)
                        break

            elif choice == 3:
                # while True:
                #     try:
                while True:
                    clear_output(1)
                    f = Figlet(font="small")
                    print(f.renderText("Assocation"))
                    try:
                        member_id = int(input("Enter Customer ID: ").strip())
                        customer_results = get_customer(member_id)
                        if len(customer_results) == 1:
                            customer_print(customer_results)
                            print()
                            associate_action = input("Do you Want to Associate?(Y/N): ").lower()
                            if associate_action == "y":
                                models.execute_kw(
                                    db,
                                    uid,
                                    password,
                                    "res.partner",
                                    "write",
                                    [[member_id], {"property_account_receivable_id": 2609,
                                                   "property_account_payable_id": 2726}],
                                )
                                print("Associated Successfully! ")
                                clear_output(2)
                            else:
                                print("Operation Cancelled!")
                                clear_output(1)
                        else:
                            print()
                            print("Customer Not Found!")
                            clear_output(0.8)

                    except (ValueError, OverflowError, KeyboardInterrupt):
                        print()
                        print("Operation Interrupted!")
                        clear_output(2.5)
                        break



            elif choice == 4:
                print()
                clear_output(1)
                f = Figlet(font="slant")
                print(f.renderText("Admin Login"))
                username_tool = input("Username: ")
                print()
                password_tool = getpass.getpass("Password: ")

                admin_lists = {"user1": ["admin", "696969"]}

                if (
                    admin_lists["user1"][0] == username_tool
                    and admin_lists["user1"][1] == password_tool
                ):
                    print()
                    print("Login Successful! ")
                    clear_output(1.5)
                    while True:

                        try:
                            f = Figlet(font="slant")
                            print(f.renderText("Admin Tools"))
                            print("1. Subscriber Deletion")
                            print("2. Subscriber Export")
                            print()
                            choice_tool: int = int(input("Choice: "))

                            if choice_tool == 1:
                                clear_output(1)
                                while True:
                                    f = Figlet(font="small")
                                    print(f.renderText("Subscriber Deletion"))
                                    try:
                                        member_id = int(input("Delete ID: ").strip())
                                        results = rule_partners_domain()
                                        customer_results = get_customer(member_id)
                                        if len(customer_results) != 0:
                                            print()
                                            customer_print(customer_results)

                                            if (
                                                input(
                                                    f"Remove {customer_results[0]['name']} from Subscriber Program? (Y/N): "
                                                ).lower()
                                                == "y"
                                            ):

                                                if (
                                                    len(customer_results) == 1
                                                    and (
                                                        '["|","|","|"' in results
                                                        and "]]" in results
                                                    )
                                                    and f'["id","=",{member_id}]' in results
                                                ):
                                                    delete = results.replace('["|",', "[")
                                                    delete = delete.replace(
                                                        f',["id","=",{member_id}]', ""
                                                    )
                                                    models.execute_kw(
                                                        db,
                                                        uid,
                                                        password,
                                                        "coupon.program",
                                                        "write",
                                                        [
                                                            [16],
                                                            {
                                                                "rule_partners_domain": f"{delete}"
                                                            },
                                                        ],
                                                    )
                                                    models.execute_kw(
                                                        db,
                                                        uid,
                                                        password,
                                                        "res.partner",
                                                        "write",
                                                        [[member_id], {"category_id": [5]}],
                                                    )
                                                    models.execute_kw(
                                                        db,
                                                        uid,
                                                        password,
                                                        "res.partner",
                                                        "write",
                                                        [
                                                            [member_id],
                                                            {"customer_level": "Member"},
                                                        ],
                                                    )
                                                    print("")
                                                    print(
                                                        f"{customer_results[0]['name']} has been removed from Subscriber Program !"
                                                    )
                                                    print("")
                                                    models.execute_kw(
                                                        db,
                                                        uid,
                                                        password,
                                                        "mail.message",
                                                        "create",
                                                        [
                                                            {
                                                                "body": "Subscriber Removed By IT Team.",
                                                                "model": "res.partner",
                                                                "message_type": "comment",
                                                                "res_id": member_id,
                                                                "author_id": 3,
                                                            }
                                                        ],
                                                    )
                                                    clear_output(2.5)

                                                else:
                                                    print()
                                                    print(
                                                        f"{customer_results[0]['name']} is not associated in Subscriber Program !"
                                                    )
                                                    clear_output(2.5)
                                                    print()

                                            else:
                                                print()
                                                print("Operation Cancelled")
                                                clear_output(2)
                                        else:
                                            print("Customer Not Found")
                                            clear_output(2)
                                    except (ValueError, OverflowError,KeyboardInterrupt):
                                        print("Wrong Member ID,please try again?")
                                        clear_output(2)
                                        break

                            elif choice_tool == 2:
                                clear_output(1)
                                f = Figlet(font="small")
                                print(f.renderText("Subscriber Export & Count"))
                                ids = rule_partners_domain()
                                temp = re.findall(r"\d+", ids)
                                res = list(map(int, temp))
                                ids_result = [res[index] for index in range(0, len(res))]
                                order = []
                                for i in range(len(res)):
                                    order.append(i + 1)
                                with open("output.csv", "w", newline="") as file:
                                    writer = csv.writer(file)
                                    writer.writerow(["Member_ID", "ID"])
                                    writer.writerows(zip(order, ids_result))

                                print()

                                # Setting initial value of the counter to zero
                                rowcount = 0
                                # iterating through the whole file
                                for row in open("output.csv"):
                                    rowcount += 1
                                # printing the result
                                print("Total Subscriber Count: ", rowcount - 1)
                                print()
                                print(
                                    '"output.csv" is generated at your file directory for your reference! '
                                )
                                clear_output(5)

                        except (ValueError, OverflowError):
                            print()
                            print("Please make choice between 1 , 2 or 3 or 4")
                            clear_output(2)
                            break
                else:
                    print()
                    print("You are not authorized to use Admin Tools")
                    clear_output(2.5)

            else:
                print()
                print("Please make choice between 1 , 2 or 3 or 4")
                clear_output(2.5)

        except (ValueError, OverflowError,KeyboardInterrupt):
            print()
            print("Please make choice between 1 to 3 or 4")
            clear_output(2.5)



def get_customer(member_id):
    get_customer = models.execute_kw(
        db,
        uid,
        password,
        "res.partner",
        "search_read",
        [[["id", "=", member_id]]],
        {
            "fields": [
                "name",
                "category_id",
                "customer_level",
                "phone",
                "mobile",
                "loyalty_points",
            ]
        },
    )
    return get_customer


def customer_print(customer_results):
    results = rule_partners_domain()
    if len(customer_results) == 1:
        customer_name = customer_results[0]["name"]
        print("Customer Information")
        print("####################")
        print("Name: ", customer_name)
        print("Phone: ", customer_results[0]["phone"] or "None")
        print("Mobile: ", customer_results[0]["mobile"] or "None")
        tags = customer_results[0]["category_id"]
        if tags == [1]:
            tags = "Subscriber"
        else:
            tags = "Member"
        print("Tags: ", tags)
        print("Membership: ", customer_results[0]["customer_level"])
        print("Member ID: ", customer_results[0]["id"])
        if f'["id","=",{member_id}]' in results:
            associated = "Yes"
        else:
            associated = "No"
        print("Associated: ", associated)
        print("Loyalty Points: ", customer_results[0]["loyalty_points"])
        print()
    else:
        clear_output(1.5)


def clear_output(n):
    time.sleep(n)
    os.system("cls" if os.name == "nt" else "printf '\033c'")


def rule_partners_domain():
    global lists
    global results
    lists = models.execute_kw(
        db,
        uid,
        password,
        "coupon.program",
        "search_read",
        [[["id", "=", 16]]],
        {"fields": ["rule_partners_domain"]},
    )

    results = lists[0]["rule_partners_domain"]
    return results


if __name__ == "__main__":
    main()
