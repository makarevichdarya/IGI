import math, statistics, matplotlib.pyplot as plot
from input_check import input_float, input_int, input_positive_int

def task3():
    print("Введите значение аргумента x (|x| < 1): ")
    while True: 
        x = input_float()
        if abs(x) <  1: break
        else: print("Ошибка: |x| < 1")

    print("Введите точность вычислений eps: ")
    eps = input_positive_int(input_int)
 
    my_f, elems = my_asin(x, eps)
    math_f = math.asin(x)
    print("Результат работы ручной функции:     ", my_f)
    print("Результат работы встроенной функции: ", math_f)
    print("Среднее арифм. элементов: ", statistics.mean(elems))
    print("Медиана элементов: ", statistics.median(elems))
    print("Мода элементов: ", statistics.mode(elems))
    print("Дисперсия элементов: ", statistics.variance(elems))
    print("СКО элементов: ", statistics.stdev(elems))
    my_asin_plot(eps)


def my_asin(x, eps, max_iter = 500):
    asin = 0.0
    n = 0
    elems = list()
    if eps > max_iter:
        print("Программа может выполнять не более 500 итераций. Ответ будет рассчитан по точности eps = 500")

    while n <= max_iter:
        if n == eps:
            break
        temp = (math.factorial(2*n) / ((4**n) * (math.factorial(n)**2) * (2*n + 1))) * (x**(2*n + 1))
        elems.append(temp)
        asin += temp
        n += 1
    return asin, elems

def my_asin_plot(n): 
    func = list()
    args = list()
    func_math = list()
    print("--------------------------------")
    print("-x-------n-----F(x)-----MF(x)---")

    for i in range(-10, 11, 1):
        if i / 10 == 1 or i / 10 == -1:
            continue
        y, _ = my_asin(i / 10, n)
        func.append(y)
        y_math = math.asin(i / 10)
        func_math.append(y_math)
        args.append(i / 10)
        print(f"{(i / 10):<6}  {n}  {y:<8.4f}   {y_math:<8.4f}")

    print("--------------------------------")

    plot.axhline(0, color='black',linewidth=0.5)
    plot.axvline(0, color='black',linewidth=0.5)
    plot.xlim(-1, 1)
    plot.ylim(-math.pi/2, math.pi/2)
    plot.plot(args, func, color = 'red')
    plot.plot(args, func_math, color = 'blue')
    plot.title("График функции ASIN")
    plot.ylabel("Ось Y")
    plot.xlabel("Ось X")
    plot.legend(loc = 'lower center', title = 'Красный - пользовательская ф.\n Синий - встроенная ф.')
    plot.annotate('Точка (0, 0)',
             xy=(0, 0), xycoords='data',
             xytext=(-20, 20), textcoords='offset points',
             arrowprops=dict(facecolor='black', arrowstyle="->"))
    
    plot.savefig('graph.png', dpi=300)
    plot.show()

