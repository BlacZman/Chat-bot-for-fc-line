from cook import Cook
import os

def get_menu():
    print("***********************************************")
    print("* My Test function                            *")
    print("***********************************************")
    print("* 1. Add                                      *")
    print("* 2. Edit                                     *")
    print("* 3. Delete                                   *")
    print("* 4. Show                                     *")
    print("* 0. exit                                     *")
    print("***********************************************")
    select = get_int(0,4)
    return select


def get_int(min, max):
	x = int(input("Enter the numbers "))
	while x < min or x > max:
		x = int(input("Enter the numbers between {} and {} ".format(min, max)))
	return x

menu = get_menu()
while menu != 0:
    if menu == 1:
        os.system("cls")
        ck = Cook()
        check = ck.writeCus(0,1)
        os.system("pause")
    elif menu == 2:
        os.system("cls")
        ck = Cook()
        check = ck.writeCus(1,1)
        os.system("pause")
    elif menu == 3:
        os.system("cls")
        ck = Cook()
        check = ck.writeCus(2,1)
        os.system("pause")
    elif menu == 4:
        os.system("cls")
        ck = Cook()
        ck.showInDevMode()
        os.system("pause")
    os.system("cls")
    menu = get_menu()