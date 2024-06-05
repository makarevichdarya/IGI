import input_check, csv, pickle

class Country():
    def __init__(self, name, cities):
        self.name = name
        self.cities = cities

class Cities_Dict():
    def __init__(self):
        self.country_cities = {}
        
    def add_country(self, country):
        self.country_cities[country.name] = country.cities

    def add_city(self, city_name, country_name):
       for country, cities in self.country_cities.items():
            if country_name == country:
                cities.append(city_name)

    def find_country_by_city(self, city_name):
        for country, cities in self.country_cities.items():
            if city_name in cities:
                return country
        
    
    def sort_countries_by_name(self):
        self.country_cities = dict(sorted(self.country_cities.items(), key=lambda x: x[0]))
    
    def print(self):
        for country, city in self.country_cities.items():
            print(f"{country}: {city}")

def task1():

    country_cities = Cities_Dict()

    russia = Country("Россия", ["Москва", "Санкт-Петербург", "Волгоград", "Красноярск"])
    belarus = Country("Беларусь", ["Минск", "Витебск", "Гродно", "Могилев"])
    usa = Country("США", ["Нью-Йорк", "Вашингтон", "Лос-Анджелес"])
    china = Country("Китай", ["Пекин", "Шанхай", "Гуанчжоу"])

    country_cities.add_country(russia)
    country_cities.add_country(usa)
    country_cities.add_country(china)
    country_cities.add_country(belarus)

    while True:
        print("Выберите действие: 1 - Найти, в какой стране расположен город\n 2 - Отсортировать страны по алфавиту\n 3 - Вывести все страны и их города\n 4 - Добавить город\n 5 - Сохранить в CSV\n 6 - Сохранить в pickle\n 7 - Считать c CSV\n 8 - Считать с Pickle\n 9 - Добавить свои данные")
        choice = input_check.input_positive_int(input_check.input_int)

        if choice == 1: 
            city = input("Введите город: ")
            country = country_cities.find_country_by_city(city)
            print(f"Страна: {country}")
        elif choice == 2:
            country_cities.sort_countries_by_name()
            country_cities.print()
        elif choice == 3:
            country_cities.print()
        elif choice == 4:
            city = input("Введите город: ")
            country = country_cities.find_country_by_city(city)
            if country == None: 
                country = input("Введите страну: ")
                country_cities.add_city(city, country)
            else: print("Город уже добавлен")
        elif choice == 5:
            save_to_scv(country_cities)
        elif choice == 6:
            save_to_pickle(country_cities)
        elif choice == 7:
            read_from_csv(country_cities)
        elif choice == 8:
            read_from_pickle(country_cities)
        elif choice == 9:
            add_data(country_cities)

def add_data(dict):
    data = Country('',[])
    data.name = input("Введите страну: ")
    print("Вводите города (0 - окончание ввода)")
    while True:
        city = input()
        if city != '0': data.cities.append(city)
        else: break

    if data.name.capitalize() not in dict.country_cities.keys():
        dict.add_country(data)
    else: print("Страна уже существует")

def save_to_scv(dict):
    csv_file_path = "saved.csv"
    with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for country, cities in dict.country_cities.items():
            writer.writerow([country, ", ".join(cities)])

def save_to_pickle(dict):
    pickle_file_path = "saved.pickle"
    with open(pickle_file_path, "wb") as file:
        pickle.dump(dict.country_cities, file)

def read_from_csv(dict):
    csv_file_path = "saved.csv"
    data = Country('', [])
    data_lst = list()

    with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            country_name = row[0]
            cities_name = row[1].split(", ")
            data.name = country_name
            data.cities = cities_name 
            data_lst.append(data)

    for data in data_lst:
        if data.name.capitalize() not in dict.country_cities.keys():
            dict.add_country(data)
        else: continue

def read_from_pickle(dict):
    pickle_file_path = "saved.pickle"
    data = Country('', [])
    data_lst = list()
    with open(pickle_file_path, "rb") as file:
        data = pickle.load(file)
        data_lst = [Country(country_name, cities) for country_name, cities in data]
    
    for data in data_lst:
        if data.name.capitalize() not in dict.country_cities.keys():
            dict.add_country(data)
        else: continue





    

    
    
    
    