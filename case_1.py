import xml.dom.minidom as minidom
import shutil
import os
from sys import exit

SOURCE = 'case_1_config.xml'  # исходный конфигурационный xml-файл из задания


def dict_prepper(file_name):
    """
    Извлекает данные из конфигурационного xml-файла
    На входе xml-файл
    На выходе словарь
    """
    try:
        xml_dom = minidom.parse(file_name)  # парсим xml-файл
        files = xml_dom.getElementsByTagName('file')  # ищем тэги files
        file_dict = {}  # формируем словарь под файлы
        for file in files:  # заносим данные из тэгов в словарь
            source_path = file.attributes['source_path'].value
            destination_path = file.attributes['destination_path'].value
            file_name = file.attributes['file_name'].value
            file_dict[file_name] = {'source_path': source_path, 'destination_path': destination_path}
        return file_dict
    except Exception as ex:
        exit(f'Configuration file broken or not found and {ex}')


def copy(src, dst):
    """
    Просто копирует файл из src в dst
    (необходимо прописывать полный путь)
    Не создаёт папки на пути и не проверяет замену
    """
    print(f'Copying {src} to {dst}')
    try:
        print(f'Success!')
        shutil.copyfile(src, dst)
    except PermissionError:
        print(f'Can\'t copy {src} to {dst}')
        print('Permission error, run under admin rights')
    except Exception as ex:
        print(f'Can\'t copy {src} to {dst}')
        print(f'{ex}')


def copy_from_dict(dict_of_files):
    """
    Запускает процесс копирования по данным из словаря
    {'spam.eggs': {'source_path' : '/foo', 'destination_path' : '/bar'}
    Создаёт по пути каталоги и надо ли перезаписать файл, если такой существует
    """
    for file_name in dict_of_files:
        s_path = dict_of_files[file_name]['source_path'] + '/' + file_name  # формирую путь к исходнику
        if os.path.exists(s_path):  # проверяю, существует ли исходник в принципе
            d_path = dict_of_files[file_name]['destination_path']  # формирую путь к назачению
            d_full_path = d_path + '/' + file_name  # формирую путь к назначению с названием файла
            if os.path.exists(d_path):  # проверяю, есть ли папки по пути к назначению
                if os.path.isfile(d_full_path):  # проверяю, существует ли такой файл в назначении
                    print('File exists, overwrite? (Y(es) / Any other input (Cancel)')
                    overwrite = input().capitalize()
                    if overwrite == 'Y':
                        copy(s_path, d_full_path)  # копирую
                    else:
                        pass  # если решили не переписывать ничего не происходит,
                else:
                    copy(s_path, d_full_path)
            else:
                os.makedirs(d_path)  # создаёт дирекории по пути
                copy(s_path, d_full_path)  # копирует
        else:
            print(f'Can\'t find {s_path}, check file for existence')


xml_dic = dict_prepper(SOURCE)  # готовлю словарь
copy_from_dict(xml_dic)  # копирую
