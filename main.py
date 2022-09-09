import shutil
import sys
import os
import win32api
from os import path
import json
import xml.etree.ElementTree as ET
import time
import psutil
from pynput import keyboard
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import zipfile

def show_info():
    """Доделать инфу на ноуте"""
    d = psutil.disk_partitions()
    c = psutil.disk_usage(d[0][0])
    metka = win32api.GetVolumeInformation(d[0][0])
    print('\nНазвание диска: ', d[0][0][:1])
    print('Тип: ', d[0][3][3:])
    print('Объем диска: ', round(c.total/1024/1024/1024, 2), "gb")
    print('Свободное пространство: ', round(c.free/1024/1024/1024, 2), "gb")
    print('Метка: ', metka[0], '\n')
    XmlGenerator.restart()


def writefile():
    with open("writefile/new_file.txt", 'w') as file:
        print("Введите строку для записи в файл:")
        file.write(input())
    with open("writefile/new_file.txt", 'r') as file:
        print("Информация внутри файла:\n", file.read())
    if os.path.isfile("writefile/new_file.txt"):
        os.remove("writefile/new_file.txt")
    print('Success!')
    time.sleep(2)
    XmlGenerator.restart()


class JsonSerializer:

    def __call__(self, *args, **kwargs):
        with open("jsonserializer/new_file.json", 'w') as file:
            data = {'a': 34, 'b': 61, 'c': 82, 'd': 21}
            json.dump(data, file, indent=4, )
        with open('jsonserializer/new_file.json') as f:
            dataJSON = json.load(f)
            with open('jsonserializer/json_serializedLAB.txt', 'w') as file:
                file.write(str(dataJSON))
            with open('jsonserializer//json_serializedLAB.txt', 'r') as file:
                print(f"Информация внутри файла\n {file.read()}")
            os.remove("jsonserializer/json_serializedLAB.txt")
        print('Success!')
        time.sleep(2)
        XmlGenerator.restart()



class XmlGenerator:

    tag = ""
    xml = None
    root = None
    tags = {}

    def __call__(self):
        self.tag = ""
        self.tags = {}
        self.xml = ET.parse('xml/orders.xml')
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
        options = {'1': self.add_tag, '2': self.change_tag, '3':self.delete_tag, '4': self.restart}
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
        print("\n*Напишите название тега и родительский элемент\n  Название тега: \n")
        tag_name = str(input())
        print("Выберете родительский элемент (опционально)\n")
        for tag in self.tags.items():
            print(tag[1], " - ", tag[0])
        parent = str(input())
        print("Текст внутри тега (опционально)\n")
        text_inside = str(input())
        if parent not in self.tags.keys():
            parent = self.tags['0']
        for elem in self.root.findall(self.tags[parent]):
            new_element = ET.SubElement(elem, tag_name)
            new_element.text = text_inside
        ET.dump(self.root)
        self.xml = ET.ElementTree(self.root)
        self.xml.write(open('xml/orders.xml', 'w'), encoding='unicode')

        print(f"Тег успешно добавлен!\nНовый XML:\n")

        time.sleep(2)
        self.restart()



    """Изменение существующего тега"""
    def change_tag(self):
        print("Выберете тег, который хотите изменить:")
        for tag in self.tags.items():
            print(tag[1], " - ", tag[0])
        key = str(input())
        self.tag_selected(key)

    def tag_selected(self, key):
        print(key)
        if key in tuple(item for item in self.tags.keys()):
            print(f"\nВыбран тег - {self.tags[key]}\n")
            print(" Новое название тега: \n")
            tag_name = str(input())
            for elem in self.xml.findall(self.tags[key]):
                elem.tag = tag_name
            self.xml.write("xml/orders.xml")
            print(f"Тег успешно изменен!\nНовый XML:\n")

        time.sleep(2)
        self.restart()

    def delete_tag(self):
        print("Выберете тег, который хотите удалить:")
        for tag in self.tags.items():
            print(tag[1], " - ", tag[0])
        key = str(input())
        self.tag_deleted(key)

    def tag_deleted(self, key):
        if key in tuple(item for item in self.tags.keys()):
            print(f"\nВыбран тег - {self.tags[key]}\n")
            self.tag = self.tags[key]
            print(f"\nВы действительно хотите удалить этот тег? (y,n)")
            with keyboard.Listener(on_press=self.finally_delete, suppress=True) as listener:
                listener.join()

    def get_key(self, value):
        for k, v in self.tags.items():
            if v == value:
                return str(k)


    def finally_delete(self, key):
        if hasattr(key, "char"):
            if key.char in ('y', 'n'):
                if key.char == 'y':
                    pass
                else:
                    self.tag_selected(self.get_key(self.tag))
            else:
                self.tag_selected(self.get_key(self.tag))
        else:
            self.tag_selected(self.get_key(self.tag))

        print("\nПроцесс удаления...\n")
        for i in reversed(range(len(self.tag))):
            print(f"{self.tag[0:i+1]}...")
            time.sleep(0.5)

        for elem in self.root.iter():
            if elem.tag == self.tag:
                self.root.remove(elem)
                break
            else:
                for child in elem.findall(self.tag):
                    elem.remove(child)
        tree = ET.ElementTree(self.root)
        tree.write(open('xml/orders.xml', 'w'), encoding='unicode')
        print("\nТег успешно удален!\n")
        print("ОБНОВЛЕННЫЙ XML\n")
        ET.dump(self.root)
        time.sleep(2)
        self.restart()



def create_zip():

    def contin(key):
        def contin(key):
            if hasattr(key, "char"):
                if key.char == 'y':
                    os.remove("new.zip")
                    os.remove(path.split(src)[1])
                    XmlGenerator.restart()
            XmlGenerator.restart()

        zip = zipfile.ZipFile('new.zip')
        zip.extractall("zip")
        zip.close()

        print("\nФайл успешно разархивирован\n Он находится в папке zip")
        print("\n Нажмите на клавишу y, чтобы удалить файл и архив")
        with keyboard.Listener(
                on_release=contin, suppress=True) as listener:
            listener.join()

    Tk().withdraw()
    src = askopenfilename()
    new_zip = zipfile.ZipFile('new.zip', 'w')
    new_zip.write(path.split(src)[1], compress_type=zipfile.ZIP_DEFLATED)
    new_zip.close()
    print("\nФайл успешно заархивирован\n Нажмите любую клавижу для продолжения")

    with keyboard.Listener(
            on_release=contin, suppress=True) as listener:
        listener.join()


def close_program():
    clear = "\n" * 100
    print(clear)
    raise SystemExit


def on_release(key):
    if hasattr(key, 'char'):
        if key.char in ('1', '2', '3', '4', '5', 'z'):
            menu = {'1': show_info,
                    '2': writefile,
                    '3': JsonSerializer(),
                    '4': XmlGenerator(),
                    '5': create_zip,
                    'z': close_program
                    }
            menu[key.char]()
        else:
            print("Ошибка! Неверно введена клавиша.")
            show_menu()
    return False


def show_menu():
    print(f"\n\n\nВведите цифру соответствующему пункту: \n")
    time.sleep(1)
    print(" Информация по дискам - 1 \n",
          "Запись и чтение файла - 2 \n",
          "JSON сериалайзер - 3 \n",
          "XML - 4 \n",
          "ZIP - 5\n",
          "Закрыть программу - z \n",
          )
    with keyboard.Listener(
            on_release=on_release) as listener:
        listener.join()


show_menu()
