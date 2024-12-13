def input_int():
    '''Корректный ввод целого числа'''
    while True:
        try:
            int_num = int(input())
            return int_num
        except ValueError:
            print("Ошибка ввода: введите целое число!")
            continue


def input_float():
    '''Корректный ввод вещественного числа'''
    while True:
        try:
            float_num = float(input())
            return float_num
        except ValueError:
            print("Ошибка ввода: введите вещественное число!")
            continue
    
def input_positive_int(input_int):
    '''Декоратор к функции input_int(). Корректный ввод целого положительного числа'''
    while True:
        num = input_int()
        if num > 0: return num
        else: print("Ошибка: введите положительное число!")