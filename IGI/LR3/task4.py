def task4():
    '''Выполняет задачу из условия Задания 4.'''
    text = "So she was zad considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    print("Исходный текст:\n", text)

    point_a(text)
    point_b(text)
    point_c(text)

def point_a(text):
    '''Определяет количество заглавных и строчных букв в тексте из Задания 4.'''
    count_big = 0
    count_small = 0

    for i in text:
        if i >= 'A' and i <= 'Z':
            count_big += 1
        elif i >= 'a' and i <= 'z':
            count_small += 1
    
    print("Количество заглавных букв: ", count_big)
    print("Количество строчных букв: ", count_small)
    print()

def point_b(text):
    '''Находит в тексте из Задания 4 первое слово, содержащее букву 'z', и его номер'''
    words = text.replace(',', '').replace('.', '').split(' ')

    k = 0
    check = False
    for i in words:
        k += 1
        try:
            pos = i.index('z')
            print("Найденное слово: ", i)
            print("Его номер: ", k)
            check = True
            break
        except ValueError:
            continue

    if check == False: print("Слово не найдено")
    print()
        
def point_c(text):
    '''В тексте из Задания 4 удаляет все слова, начинающиеся на 'a' '''
    words = text.split(' ')

    result = [word for word in words if not word.startswith('a')]
    print(' '.join(result))

      