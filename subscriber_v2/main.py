from kivymd.app import MDApp
from kivymd.uix.screen import Screen
import ssl
from kivy.properties import StringProperty
import xmlrpc.client

# making ssl connection secure at mobile app by adding context
context = ssl.SSLContext()
url = ''
db = ''
username = ''
password = ''
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url),context=context)
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url),context=context)

class DemoApp(MDApp):
    pass
    title = "Subscriber Program"

class Screen1(Screen):
    member_id = StringProperty("Subscriber Program")
    def textInput(self, widget):
        try:
            if "delete".lower() in widget.text.lower() and " " not in widget.text:
                id = widget.text.lower().replace("delete","")
                id = int(id)
                lists = models.execute_kw(db, uid, password, 'coupon.program', 'search_read', [[['id', '=', 19]]],
                                          {'fields': ['rule_partners_domain']})
                results = lists[0]['rule_partners_domain']
                get_customer = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['id', '=', id]]],
                                                 {'fields': ['name', 'category_id']})
                if len(get_customer) == 1 and ('["|","|","|"' in results and "]]" in results) and str(id) in results:
                    delete = results.replace('["|",', '[')
                    delete = delete.replace(f',["id","=",{id}]', '')
                    models.execute_kw(db, uid, password, 'coupon.program', 'write',
                                      [[19], {'rule_partners_domain': f'{delete}'}])
                    models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'category_id': [3]}])
                    models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'customer_level': 'Member'}])
                    models.execute_kw(db, uid, password, 'mail.message', 'create', [{
                    'body': 'Subscriber Removed By IT Department!',
                    'model': 'res.partner',
                    'message_type': 'comment',
                    'res_id': id,
                    'author_id': 3

                }])
                    widget.text = ""
                    self.member_id = f"{get_customer[0]['name']} has been removed from Subscriber Program !"
                else:
                    widget.text = ""
                    self.member_id = "Customer not found, failed to delete!"
            elif "check".lower() in widget.text.lower() and " " not in widget.text:
                lists = models.execute_kw(db, uid, password, 'coupon.program', 'search_read', [[['id', '=', 19]]],
                                          {'fields': ['rule_partners_domain']})
                results = lists[0]['rule_partners_domain']
                id = widget.text.lower().replace("check", "")
                id = int(id)
                get_customer = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['id', '=', id]]],
                                                 {'fields': ['name', 'category_id', 'customer_level', 'phone',
                                                             'mobile']})
                if len(get_customer) == 1:
                    tags = get_customer[0]['category_id']
                    if tags == [1]:
                        tags = "Subscriber"
                    else:
                        tags = "Member"
                    widget.text = ""
                    associated = ""
                    if str(id) in results:
                        associated = "Yes"
                    else:
                        associated = "No"

                    self.member_id = f"Name: {get_customer[0]['name']}\n Phone: {get_customer[0]['phone'] or 'None'} \n Mobile: {get_customer[0]['mobile'] or 'None'} \n Tag: {tags} \n Membership: {get_customer[0]['customer_level']} \n Associated: {associated}"
                else:

                    widget.text = ""
                    self.member_id = "Customer Not Found"
            elif widget.text.lower().strip() == "count":
                widget.text = ""
                subscriber_program_list = models.execute_kw(db, uid, password, 'coupon.program', 'search_read',
                                                            [[['id', '=', 19]]], {'fields': ['rule_partners_domain']})
                count = 1
                subscriber_list = subscriber_program_list[0]['rule_partners_domain']
                for i in subscriber_list:
                    if "|" in i:
                        count += 1

                    else:
                        count += 0



                self.member_id = f"Total Subscriber Count: {count}"

            elif widget.text.lower().strip() == "help":
                widget.text = ""
                self.member_id = "\n Usage \n ===== \n 1. {id} will add customer to Subscriber. \n 2. {id}delete will delete customer from Subscriber Program. \n 3. {id}search will search customer information. \n 4. 'count' will show current subscriber count. \n 5. 'help' will show usage of the app."

            else:
                id = int(widget.text)
                get_customer = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['id', '=', id]]], {'fields': ['name','id']})
                subscriber_program_list = models.execute_kw(db, uid, password, 'coupon.program', 'search_read', [[['id', '=', 19]]], {'fields': ['rule_partners_domain']})
                results = subscriber_program_list[0]['rule_partners_domain']
                if len(get_customer) == 1:
                    if ("|" in results and "]]" in results) and str(id) not in results:
                        new = results.replace('["|",', '["|","|",')
                        new = new.replace(']]', f'],["id","=",{id}]]')
                        models.execute_kw(db, uid, password, 'coupon.program', 'write',[[19], {'rule_partners_domain': f'{new}'}])
                        models.execute_kw(db, uid, password, 'res.partner', 'write',[[id], {'customer_level': 'Subscriber'}])
                        models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'category_id': [1]}])
                        models.execute_kw(db, uid, password, 'mail.message', 'create', [{
                            'body': 'Subscriber Added by IT Department!',
                            'model': 'res.partner',
                            'message_type': 'comment',
                            'res_id': id,
                            'author_id': 3}])
                        widget.text = ""
                        self.member_id = f"{get_customer[0]['name']} has been added to Subscriber List Successfully!"
                    else:
                        widget.text = ""
                        self.member_id = f"{get_customer[0]['name']} is already Subscriber !"
                else:
                    widget.text = ""
                    self.member_id = "Member Not found!"
            #catching ValueError bacause superscript integer crash the app
        except (ValueError, OverflowError):
            widget.text = ""
            self.member_id = "Wrong Member ID,please re-type! "

    def onClick(self):
        self.textInput(self.ids.text_field)
        print(self.member_id)


if __name__ ==  "__main__":
    DemoApp().run()
