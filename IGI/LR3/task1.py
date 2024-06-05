import math
from input_check import input_float, input_int, input_positive_int

def task1():
    '''Выполняет задачу из условия Задания 1.'''
    print("Введите значение аргумента x (|x| < 1): ")
    while True: 
        x = input_float()
        if abs(x) <  1: break
        else: print("Ошибка: |x| < 1")

    print("Введите точность вычислений eps: ")
    eps = input_positive_int(input_int)
        
    my_f = my_asin(x, eps)
    math_f = math.asin(x)
    print("Результат работы ручной функции:     ", my_f)
    print("Результат работы встроенной функции: ", math_f)


def my_asin(x, eps, max_iter = 500):
    '''Рассчитывает asin(x) с заданными точностью и аргументом'''
    asin = 0.0
    n = 0

    if eps > max_iter:
        print("Программа может выполнять не более 500 итераций. Ответ будет рассчитан по точности eps = 500")

    while n <= max_iter:
        if n == eps:
            break
        asin += (math.factorial(2*n) / ((4**n) * (math.factorial(n)**2) * (2*n + 1))) * (x**(2*n + 1))
        n += 1
    return asin