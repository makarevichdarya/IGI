#LAB WORK 3 -- Standard data types, collections, functions, modules.
#Makarevich Darya
#253505
#last changes: 09.04.2023

from input_check import input_int 
import task1, task2, task3, task4, task5

def main():
    '''Вызов меню'''
    print("Выберите задание: ")
    print("1. Рассчитать значение функции arcsin с помощью ряда. Точность вычислений задается. Сравнить самописную и встроенную функции.")
    print("2. Организовать цикл, который принимает целые числа и вычисляет количество чисел, больше 12. Окончание цикла – ввод 0")
    print("3. Определить, является ли введенная с клавиатуры строка двоичным числом")
    print("4. В тексте:\nа) определить количество заглавных строчных букв;\nб) найти первое слово, содержащее букву 'z' и его номер;\nв) вывести строку, исключив из нее слова, начинающиеся с 'a'")
    print("5. Найти произведение положительных элементов списка и сумму элементов списка, расположенных до минимального по модулю элемента")
    print()

    task = 0
    while(task < 1 or task > 6): 
        task = input_int()
        
    if task == 1: task1.task1()
    elif task == 2: task2.task2()
    elif task == 3: task3.task3()
    elif task == 4: task4.task4()
    elif task == 5: task5.task5()

if __name__ == "__main__":
    while True:
        main()
        exit = input("Хотите завершить программу?").lower() in (1, "да", "yes", "y", "д", "+")
        if exit: break
