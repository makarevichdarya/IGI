def task3():
    '''Выполняет задачу из условия Задания 3.'''
    s = str(input("Введите строку:"))
    check_sign = False
    
    if (s.count(".") + s.count(",") == 1) and s[0] != "," and  s[0] != "." and s[len(s) - 1] != "," and s[len(s) - 1] != ".":
        check_sign = True

    if check_sign == True: 
        if s.count("1") + s.count("0") + 1 == len(s): print("Число является двоичным")
    elif check_sign == False: 
        if s.count("1") + s.count("0") == len(s): print("Число является двоичным")
        else: print("Число не является двоичным")
