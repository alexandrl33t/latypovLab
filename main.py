import sys
import os
import json
import xml.etree.ElementTree as ET
import time
import psutil
from pynput import keyboard


def show_info():
    """Доделать инфу на ноуте"""
    d = psutil.disk_partitions()
    print('C диск информация:', d[0])
    # print('D информация о диске:', d[1])
    # print('Информация о диске:', d[2])
    # print('Получить поле диска:', d[0][0], d[1][0], d[2][0])
    # print('Тип данных:', тип(d), '\ n')
    show_menu()


def writefile():
    with open("new_file", 'w') as file:
        print("Введите строку для записи в файл:")
        file.write(input())
    with open("new_file", 'r') as file:
        print("Информация внутри файла:\n", file.read())
    if os.path.isfile("new_file"):
        os.remove("new_file")
    exit()


class JsonSerializer:

    def __call__(self, *args, **kwargs):
        with open("new_file.json", 'w') as file:
            data = {'a': 34, 'b': 61, 'c': 82, 'd': 21}
            json.dump(data, file, indent=4, )
        with open('new_file.json') as f:
            dataJSON = json.load(f)
            with open('json_serializedLAB.txt', 'w') as file:
                file.write(str(dataJSON))
            with open('json_serializedLAB.txt', 'r') as file:
                print(f"\n {file.read()}")
            os.remove("json_serializedLAB.txt")
        exit()


class XmlGenerator:

    def __call__(self):
        self.tags = {}
        self.xml = ET.parse('orders.xml')
        self.root = self.xml.getroot()
        for i, child in enumerate(self.root.iter()):
            self.tags[str(i)] = child.tag

        print("Полученный  XML: \n")
        time.sleep(1)
        if ET.dump(self.xml):
            print(ET.dump(self.xml))
        print("Выберете опцию: \n",
              "Добавить тег - 1\n",
              "Изменить тег - 2\n",
              "Удалить тег - 3\n",
              "Вернуться назад - 4\n"
              )
        with keyboard.Listener(on_press=self.option) as listener:
            listener.join()

    def option(self, key):
        options = {'1': self.add_tag, '2': self.change_tag, '4': self.restart}
        if hasattr(key, "char"):
            if key.char in tuple(item for item in options.keys()):
                options[key.char]()
            else:
                print("Ошибка")
                XmlGenerator()

    @staticmethod
    def restart():
        os.execv(sys.executable, [sys.executable] + sys.argv)


    """Добавить новый тег"""
    def add_tag(self):
        print("\n*Напишите название тега и родительский элемент  Название тега: \n")
        tag_name = str(input())
        print("Родительский элемент (опционально)\n")
        parent = str(input())
        if parent not in self.tags.values():
            parent = self.tags['0']
        parent_element = ET.Element(parent)
        new_element = ET.SubElement(parent_element, tag_name)
        self.root.insert(0, new_element)
        ET.dump(self.root)
        tree = ET.ElementTree(self.root)
        tree.write(open('orders.xml', 'w'), encoding='unicode')


    """Изменение существующего тега"""
    def change_tag(self):
        print("Выберете тег, который хотите изменить:")
        for tag in self.tags.items():
            print(tag[1], " - ", tag[0])
        with keyboard.Listener(on_press=self.tag_selected) as listener:
            listener.join()

    def tag_selected(self, key):

        def tag_option(key):
            if hasattr(key, 'char'):
                if key.char in ('1', '2'):
                    if key.char == '1':
                        parent_element = ET.Element(self.tags[key.char])
                        print("Введите название тега: \n")
                        tag_name = str(input())
                        new_element = ET.SubElement(parent_element, tag_name)
                        for item in self.root.iter():
                            if item.tag == self.tags[key.char]:
                                item = parent_element
                        ET.dump(self.root)
                        tree = ET.ElementTree(self.root)
                        tree.write(open('orders.xml', 'w'), encoding='unicode')
                        return False
                    else:
                        print(2)
                else:
                    print("Ошибка")
                    return False
            else:
                print("Ошибка")
                return False

        if hasattr(key, 'char'):
            if key.char in tuple(item for item in self.tags.keys()):
                print(f"\nВыбран тег - {self.tags[key.char]}\n")
                print("Выберете опцию: \n"
                      "Добавить дочерний тег - 1 \n"
                      "Изменить название текущего тега - 2 \n"
                      )
                with keyboard.Listener(on_press=tag_option) as listener2:
                    listener2.join()
            else:
                XmlGenerator()
        else:
            print(list(item for item in self.tags.keys()))
            print("Ошибка")
            XmlGenerator()


def exit():
    clear = "\n" * 100
    print(clear)
    raise SystemExit


def on_release(key):
    if hasattr(key, 'char'):
        if key.char in ('1', '2', '3', '4', 'z'):
            menu = {'1': show_info, '2': writefile, '3': JsonSerializer(), '4': XmlGenerator(), 'z': exit}
            menu[key.char]()
        else:
            print("Ошибка! Неверно введена клавиша.")
            show_menu()
    return False


def show_menu():
    print(f"Введите цифру соответствующему пункту: \n")
    time.sleep(1)
    print("Информация по дискам - 1 \n"
          "Запись и чтение файла - 2 \n"
          "JSON сериалайзер - 3 \n"
          "XML - 4 \n",
          "Закрыть программу - z \n"
          )
    with keyboard.Listener(
            on_release=on_release) as listener:
        listener.join()


show_menu()
