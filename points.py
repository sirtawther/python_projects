import os
import signal
import cowsay
import random
chars = cowsay.char_names
choice = random.choice(chars)
print(cowsay.get_output_string(choice, 'Loyalty Points Editor'))
print("1) Loyalty Points Viewer")
print("2) Loyalty Points Editor")
print("3) Exit")
while True:
    try:
        clear = 'clear'
        
        user = int(input("Your Choice(1 or 2 or 3): "))
        os.system(clear)
    except ValueError:
        pass
    else:
        
        if user == 1:

            while True:
                try:
                    print("Points Viewer")
                    print()
                    user_id = int(input("Customer ID: "))

                except ValueError:
                    pass
                else:
                    cmd = 'psql -c \'SELECT id,name,phone,loyalty_points FROM res_partner WHERE id=' +str(user_id)+ "\'"
                    os.system(cmd)
                    print("1) Loyalty Points Viewer")
                    print("2) Loyalty Points Editor")
                    print("3) Exit")
                    
                    break
            
        elif user == 2:
            while True:
                try:
                    print("Points Editor")
                    print()
                    user_id = int(input("Customer ID: "))
                except ValueError:
                    pass
                else:
                    
                    while True:
                        try:        
                            points = int(input("Loyalty Points: "))
                        except ValueError:
                            pass
                        else:
                            cmd = 'psql -c \'UPDATE res_partner set loyalty_points='+str(points)+' WHERE id='+str(user_id)+ "\'"
                            cmd1 = 'psql -c \'SELECT id,name,phone,loyalty_points FROM res_partner WHERE id=' +str(user_id)+ "\'"
                            os.system(cmd)
                            print("Points Updated Successfully!")
                            os.system(cmd1)
                            print("1) Loyalty Points Viewer")
                            print("2) Loyalty Points Editor")
                            print("3) Exit")
                            break
                    break
        elif user == 3:

            os.kill(os.getppid(), signal.SIGHUP)
            

        else:
            pass