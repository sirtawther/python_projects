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
            id = int(widget.text)
            get_customer = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['id', '=', id]]], {'fields': ['name','id']})
            subscriber_program_list = models.execute_kw(db, uid, password, 'coupon.program', 'search_read', [[['id', '=', 11]]], {'fields': ['rule_partners_domain']})
            results = subscriber_program_list[0]['rule_partners_domain']
            if len(get_customer) == 1:
                if ("|" in results and "]]" in results) and str(id) not in results:
                    new = results.replace('["|",', '["|","|",')
                    new = new.replace(']]', f'],["id","=",{id}]]')
                    models.execute_kw(db, uid, password, 'coupon.program', 'write',[[11], {'rule_partners_domain': f'{new}'}])
                    models.execute_kw(db, uid, password, 'res.partner', 'write',[[id], {'customer_level': 'Subscriber'}])
                    models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'category_id': [1]}])
                    widget.text = ""
                    self.member_id = f"{get_customer[0]['name']} has been added to Subscriber List Successfully!"
                else:
                    widget.text = ""
                    self.member_id = f"{get_customer[0]['name']} is already Subscriber !"
            else:
                widget.text = ""
                self.member_id = "Member Not found!"
        #catching ValueError bacause superscript integer crash the app
        except (ValueError,OverflowError):
            widget.text = ""
            self.member_id = "Please type Correct Member ID"

    def onClick(self):
        self.textInput(self.ids.text_field)
        print(self.member_id)


if __name__ ==  "__main__":
    DemoApp().run()
