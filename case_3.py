import os
import datetime
import random
import sys


class Testing:  # Головной класс
    def __init__(self):
        """
        Инициализация головного класса и запуск подклассов
        """
        print('Testing begins')
        Testing.FileListCase()  # вызов первого тест-кейса
        print('...')
        Testing.RandomFileCase()  # вызов второго тест-кейса

    class FileListCase:  # Тест-кейс 1: Список файлов
        def __init__(self, name='FileListCase', tc_id='0'):  # инициализация кейса через вызов метода execute
            """
            Инициализация первого тест-кейса
            """
            self.name = name
            self.tc_id = tc_id
            Testing.FileListCase.execute(self)

        def prep(self):
            """
            Если текущее системное время, заданное как целое количество секунд от
            начала эпохи Unix, не кратно двум, выполнение тест-кейса прерывается.
            """
            if int(datetime.datetime.timestamp(datetime.datetime.now())) % 2 == 1:  # проверка времени от начала эпохи
                return False
            else:
                return True

        def run(self):
            """
            Выводит список файлов из домашней директории текущего пользователя.
            """
            home_dir = os.path.expanduser('~')  # ищет домашнюю директорию пользователя
            files = os.listdir(home_dir)  # вызывает список объектов в домашней директории
            for diry in files[::-1]:  # удаляет папки из списка директории (вывести надо файлы)
                if os.path.isdir(f'C:/Users/georg/{diry}'):
                    files.remove(diry)
            print('Home directory files list:')
            for file in files:  # выводит список файлов
                print(file)

        def clean_up(self):
            """
            Метод завершения кейса, в данном случае пустой
            """
            pass

        def execute(self):
            """
            Задаёт общий порядок выполнения тест-кейса и обрабатывает исключительные ситуации.
            """
            print(f'Executing test: {self.name}, ID: {self.tc_id}')
            print('Checking datestamp')
            try:  # попытка запуска метода prep
                if Testing.FileListCase.prep(self):
                    print('Datestamp checked')
                    print('Parsing home directory')
                    try:  # попытка запуска метода run
                        Testing.FileListCase.run(self)
                        print('Home directory parsed')
                        print('Cleaning up')
                        try:  # попытка запуска метода clean_up
                            Testing.FileListCase.clean_up(self)
                            print('Test passed')
                        except Exception as ex:
                            print(f'Clean up failed with {ex}')
                    except Exception as ex:
                        print(f'Exception. Home directory parsing failed with {ex}')
                        print('Exception. Test stopped')
                else:
                    print('Datestamp unsuitable')
                    print('Test stopped')
            except Exception as ex:
                print(f'Exception. Datestamp check failed with {ex}')
                print('Exception. Test stopped')

    class RandomFileCase:
        def __init__(self, name='RandomFileCase', tc_id='1'):
            """
            Инициализация второго тест-кейса
            """
            self.name = name
            self.tc_id = tc_id
            Testing.RandomFileCase.execute(self)

        def prep(self):
            """
            Проверяет объем оперативной памяти машины, на которой исполняется тест,
            если меньше одного гигабайта, тест-кейс прерывается
            """
            if sys.platform == 'win32':  # проверка платформы на Win
                spec = os.popen('wmic memorychip get capacity')  # запрос на объем плашек оперативной памяти
                result = spec.read()
                spec.close()
                result = result.split('\n')
                ram_size = 0
                for data in result:
                    try:
                        ram_size += int(data)
                    except:
                        pass
                if ram_size <= 1024 ** 3:
                    return False  # если памяти меньше гигабайта возвращает False
                return True
            elif sys.platform == 'linux':  # проверка платформы на Linux
                tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
                if tot_m <= 1024 ** 3:
                    return False
                return True
            else:
                print('Unexpected platform, can\'t read RAM size')
                return False

        def run(self):
            """
            Создаёт файл test размером 1024кб состоящий из случайного набора байт
            """
            data = random.randbytes(1024 ** 2)  # генерирует случайную строку размером 1 Мб
            with open('test', 'wb') as test_file:
                test_file.write(data)  # записывает эту строку в файл

        def cleanup(self):
            """
            Удаляет файл тест
            """
            if os.path.exists('test'):
                os.remove('test')  # удаляет файл test

        def execute(self):
            """
            Задаёт общий порядок выполнения тест-кейса и обрабатывает исключительные ситуации.
            """
            print(f'Executing test: {self.name}, ID: {self.tc_id}')
            print('Testing RAM')
            try:
                if Testing.RandomFileCase.prep(self):
                    print('RAM test passed')
                    print('Creating random file')
                    try:
                        Testing.RandomFileCase.run(self)
                        try:
                            print('Cleaning up')
                            Testing.RandomFileCase.cleanup(self)
                            print('Test passed')
                        except Exception as ex:
                            print(f'Exception. Clean up failed with {ex}')
                            print('Exception. Test stopped')
                    except Exception as ex:
                        print(f'Exception. Random file creation failed with {ex}')
                        print('Exception. Test stopped')
                else:
                    print('RAM test failed')
                    print('Test stopped')
            except Exception as ex:
                print(f'Exception. RAM test failed with {ex}')
                print('Exception. Test stopped')


Testing()  # вызов головного класса с тест-кейсами
