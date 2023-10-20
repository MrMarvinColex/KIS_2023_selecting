import difflib
import os
import sys



# Достаем контент из файла
def get_content(file):
    with open(file, 'rb') as f:
        return f.read()


# Ищем, насколько файлы похожи в процентах
def files_similary(f_cont, s_cont):
    len1 = len(f_cont)
    len2 = len(s_cont)
    if len1 < len2:
        f_cont, s_cont = s_cont, f_cont
        len1, len2 = len2, len1

    # дополняем контент относительно наибольшего файла
    new_cont = s_cont + b'#' * (len1 - len2)
    # собственно подсчет сходства, эта бибилиотека работает через Хэши, а значит
    # имеет приемлемую скорость
    return difflib.SequenceMatcher(None, f_cont, new_cont).ratio() * 100


# --------------------------------------------------

# BEGIN OF MAIN :0

dir_name_1 = sys.argv[1]
dir_name_2 = sys.argv[2]
is_similar = float(sys.argv[3])

# собираем контент
dir_1 = [get_content(f'{dir_name_1}{f}') for f in os.listdir(dir_name_1)]
dir_2 = [get_content(f'{dir_name_2}{f}') for f in os.listdir(dir_name_2)]


# То, где мы будем хранить наши ответы
identicals = [list() for i in range(len(dir_1))]
similars = [list() for i in range(len(dir_1))]
is_used = [False for i in range(len(dir_2))]


# Подсчет ответов, рассматриваем все пары из DIR_1 и DIR_2
for i, file_1 in enumerate(dir_1):
    for j, file_2 in enumerate(dir_2):
        files_sim = files_similary(file_1, file_2)
        if (abs(files_sim - 100) < 0.01):
            identicals[i].append(file_2)
            is_used[j] = True
        elif (files_sim - is_similar > -0.01):
            similars[i].append(file_2)
            is_used[j] = True


# Выводим соответсвующие ответы.
print("Identical files:")
for i, d in enumerate(identicals):
    for f in d:
        print(dir_1[i], " - ", f)

print("\n\nSimilar files:")
for i, d in enumerate(similars):
    for f in d:
        print(dir_1[i], " - ", f)

print("\n\nUnique in DIR_1")
for i in range(len(dir_1)):
    if (identicals[i] == list() and similars[i] == list()):
        print(dir_1[i])

print("\n\nUnique in DIR_2")
for i in range(len(dir_2)):
    if (not is_used[i]):
        print(dir_2[i])
