import input_check, matplotlib.pyplot as plot
from abc import ABC, abstractmethod
import math

class GeometricFigure(ABC):
    @abstractmethod
    def calculate_area(self):
        pass

class FigureColor:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

class Triangle(GeometricFigure):
    side = 0
    def __init__(self, height, base, red, green, blue):
        super().__init__
        self.height = height
        self.base = base
        self.color = FigureColor(red, green, blue)
    
    @property
    def side(self):
        return math.sqrt(self.height**2 + (self.base / 2)**2)

    @side.setter
    def side(self, value):
        self.side = value

    def calculate_area(self):
        return 0.5 * self.base * self.height
    
    def info(self):
        if self.color.blue == 255: col_name = 'синий'
        elif self.color.green == 255: col_name = 'зеленый'
        elif self.color.red == 255: col_name = 'красный'
        area = self.calculate_area()
        print("Треугольник: цвет - {0}, высота - {1}, основание - {2}, площадь - {3}".format(col_name, self.height, self.base, area))
    
    def draw(self):
        figure, ax = plot.subplots()
        triangle = plot.Polygon([[0, 0], [self.base, 0], [self.base/2, self.height]],
                           closed=True,
                           facecolor=(self.color.red/255, self.color.green/255, self.color.blue/255))
        
        ax.add_patch(triangle)
        ax.set_xlim(0, self.base)
        ax.set_ylim(0, self.height)
        plot.title("РАВНОБЕДРЕННЫЙ ТРЕУГОЛЬНИК")

        plot.savefig('triangle.png', dpi=300)
        plot.show()


def task4():
    print("Для измерений треугольника введите:")
    print("Длина основания: ")
    base_len = input_check.input_positive_int(input_check.input_int)
    print("Длина высоты: ")
    height_len = input_check.input_positive_int(input_check.input_int)
    col_type = 0
    while col_type < 1 or col_type > 3:
        print("Введите цвет: 1 - красный, 2 - зеленый, 3 - синий: ")
        col_type = input_check.input_positive_int(input_check.input_int)
    if col_type == 1: red_c, green_c, blue_c = 255, 0, 0
    elif col_type == 2: red_c, green_c, blue_c = 0, 255, 0
    elif col_type == 3: red_c, green_c, blue_c = 0, 0, 255

    triangle = Triangle(height_len, base_len, red_c, green_c, blue_c)
    triangle.info()
    print("Сторона треугольника: ", triangle.side)
    triangle.draw()


