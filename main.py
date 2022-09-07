import psutil


def show_info():
    d = psutil.disk_partitions()
    print('C диск информация:', d[0])
    # print('D информация о диске:', d[1])
    # print('Информация о диске:', d[2])
    # print('Получить поле диска:', d[0][0], d[1][0], d[2][0])
    # print('Тип данных:', тип(d), '\ n')

if __name__ == '__main__':
    show_info()