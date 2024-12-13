import numpy, input_check

class PrintMixin:
    def print_info(self):
        print("Строки: ", self.n)
        print("Столбцы: ", self.m)
    def __str__(self):
        return f"Размерность: ({self.n}, {self.m})"
    
class Array:
    def __init__(self, n, m):
        self.n = n
        self.m = m

class Matrix(PrintMixin, Array):
    def __init__(self, n, m):
        super().__init__(n,m)

    @staticmethod
    def cells(n, m):
        return n*m


def task5():
    print("Для создания матрицы введите")
    print("Количество строк n: ")
    n = input_check.input_positive_int(input_check.input_int)
    print("Количество столбцов m: ")
    m = input_check.input_positive_int(input_check.input_int)

    A = numpy.random.randint(-15, 20, size=(n, m)) #array
    print("Введенная матрица A:")
    print(A)

    B = numpy.mat(numpy.random.randint(-15, 20, size=(n, m))) #matrix
    print("\nМатрица B:")
    print(B)

    C = numpy.arange(0, 10, 2)
    print("\nМассив C:") 
    print(C)

    print("\nВывод 2,3,4 элемента: ",C[1:4])
    print("\nВывод 1, 2 строки и 2+ столбцов:\n", B[:2, 1:])
    print(f"\nВывод B[0,0]: {B[0,0]} и С[n]: {C[len(C)-1]}, где n - кол-во эл. в массиве")

    print("\nМатрица В в квадрате:\n", numpy.square(B))
    print("\nМассив синусов из исходного C: \n", numpy.sin(C))

    print("\nОбъеденинение A и B:")
    print(numpy.concatenate((numpy.mat(A), B), axis = 0))

    print("\nСреднее значение м-цы A: ", numpy.mean(A))
    print("Медиана массива C: ", numpy.median(C))
    print("Кореляционная м-ца из м-цы B:\n", numpy.corrcoef(B))
    print("Дисперсия массива С: ", numpy.var(C))
    print("СКО массива С: ", numpy.std(C))

    print("\nМатрица A: \n", A)
    insert_after_max(A)
    find_median(A)

    matr = Matrix(5,6)
    matr.print_info()
    print(matr)

def insert_after_max(matrix):
    min_index = numpy.argmin(matrix)
    min_row, min_col = numpy.unravel_index(min_index, matrix.shape)
    print("Минимальный элемент: ", matrix[min_row, min_col])
    matrix = numpy.insert(matrix, min_row+1, matrix[0], axis = 0)
    print("\nМатрица после вставки:\n", matrix)

def find_median(matrix):
    print("Медиана 1-й строки матрицы А (встроенная ф.): ", numpy.median(matrix[0]))

    sorted_row = numpy.sort(matrix[0])
    mid = len(sorted_row) // 2

    if mid % 2 == 0:
        median = (sorted_row[mid - 1] + sorted_row[mid]) / 2
    else: median = sorted_row[mid]

    print("Медиана 1-й строки (программирование формулы): ", median)


