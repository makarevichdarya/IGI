import re, zipfile
from collections import Counter

def task2():
    with open('text_for_2task.txt', 'r', encoding="utf-8") as file:
        text = file.read()
        print(text)
    
    print(f"\n Количество предложений в тексте: {count_sentences(text)}")
    print(f"Количество вопросительных предложений в тексте: {count_vopr_sent(text)}")
    print(f"Количество восклицательных предложений в тексте: {count_voskl_sent(text)}")
    print(f"Количество повествовательных предложений в тексте: {count_povest_sent(text)}\n")
    print(f"\nСреднее значение длины слова: {count_sr_word_length(text)}")
    print(f"Среднее значение длины предложения: {count_sr_sent_length(text)}")
    print(f"Количество смайликов: {count_smileys(text)}")
    print(f"Найти бинарные числа: {get_binary_nums(text)}")
    print(f"\nНайти числа, где 1-я буква гласная, 2-я согласная:\n{get_words_ab(text)}")
    print(f"\nКоличество слов нач. или заканч. на гласную: {count_words_aa(text)}")
    print(f"\nПосчитать количество вхождений всех символов:\n{count_all_symbols(text)}")
    print(f"\nНайти слова после \",\" по алфавиту:\n{sort_words(text)}")

    with open('result_2task.txt', 'w', encoding="utf-8") as file:
        file.write(f"Количество предложений в тексте: {count_sentences(text)}\n" 
                   + f"Количество вопросительных предложений в тексте: {count_vopr_sent(text)}\n"
                   + f"Количество восклицательных предложений в тексте: {count_voskl_sent(text)}\n"
                   + f"Количество повествовательных предложений в тексте: {count_povest_sent(text)}\n"
                   + f"Среднее значение длины слова: {count_sr_word_length(text)}\n"
                   + f"Среднее значение длины предложения: {count_sr_sent_length(text)}\n"
                   + f"Количество смайликов: {count_smileys(text)}\n"
                   + f"Найти бинарные числа: {get_binary_nums(text)}\n"
                   + f"Найти числа, где 1-я буква гласная, 2-я согласная:\n{get_words_ab(text)}\n"
                   + f"Количество слов нач. или заканч. на гласную: {count_words_aa(text)}\n"
                   + f"Посчитать количество вхождений всех символов:\n{count_all_symbols(text)}\n"
                   + f"Найти слова после \",\" по алфавиту:\n{sort_words(text)}\n")
    
    with zipfile.ZipFile('result_2task.zip', 'w') as archive:
        archive.write('result_2task.txt')
        info = zipfile.ZipInfo('result_2task.txt')
    print(f"Информация о файле: {info}")

        

def count_sentences(text):
    pattern = r'[.!?]\s+'
    sentences = re.findall(pattern, text)
    return len(sentences)

def count_vopr_sent(text):
    pattern = r'\?\s+'
    sentences = re.findall(pattern, text)
    return len(sentences)

def count_voskl_sent(text):
    pattern = r'!\s+'
    sentences = re.findall(pattern, text)
    return len(sentences)

def count_povest_sent(text):
    pattern = r'\.\s+'
    sentences = re.findall(pattern, text)
    return len(sentences)

def count_sr_sent_length(text):
    sentences = re.split(r'[.!?]\s+', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    lengths = 0
    count = 0
    for sent in sentences:
        words = re.findall(r'\b\w+\b', sent)
        length = 0
        for word in words:
            length += len(word)
        lengths += length
        count += 1
    
    return int(lengths / count)

def count_sr_word_length(text):
    sentences = re.split(r'[.!?]\s+', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    length = 0
    count = 0
    for sent in sentences:
        words = re.findall(r'\b\w+\b', sent)
        for word in words:
            length += len(word)
            count += 1
    
    return int(length / count)

def count_smileys(text):
    pattern = r'[;:]-*[\(\[\]\)]+'
    smileys = re.findall(pattern, text)
    
    return len(smileys)

def get_binary_nums(text):
    pattern = r'\b(?:[01]+(?:[.,][01]+)?)\b'
    nums = re.findall(pattern, text)
    return nums

def get_words_ab(text):
    pattern = r'\b[ёуеыаоэяию][^ёуеыаоэяию_\W\s]\w*\b'
    words = re.findall(pattern, text, re.IGNORECASE) 
    return words

def count_words_aa(text):
    pattern = r'\b[ёуеыаоэяию]\w*\b|\b\w+[ёуеыаоэяию]\b'
    words = re.findall(pattern, text, re.IGNORECASE)
    return len(words)

def count_all_symbols(text):
    pattern = r'.'
    symbols = re.findall(pattern, text)
    symb_counts = dict(Counter(symbols))

    return symb_counts

def sort_words(text):
    pattern = r'(?<=,\s)\w+'
    words = re.findall(pattern, text)
    return sorted(words)