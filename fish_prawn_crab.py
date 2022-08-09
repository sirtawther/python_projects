from random import choices
cash = 0
while True:
    try:
        print("Welcome to PTT Gaming Python Version")
        print("===================================")
        cash = int(input("Please type Cash in amount: "))
    except ValueError:
        pass
    else:
        break
while True:
    try:
        amount = int(input("What many times you like to bet? "))
    except ValueError:
        pass
    else:
        if amount > 0:
            print("Total Bet Amount: ", amount * 500)
            cash = cash - amount*500
        else:
            print("Good Job, you typed negative amount")
            break
        if cash < 0:
            print("Please Cash in again")
            break
        print("Your Balance: ", cash)
        win = 0
        result = choices(['a','b','c','d','e','f'],k=3)
        for i in range(amount):
            try:
                bet = input("Guess your bet: ")
            except ValueError:
                break
            else:   
                if "," in bet:
                    bet1,bet2 = bet.split(",")
                    if ([bet1,bet2] == result[:2] or [bet1,bet2] == result[1:3] or [bet1,bet2] == [result[0],result[-1]]) and (bet1==bet2) :
                        win += 5000
                        cash += 5000
                    if ([bet1,bet2] == result[:2] or [bet1,bet2] == result[1:3] or [bet1,bet2] == [result[0],result[-1]]) and (bet1 != bet2):
                        win += 3000
                        cash += 3000
                else:
                    print("use comma, restarting your bets")
        print("Result is",result)
        if win == 0:
            print(":(")
            print("Your Balance:", cash)
        elif win >= 8000:
            print("Wow,2 slot JackPOT!!!")
            print("Your Balance:", cash)
        elif win >= 5000:
            print("Wow, Win 10x !! ")
            print("Your Balance:", cash)
        else:
            print("You win 1 slot")
            print("Your Balance:", cash)