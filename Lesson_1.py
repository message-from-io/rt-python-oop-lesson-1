
'''
1. Получите текст из файла.
2. Разбейте текст на предложения.
3. Найдите самую используемую форму слова, состоящую из 4 букв и более, на русском языке.
4. Отберите все ссылки.
5. Ссылки на страницы какого домена встречаются чаще всего?
6. Замените все ссылки на текст «Ссылка отобразится после регистрации».
'''


import re


# 1. Получите текст из файла

with open('text.txt', 'r', encoding='utf-8') as raw_file:
    raw_text = raw_file.read()


# 2. Разбейте текст на предложения

print('\n2:\n')

sentences_list = []
raw_sentences_list = re.split('(\.{1,3}|!|\?)\s', raw_text)

print('raw_sentences_list:\n', raw_sentences_list, '\n')

# Обработать список, убрав лишние пробелы и объединив каждое предложение с последующим знаком препинания, которое к нему относится
for i in range(1, len(raw_sentences_list), 2):
    item = raw_sentences_list[i - 1].strip() + raw_sentences_list[i]
    sentences_list.append(item)

# Добавить последнее предложение, если это не пустой элемент списка
item = raw_sentences_list[len(raw_sentences_list) - 1].strip()
if item:
    sentences_list.append(item)

print('sentences_list:\n', sentences_list)

# Результат:
#
# raw_sentences_list:
# [' В этой статье собраны самые интересные, популярные и полезные туристические сайты', '.', 'А дальше анализ сайта...
# ...безо всяких виз', '.', 'Путешественники оставляют не только фотоотчеты, а еще видеозаписи из поездок.']
#
# sentences_list:
# ['В этой статье собраны самые интересные, популярные и полезные туристические сайты.', 'А дальше анализ сайта...
# ...безо всяких виз.', 'Путешественники оставляют не только фотоотчеты, а еще видеозаписи из поездок.']


# 3. Найдите самую используемую форму слова, состоящую из 4 букв и более, на русском языке

print('\n3:\n')

# Получить список всех слов на русском языке
words_list = re.findall('[А-я]{4,}', raw_text)

# Преобразовать элементы списка к нижнему регистру
words_list = list(map(lambda x: x.lower(), words_list))

# Перебрать все элементы списка и создать на их основе словарь, в который будет включен сам элемент и число его появлений в тексте, например: {'новости': 3}
words_dict = {}
for item in words_list:
    count = words_list.count(item)
    words_dict[item] = count

# Отсортировать словарь и найти наиболее часто встречающийся элемент. Метод items() возвращает новое представление элементов словаря в виде списка кортежей
sorted_words_list = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)
print(sorted_words_list, '\n')

# Получить первый элемент первого кортежа отсортированного словаря
most_frequent_word = sorted_words_list[0][0]
print(most_frequent_word)

# Результат:
#
# [('новости', 3), ('можно', 3), ... ('найти', 2), ('описание', 2), ... ('помочь', 1), ('узнать', 1)]
#
# новости


# 4. Отберите все ссылки

print('\n4:\n')

# Ключевым элементом поиска является шаблон '\.[A-z]'. Шаблон '[A-z\d/]+' позволяет исключить из поиска возможные точки на концах ссылок
links_list = re.findall('[A-z\d\./]+\.[A-z][A-z\d/]+', raw_text)
print(links_list)

# Результат:
#
# ['travel.mail.ru/travel', 'Mail.ru', 'travel.mail.ru/travel2', 'votpusk.ru/main', '3totravel.ru', 'geospot.ru/about']


# 5. Ссылки на страницы какого домена встречаются чаще всего?

print('\n5:\n')

# Преобразовать элементы списка со ссылками к нижнему регистру
links_list = list(map(lambda x: x.lower(), links_list))

# Найти все домены в списке со ссылками
domains_list = []
for link in links_list:
    # Разбить ссылку на элементы
    # ['travel', '.', 'mail', '.', 'ru', '/', 'travel']
    link_parts = re.split('([\./])', link)
    # Скомпоновать из элементов ссылки только домен, начиная поиск с конце списка
    for i in range(len(link_parts) - 1, -1, -1):
        # Включить в имя домена элементы списка по обе стороны от первой встретившейся точки
        if link_parts[i] == '.':
            domains_list.append(link_parts[i - 1] + link_parts[i] + link_parts[i + 1])
            break

# Перебрать все элементы списка доменов и создать на их основе словарь, в который будет включен домен и число его появлений в тексте, например {'mail.ru': 3}
domains_dict = {}
for domain in domains_list:
    count = domains_list.count(domain)
    domains_dict[domain] = count

# Отсортировать словарь и найти наиболее часто встречающийся элемент. Метод items() возвращает новое представление элементов словаря в виде списка кортежей
sorted_domains_list = sorted(domains_dict.items(), key=lambda x: x[1], reverse=True)
print(sorted_domains_list, '\n')

# Получить первый элемент первого кортежа отсортированного словаря
most_frequent_domain = sorted_domains_list[0][0]
print(most_frequent_domain)

# Результат:
#
# [('mail.ru', 3), ('votpusk.ru', 1), ('3totravel.ru', 1), ('geospot.ru', 1)]
#
# mail.ru


# 6. Замените все ссылки на текст <Ссылка отобразится после регистрации>

print('\n6:\n')

masked_links_text = re.sub('[A-z\d\./]+\.[A-z][A-z\d/]+', '<Ссылка отобразится после регистрации>', raw_text)
print(masked_links_text)

# Результат:
#
# В этой статье собраны самые интересные, популярные и полезные туристические сайты. А дальше анализ сайта и его удобство вы оцените для себя сами.
# 1) <Ссылка отобразится после регистрации>. Проект под названием ...
