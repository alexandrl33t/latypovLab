import os
def writefile():
    with open("file_to_write", 'w') as file:
        print("Введите строку для записи в файл:")
        file.write(input())
    with open("file_to_write", 'r') as file:
        print("Информация внутри файла:\n", file.read())
    # if os.path.isfile("file_to_write"):
    #     os.remove("file_to_write")

writefile()