import xmlrpc.client
import sys
import os
import time


url = ''
db = ''
username = ''
password = ''


# id = models.execute_kw(db, uid, password, 'coupon.program', 'create', [{'rule_products_domain': ["id","=",2]}])
while True:
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        lists = models.execute_kw(db, uid, password, 'coupon.program', 'search_read', [[['id', '=', 19]]], {'fields': ['rule_partners_domain']})
        results = lists[0]['rule_partners_domain']
        print("================")
        print("Add Subscriber")
        print("================")
        id = int(input("Enter Customer ID: ").strip())
        print()


        if id == 7777777:
            print("=====================")
            print("Delete Subscriber")
            print("=====================")
            id = int(input("Delete ID: ").strip())
            get_customer = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['id', '=', id]]],{'fields': ['name', 'category_id']})
            if len(get_customer) == 1 and ('["|","|","|"' in results and "]]" in results) and str(id) in results:
                delete = results.replace('["|",', '[')
                delete = delete.replace(f',["id","=",{id}]', '')
                models.execute_kw(db, uid, password, 'coupon.program', 'write',
                                  [[19], {'rule_partners_domain': f'{delete}'}])
                models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'category_id': [3]}])
                models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'customer_level': 'Member'}])
                print("=======================================================================")
                print(f"{get_customer[0]['name']} has been removed from Subscriber Program !")
                print("=======================================================================")
                models.execute_kw(db, uid, password, 'mail.message', 'create', [{
                    'body': 'Subscriber Removed By Customer Service.',
                    'model': 'res.partner',
                    'message_type': 'comment',
                    'res_id': id,
                    'author_id': 6753

                }])
                time.sleep(1.5)
                os.system('cls' if os.name == 'nt' else "printf '\033c'")


            else:
                time.sleep(1.5)
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Customer Not Found! Failed to Delete!")
                print()


        else:
            get_customer = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['id', '=', id]]],
                                             {'fields': ['name', 'category_id','customer_level','phone','mobile']})
            if len(get_customer) == 1:
                customer_name = get_customer[0]['name']
                print("Customer Information")
                print("####################")
                print("Name: ",customer_name)
                print("Phone: ", get_customer[0]['phone'] or "None")
                print("Mobile: ", get_customer[0]['mobile'] or "None")
                tags = get_customer[0]['category_id']
                if tags == [1]:
                    tags = "Subscriber Tag"
                else:
                    tags= "Member Tag"
                print("Tags: ", tags)
                print("Membership: ", get_customer[0]['customer_level'])
                print("Member ID: ", get_customer[0]['id'])
                associated = ""
                if str(id) in results:
                    associated = "Yes"
                else:
                    associated = "No"
                print("Associated: ", associated)
                print()

                if input(f"Add {customer_name} to Subscriber Program? (Y/N): ").lower() == "y":

                    models.execute_kw(db, uid, password, 'res.partner', 'write',
                                      [[id], {'customer_level': 'Subscriber'}])
                    models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'category_id': [1]}])

                    print()

                    if ("|" in results and "]]" in results) and str(id) not in results:
                        new = results.replace('["|",' , '["|","|",')
                        new = new.replace(']]' , f'],["id","=",{id}]]')

                        models.execute_kw(db, uid, password, 'coupon.program', 'write', [[19], {'rule_partners_domain': f'{new}'}])
                        print(f"{get_customer[0]['name']} has been added to Subscriber List Successfully !")
                        models.execute_kw(db, uid, password, 'mail.message', 'create', [{
                            'body': 'Subscriber Added by Customer Service.',
                            'model': 'res.partner',
                            'message_type': 'comment',
                            'res_id': id,
                            'author_id': 6753

                        }])
                        print()
                        time.sleep(1.5)
                        os.system('cls' if os.name == 'nt' else "printf '\033c'")

                    else:
                        print(f"{get_customer[0]['name']} is already Subscriber !")
                        print("Restarting Program.. ")
                        print()
                        time.sleep(1.5)
                        os.system('cls' if os.name == 'nt' else "printf '\033c'")
                else:
                    print("")
                    time.sleep(1.5)
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
            else:
                print("Customer Not Found! Wrong ID? ")
                print()
            
    except (EOFError,ValueError,OverflowError):
        print("Please Input Valid Customer ID!")
        print()
    except (KeyboardInterrupt,TypeError):
        sys.exit("Bye")
        
 



    
    