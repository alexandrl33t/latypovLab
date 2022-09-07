import curses
import os
import json
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


def write_file():
    with open("new_file", 'w') as file:
        print("Введите строку для записи в файл:")
        file.write(input())
    with open("new_file", 'r') as file:
        print("Информация внутри файла:\n", file.read())
    if os.path.isfile("new_file"):
        os.remove("new_file")


def json_serializer():
    with open("new_file.json", 'w') as file:
        data = {'a': 34, 'b': 61, 'c': 82, 'd': 21}
        json.dump(data, file)


def on_press(key):
    if hasattr(key, 'char'):
        if key.char in ('1', '2', '3'):
            menu = {'1': show_info(), '2': write_file(), '3': json_serializer()}
            menu[key.char]
        else:
            return 1


def show_menu():
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    show_menu()