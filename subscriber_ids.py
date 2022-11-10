import xmlrpc.client
import sys
import os
import time
import re
import csv


url = ''
db = ''
username = ''
password = ''
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
results = models.execute_kw(db, uid, password, 'coupon.program', 'search_read', [[['id', '=', 19]]], {'fields': ['rule_partners_domain']})
try:
    ids = results[0]['rule_partners_domain']
    temp = re.findall(r'\d+', ids)
    res = list(map(int, temp))
    ids_result = [res[index] for index in range(0, len(res))]
    order = []
    for i in range(len(res)):
        order.append(i+1)
    with open("test.csv","w",newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Member_ID","ID"])
        writer.writerows(zip(order,ids_result))



except (EOFError,ValueError,OverflowError):
    print("Please Input Valid Customer ID!")
    time.sleep(1.5)
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    print()







