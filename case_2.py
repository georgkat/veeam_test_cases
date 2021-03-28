import argparse
import hashlib
import os
import traceback
from sys import exit

parser = argparse.ArgumentParser()  # объявляю парсер
parser.add_argument('instructions', type=str, help='path to the input file')  # 1-й аргумент
parser.add_argument('destination', type=str, help='path to the directory containing the files to check')  # 2-й аргумент
args = parser.parse_args()  # извлекаю аргументы
instructions_file = args.instructions.replace('\\', '/')  # присваиваю аргументы переменным, заменяя рискованные символы
destination_path = args.destination.replace('\\', '/')


def hash_it(file_name, method):
    """
    Генерирует хэш-сумму файла методами MD5, SHA1, SHA256
    Принимает путь в виде string к файлу с инструкциями и метод в виде string
    Возвращает хэш-сумму
    """
    if method == 'md5':
        hash_md5 = hashlib.md5()  # конструирую хэш-алгоритм MD5
        with open(file_name, 'rb') as file:  # читаю нужный файл
            for part in iter(lambda: file.read(4096), b''):  # по частям создаю нужную сумму
                hash_md5.update(part)
        return hash_md5.hexdigest()  # возвращаю сумму
    elif method == 'sha1':
        hash_sha_one = hashlib.sha1()
        with open(file_name, 'rb') as file:
            for part in iter(lambda: file.read(4096), b''):
                hash_sha_one.update(part)
        return hash_sha_one.hexdigest()
    elif method == 'sha256':
        hash_sha_256 = hashlib.sha256()
        with open(file_name, 'rb') as file:
            for part in iter(lambda: file.read(4096), b''):
                hash_sha_256.update(part)
        return hash_sha_256.hexdigest()
    else:
        print('Method not specified or wrong')  # не выбран метод или в него пошли не те данные


def instruction(file_name):
    """
    Делает из файла инструкций словарь
    Принимает путь в виде string к файлу с инструкциями
    В случае неправильного формата файла останавливает программу
    Возвращает dictionary с инструкциями
    """
    instruct_dict = {}
    try:
        with open(file_name) as file:
            for row in file:
                row = row.replace('\n', '').split(' ')
                instruct_dict[row[0]] = {'method': row[1], 'hash': row[2]}
        return instruct_dict
    except Exception as ex:
        err = traceback.format_exc()
        exit(f'Critical Fail! Wrong input file format and/or {ex}')
        print(err)


def review(instruction_file_name, dest_dir):
    """
    Функция проверки хэша файлов
    Принимает string путь к файлу с инструкциями и к проверяемому каталогу
    Выводит информацию о соответствии сохраненного хэша - хэшу файла
    foo.eggs NOT FOUND
    bar.eggs OK
    spam.eggs FAIL
    """
    instruction_dict = instruction(instruction_file_name)
    for file_name in instruction_dict:
        method = instruction_dict[file_name]['method']
        hash_data = instruction_dict[file_name]['hash']
        if os.path.exists(f'{dest_dir}/{file_name}'):  # проверяю есть ли там файл
            hash_check = hash_it(file_name, method)  # генерирую хэш сумму
            if hash_check == hash_data:  # если сходится - всё ок
                instruction_dict[file_name]['checked'] = 'OK'
                print(f'{file_name} OK')
            elif hash_check != hash_data:  # если не сходится - не ок
                instruction_dict[file_name]['checked'] = 'FAIL'
                print(f'{file_name} FAIL')
        else:  # если файл
            instruction_dict[file_name]['checked'] = 'NOT FOUND'
            print(f'{file_name}  NOT FOUND')


def check_everything(inst, dest):
    """
    Проверяет коррекность введённых данных
    Принимает путь в виде string к файлу с инструкциями и проверяемому каталогу
    True - если всё правильно
    False - если неправильно указан путь к инструкциям или проверяемому каталогу
    """
    if not (os.path.exists(f'{inst}') or os.path.exists(f'{dest}')):  # проверяю путь к инструкциям и к цели
        print('Wrong path to input file or destination')
        return False
    elif not os.path.isdir(f'{dest}'):  # проверяю является ли конечная цель директорией
        print('Destination is not a directory')
        return False
    return True


if check_everything(instructions_file, destination_path):  # проверяю
    review(instructions_file, destination_path)  # запускаю
