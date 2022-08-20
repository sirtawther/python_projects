import os
import signal
import cowsay
import random
import time

chars = cowsay.char_names
choice = random.choice(chars)
print(cowsay.get_output_string(choice, 'Loyalty Points Editor'))

while True:
    print("Points Viewer")
    try:
    
        
        while True:
            try:
                print()
                user_id = int(input("Customer ID: "))

            except ValueError:
                pass
            else:
                cmd = 'psql -c \'SELECT id,name,phone,loyalty_points FROM res_partner WHERE id=' +str(user_id)+ "\'"
                os.system(cmd)
                print("Points Editor")
                while True:
                    try:
                        print()
                    except ValueError:
                        pass
                    else:

                        try:        
                            points = int(input("Loyalty Points: "))
                            print()
                        except ValueError:
                            pass
                        else:
                            cmd = 'psql -c \'UPDATE res_partner set loyalty_points='+str(points)+' WHERE id='+str(user_id)+ "\'"
                            cmd1 = 'psql -c \'SELECT id,name,phone,loyalty_points FROM res_partner WHERE id=' +str(user_id)+ "\'"
                            clear = "clear"
                            os.system(cmd)
                            print()
                            print("Points Updated Successfully!")
                            print()
                            os.system(cmd1)
                            print("Restarting.. .in 5s")
                            time.sleep(1)
                            print("Restarting.. .in 4s")
                            time.sleep(1)
                            print("Restarting.. .in 3s")
                            time.sleep(1)
                            print("Restarting.. .in 2s")
                            time.sleep(1)
                            print("Restarting.. .in 1s")
                            time.sleep(1)
                            os.system(clear)
                            break
 
    except EOFError:
        print("Bye Bye!")
        os.kill(os.getppid(), signal.SIGHUP)
