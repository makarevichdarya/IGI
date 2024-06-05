import random, input_check, numpy

def task5():
    '''Выполняет задачу из условия Задания 5.'''
    nums = init_list()
    format_nums = [f'{num:.3f}' for num in nums]
    print(' '.join(format_nums))

    prod = find_prod(nums)
    if prod == 0: print("Положительные элементы отсутствуют")
    else: print(f"Произведение положительных элементов списка: {prod:.3f}")

    sum = find_sum(nums)
    print(f"Сумма элементов расположенных, до минимального: {sum:.3f}")

def init_list():
    '''Инициализация списка двумя способами: случайным образом и вручную'''
    nums = list()

    while True:
        print("Как вы хотите инициализировать список?\n 1 - Случайным образом\n 2 - Вручную")
        choice = input_check.input_int()
        if choice == 1 or choice == 2: break 
        else: print("Ошибка: введите 1 или 2")

    print("Введите количество элементов списка: ")
    length = input_check.input_positive_int(input_check.input_int)


    if choice == 1:
        nums.extend(generator(length))
    elif choice == 2:
        print("Вводите список: ")
        for i in range(length): nums.append(input_check.input_float())

    return nums

def generator(length):
    '''Заполнение генератора случайными числами'''
    for i in range(length):
        yield random.uniform(-i*2, 20)

def find_prod(nums):
    '''Находит произведение положительных элементов списка'''
    prod = 1
    flg = False
    for i in nums:
        if i > 0: 
            prod *= i
            flg = True
    if flg == True: return prod 
    else: prod = 0 

def find_sum(nums):
    '''Находит сумму элементов, стоящих перед минимальнвм по модулю элементом'''
    sum = 0
    min = abs(nums[0])
    flg = True

    for i in nums:
        if abs(i) < min: 
            min = abs(i)
            if i < 0: flg = False

    if flg == False: min *= -1
    print(f"Минимальный по модулю элемент: {min:.3f}")

    for i in range(nums.index(min)): sum += nums[i]

    return sum
