from input_check import input_int

def task2():
    '''Выполняет задачу из условия Задания 2.'''
    count = 0
    nums = list()
    print("Вводите целые числа. Окончание - ввод 0")
    while True:
        num = input_int()
        if num == 0:
            break
        elif num > 12:
            count += 1
        nums.append(num)
    
    print("Количество чисел, больших 12: ", count)
