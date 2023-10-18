dic = {'ь': '', 'ъ': '', 'а': 'a', 'б': 'b', 'в': 'v',
       'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
       'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l',
       'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
       'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
       'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ы': 'yi',
       'э': 'e', 'ю': 'yu', 'я': 'ya'}


def transliteration(x):
    t = ''
    for i in x:
        t += dic.get(i.lower(), i.lower()).upper() if i.isupper() else dic.get(i, i)
    return t

