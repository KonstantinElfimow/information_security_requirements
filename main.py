import io
import os
import tkinter as tk
from collections.abc import Iterable
from tkinter import ttk
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'YaBrowser/23.3.1.895 Yowser/2.5 Safari/537.36 '
}


class MyFiles:
    FILE_PATH_ISC: str = 'data/information_security_class.csv'
    FILE_PATH_SCR: str = 'data/security_class_requirements.csv'

    FILE_PATH_REQ_GROUP_1: str = 'data/requirements_group_1.csv'
    FILE_PATH_REQ_GROUP_2: str = 'data/requirements_group_2.csv'
    FILE_PATH_REQ_GROUP_3: str = 'data/requirements_group_3.csv'


class ReservedValuesInTables:
    COLUMNS_ISC: tuple = ('уровень_значимости', 'федеральный', 'региональный', 'объектовый')
    COLUMNS_SCR: tuple = ('номер_меры', 'мера_защиты', 'К3', 'К2', 'К1')
    COLUMNS_REQ_GROUP_1: tuple = ('подсистемы_и_требования', '1Д', '1Г', '1В', '1Б', '1А')
    COLUMNS_REQ_GROUP_2: tuple = ('подсистемы_и_требования', '2Б', '2А')
    COLUMNS_REQ_GROUP_3: tuple = ('подсистемы_и_требования', '3Б', '3А')

    SIGNIFICANCE_LEVEL_VALUES: tuple = ('УЗ 1', 'УЗ 2', 'УЗ 3')
    SCALE_VALUES: tuple = ('федеральный', 'региональный', 'объектовый')
    PRIVACY_LEVEL_VALUES: tuple = ('один', 'различный')
    POWER_VALUES: tuple = ('да', 'нет')
    MODE_VALUES: tuple = ('индивидуальный', 'коллективный')
    SECRECY_VALUES: tuple = (
        'особой важности', 'совершенно секретно', 'секретно', 'не секретно (циркулирует служебная тайна)',
        'не секретно (только персональные данные)')

    GROUP_VALUES: tuple = (1, 2, 3)


def pull_html(url: str, file_path: str) -> bool:
    # Отключение проверки сертификата SSL
    requests.packages.urllib3.disable_warnings()
    req = requests.get(url, headers=headers, verify=False)
    src = req.text

    with open(file_path, mode='w', encoding='utf-8') as html_file:
        html_file.write(src)
    return True


def write_csv(file_path: str, columns: Iterable, data: Iterable) -> bool:
    with open(file_path, mode='w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(columns)
        writer.writerows(data)
    return True


def prepare_data_from_order():
    url = 'https://fstec.ru/dokumenty/vse-dokumenty/prikazy/prikaz-fstek-rossii-ot-11-fevralya-2013-g-n-17'

    file_path_html_order = 'index_order.html'
    if not os.path.isfile(file_path_html_order):
        pull_html(url, file_path_html_order)

    if not os.path.isfile(MyFiles.FILE_PATH_ISC) or not os.path.isfile(MyFiles.FILE_PATH_SCR):
        with open(file_path_html_order, mode='r', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        tables = soup.find_all('table', class_='sltable')

        if not os.path.isfile(MyFiles.FILE_PATH_ISC):
            table_isc = tables[0]
            table_rows = table_isc.find('tbody').find_all('tr')

            data = []
            for row in table_rows:
                attr_values = row.find_all('td')

                v1 = attr_values[0].text.replace(' ', ' ').strip()
                v2 = attr_values[1].text.strip()
                v3 = attr_values[2].text.strip()
                v4 = attr_values[3].text.strip()

                data.append([v1, v2, v3, v4])

            write_csv(MyFiles.FILE_PATH_ISC, ReservedValuesInTables.COLUMNS_ISC, data)

        if not os.path.isfile(MyFiles.FILE_PATH_SCR):
            table_scr = tables[1]
            table_rows = table_scr.find('tbody').find_all('tr')

            data = []
            for row in table_rows:
                attr_values = row.find_all('td')

                if len(attr_values) != 5:
                    continue

                v1 = attr_values[0].text.replace(' ', ' ').strip()
                v2 = attr_values[1].text.replace(' ', ' ').strip()
                v3 = bool(attr_values[2].text.strip())
                v4 = bool(attr_values[3].text.strip())
                v5 = bool(attr_values[4].text.strip())

                data.append([v1, v2, v3, v4, v5])

            write_csv(MyFiles.FILE_PATH_SCR, ReservedValuesInTables.COLUMNS_SCR, data)


def prepare_data_from_guidance_document():
    url = 'https://fstec.ru/dokumenty/vse-dokumenty/spetsialnye-normativnye-dokumenty/rukovodyashchij-dokument-ot-30' \
          '-marta-1992-g-3 '

    file_path_html_document = 'index_document.html'
    if not os.path.isfile(file_path_html_document):
        pull_html(url, file_path_html_document)

    if not os.path.isfile(MyFiles.FILE_PATH_REQ_GROUP_1) or \
            not os.path.isfile(MyFiles.FILE_PATH_REQ_GROUP_2) or \
            not os.path.isfile(MyFiles.FILE_PATH_REQ_GROUP_3):
        with open(file_path_html_document, mode='r', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        tables = soup.find_all('table', class_='sltable')

        if not os.path.isfile(MyFiles.FILE_PATH_REQ_GROUP_3):
            table_req_group_3 = tables[0]
            table_rows = table_req_group_3.find('tbody').find_all('tr')

            data = []
            for row in table_rows[2:]:
                attr_values = row.find_all('td')

                v1 = attr_values[0].text.replace(' ', ' ').strip()
                v2_attr = attr_values[1].text.replace(' ', ' ').strip()
                v2 = True if v2_attr == '+' else False if v2_attr == '-' else None
                v3_attr = attr_values[2].text.replace(' ', ' ').strip()
                v3 = True if v3_attr == '+' else False if v3_attr == '-' else None

                data.append([v1, v2, v3])

            write_csv(MyFiles.FILE_PATH_REQ_GROUP_3, ReservedValuesInTables.COLUMNS_REQ_GROUP_3, data)

        if not os.path.isfile(MyFiles.FILE_PATH_REQ_GROUP_2):
            table_req_group_2 = tables[1]
            table_rows = table_req_group_2.find('tbody').find_all('tr')

            data = []
            for row in table_rows[2:]:
                attr_values = row.find_all('td')

                v1 = attr_values[0].text.replace(' ', ' ').strip()
                v2_attr = attr_values[1].text.replace(' ', ' ').strip()
                v2 = True if v2_attr == '+' else False if v2_attr == '-' else None
                v3_attr = attr_values[2].text.replace(' ', ' ').strip()
                v3 = True if v3_attr == '+' else False if v3_attr == '-' else None

                data.append([v1, v2, v3])

            write_csv(MyFiles.FILE_PATH_REQ_GROUP_2, ReservedValuesInTables.COLUMNS_REQ_GROUP_2, data)

        if not os.path.isfile(MyFiles.FILE_PATH_REQ_GROUP_1):
            table_req_group_1 = tables[2]
            table_rows = table_req_group_1.find('tbody').find_all('tr')

            data = []
            for row in table_rows[2:]:
                attr_values = row.find_all('td')

                v1 = attr_values[0].text.replace(' ', ' ').strip()
                v2_attr = attr_values[1].text.replace(' ', ' ').strip()
                v2 = True if v2_attr == '+' else False if v2_attr == '-' else None
                v3_attr = attr_values[2].text.replace(' ', ' ').strip()
                v3 = True if v3_attr == '+' else False if v3_attr == '-' else None
                v4_attr = attr_values[3].text.replace(' ', ' ').strip()
                v4 = True if v4_attr == '+' else False if v4_attr == '-' else None
                v5_attr = attr_values[4].text.replace(' ', ' ').strip()
                v5 = True if v5_attr == '+' else False if v5_attr == '-' else None
                v6_attr = attr_values[5].text.replace(' ', ' ').strip()
                v6 = True if v6_attr == '+' else False if v6_attr == '-' else None

                data.append([v1, v2, v3, v4, v5, v6])

            write_csv(MyFiles.FILE_PATH_REQ_GROUP_1, ReservedValuesInTables.COLUMNS_REQ_GROUP_1, data)


# def show_security_class_requirements(significance_level: str, scale: str):
#     df_isc = pd.read_csv(MyFiles.FILE_PATH_ISC, delimiter=';')
#     df_scr = pd.read_csv(MyFiles.FILE_PATH_SCR, delimiter=';')
#
#     root = tk.Tk()
#
#     root.attributes('-fullscreen', True)
#
#     label = tk.Label(root, text='Требования по приказу №17 ФСТЭК России')
#     label.pack()
#
#     text = tk.Text(root, padx=15, pady=15)
#     text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
#
#     button_back = tk.Button(root, text='Назад', command=root.destroy)
#     button_back.pack(side=tk.LEFT, fill=tk.Y)
#
#     if significance_level not in ReservedValuesInTables.SIGNIFICANCE_LEVEL_VALUES or \
#             scale not in ReservedValuesInTables.SCALE_VALUES:
#         text.insert(tk.END, 'Введены неверные данные!')
#     else:
#         security_class = df_isc.loc[df_isc['уровень_значимости'] == significance_level, scale].values[0]
#         requirements = (df_scr.loc[df_scr[security_class], ['номер_меры', 'мера_защиты']])
#
#         stringIO = io.StringIO()
#         for index, row in requirements.iterrows():
#             number_measure = row['номер_меры']
#             protective_measure = row['мера_защиты']
#             stringIO.write('- {}: {}\n'.format(number_measure, protective_measure))
#
#         text.insert(
#             tk.END, 'Ваш класс защищённости:\n{}\nТребования к системе:\n{}'.format(security_class, stringIO.getvalue())
#         )
#
#     root.mainloop()


# def show_automated_system_requirements(privacy_level: str, power: str, mode: str, secrecy: str):
#     df_define_group = pd.DataFrame({
#         'группа': ReservedValuesInTables.GROUP_VALUES,
#         'уровень_конфиденциальности': ['различный', 'различный', 'один'],
#         'равные_полномочие': ['нет', 'да', 'да'],
#         'режим_обработки': ['коллективный', 'коллективный', 'индивидуальный']
#     })
#
#     df_define_class = pd.DataFrame({
#         'секретность_данных': ReservedValuesInTables.SECRECY_VALUES,
#         1: ['1А', '1Б', '1В', '1Г', '1Д'],
#         2: ['2А', '2А', '2А', '2Б', '2Б'],
#         3: ['3А', '3А', '3А', '3Б', '3Б']
#     })
#
#     root = tk.Tk()
#     root.attributes('-fullscreen', True)
#
#     label = tk.Label(root, text='Требования по руководящему документу (Автоматизированные системы. Защита от '
#                                 'несанкционированного доступа к информации) ФСТЭК России')
#     label.pack()
#
#     text = tk.Text(root, padx=15, pady=15)
#     text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
#
#     button_back = tk.Button(root, text='Назад', command=root.destroy)
#     button_back.pack(side=tk.LEFT, fill=tk.Y)
#
#     if privacy_level not in ReservedValuesInTables.PRIVACY_LEVEL_VALUES or \
#             power not in ReservedValuesInTables.POWER_VALUES or \
#             mode not in ReservedValuesInTables.MODE_VALUES:
#         text.insert(tk.END, 'Введены неверные данные!')
#     else:
#         automated_system_group = df_define_group.loc[(df_define_group['уровень_конфиденциальности'] == privacy_level) &
#                                                      (df_define_group['равные_полномочие'] == power) &
#                                                      (df_define_group['режим_обработки'] == mode), 'группа']
#         if len(automated_system_group) < 1:
#             text.insert(tk.END, 'Введенные данные не удовлетворяют ни одной из групп АС!')
#         else:
#             automated_system_group = automated_system_group.values[0]
#             automated_system_class = \
#                 df_define_class.loc[df_define_class['секретность_данных'] == secrecy, automated_system_group].values[0]
#
#             file = getattr(MyFiles, f'FILE_PATH_REQ_GROUP_{automated_system_group}', None)
#             if file is None:
#                 raise FileExistsError('Файл был удалён или перенесён в другую директорию!')
#
#             df_group_requirements = pd.read_csv(file, delimiter=';', keep_default_na=False, na_values='')
#             requirements = df_group_requirements.loc[df_group_requirements[automated_system_class].isna() |
#                                                      df_group_requirements[automated_system_class],
#                                                      ['подсистемы_и_требования']]
#
#             stringIO = io.StringIO()
#             for index, row in requirements.iterrows():
#                 subsystems_and_requirements = row['подсистемы_и_требования']
#                 stringIO.write('- {}\n'.format(subsystems_and_requirements))
#
#             text.insert(
#                 tk.END,
#                 'Ваш класс АС:\n{}\nТребования по защите информации от НСД для АС:\n{}'.format(automated_system_class,
#                                                                                                stringIO.getvalue())
#             )
#
#     root.mainloop()

def save_data(path: str, data: str):
    dirs = path.split('/')
    dirs.pop()

    current_dir = io.StringIO()
    for d in dirs:
        current_dir.write(f'{d}/')
        if not os.path.exists(current_dir.getvalue()):
            os.makedirs(current_dir.getvalue())

    with open(path, mode='w', encoding='windows-1251') as file:
        file.write(data)


def show_requirements(significance_level: str, scale: str, privacy_level: str, power: str, mode: str, secrecy: str):
    df_isc = pd.read_csv(MyFiles.FILE_PATH_ISC, delimiter=';')
    df_scr = pd.read_csv(MyFiles.FILE_PATH_SCR, delimiter=';')

    df_define_group = pd.DataFrame({
        'группа': ReservedValuesInTables.GROUP_VALUES,
        'уровень_конфиденциальности': ['различный', 'различный', 'один'],
        'равные_полномочие': ['нет', 'да', 'да'],
        'режим_обработки': ['коллективный', 'коллективный', 'индивидуальный']
    })

    df_define_class = pd.DataFrame({
        'секретность_данных': ReservedValuesInTables.SECRECY_VALUES,
        1: ['1А', '1Б', '1В', '1Г', '1Д'],
        2: ['2А', '2А', '2А', '2Б', '2Б'],
        3: ['3А', '3А', '3А', '3Б', '3Б']
    })

    root = tk.Tk()
    root.attributes('-fullscreen', True)

    label = tk.Label(root, text='Требования по документам ФСТЭК России')
    label.pack()

    text = tk.Text(root, padx=15, pady=15)
    text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    button_back = tk.Button(root, text='Назад', command=root.destroy)
    button_back.pack()

    if significance_level not in ReservedValuesInTables.SIGNIFICANCE_LEVEL_VALUES or \
            scale not in ReservedValuesInTables.SCALE_VALUES or \
            privacy_level not in ReservedValuesInTables.PRIVACY_LEVEL_VALUES or \
            power not in ReservedValuesInTables.POWER_VALUES or \
            mode not in ReservedValuesInTables.MODE_VALUES:
        text.insert(tk.END, 'Введены неверные данные!')
    else:
        security_class = df_isc.loc[df_isc['уровень_значимости'] == significance_level, scale].values[0]
        order_requirements = (df_scr.loc[df_scr[security_class], ['номер_меры', 'мера_защиты']])

        automated_system_group = df_define_group.loc[(df_define_group['уровень_конфиденциальности'] == privacy_level) &
                                                     (df_define_group['равные_полномочие'] == power) &
                                                     (df_define_group['режим_обработки'] == mode), 'группа']
        if len(automated_system_group) < 1:
            text.insert(tk.END, 'Введенные данные не удовлетворяют ни одной из групп АС!')
        else:
            automated_system_group = automated_system_group.values[0]
            automated_system_class = \
                df_define_class.loc[df_define_class['секретность_данных'] == secrecy, automated_system_group].values[0]

            file = getattr(MyFiles, f'FILE_PATH_REQ_GROUP_{automated_system_group}', None)
            if file is None:
                raise FileExistsError('Файл был удалён или перенесён в другую директорию!')

            df_group_requirements = pd.read_csv(file, delimiter=';', keep_default_na=False, na_values='')
            document_requirements = df_group_requirements.loc[df_group_requirements[automated_system_class].isna() |
                                                              df_group_requirements[automated_system_class],
                                                              ['подсистемы_и_требования']]

            stringIO = io.StringIO()

            stringIO.write('Ваш класс защищённости:\n{}\n'.format(security_class))
            for index, row in order_requirements.iterrows():
                number_measure = row['номер_меры']
                protective_measure = row['мера_защиты']
                stringIO.write('- {}: {}\n'.format(number_measure, protective_measure))
            stringIO.write('Ваш класс АС:\n{}\n'
                           'Требования по защите информации от НСД для АС:\n'.format(automated_system_class))
            for index, row in document_requirements.iterrows():
                subsystems_and_requirements = row['подсистемы_и_требования']
                stringIO.write('{}\n'.format(subsystems_and_requirements))

            text.insert(tk.END, stringIO.getvalue())

            label = tk.Label(root, text='Сохранить как:')
            label.pack()

            entry = tk.Entry(root)
            entry.insert(0, 'output/your_requirements.txt')
            entry.pack()

            button = tk.Button(root, text='Сохранить', command=lambda: save_data(entry.get(), stringIO.getvalue()))
            button.pack()

    root.mainloop()


def create_window():
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - root.winfo_reqwidth() - 400) / 2
    y = (screen_height - root.winfo_reqheight() - 400) / 2

    # Set the position of the window
    root.geometry('600x500+%d+%d' % (x, y))

    title_1 = tk.Label(root, text='\nТребования к мерам защиты информации, содержащейся в информационной системе\n',
                       font=("Helvetica", 10, "bold"))
    title_1.pack()

    label1 = tk.Label(root, text='Выберите уровень значимости информации:')
    label1.pack()

    combo_significance_level = ttk.Combobox(root, values=ReservedValuesInTables.SIGNIFICANCE_LEVEL_VALUES)
    combo_significance_level.pack()

    label2 = tk.Label(root, text='Выберите масштаб системы:')
    label2.pack()

    combo_scale = ttk.Combobox(root, values=ReservedValuesInTables.SCALE_VALUES)
    combo_scale.pack()

    # button = tk.Button(root, text='Вывести требования',
    #                    command=lambda: show_security_class_requirements(combo_significance_level.get(),
    #                                                                     combo_scale.get()))
    # button.pack()

    title_2 = tk.Label(root, text='\nКлассификация AC и требования по защите информации\n',
                       font=("Helvetica", 10, "bold"))
    title_2.pack()

    label3 = tk.Label(root, text='Наличие в АС информации различного уровня конфиденциальности:')
    label3.pack()

    combo_privacy_level = ttk.Combobox(root, values=ReservedValuesInTables.PRIVACY_LEVEL_VALUES)
    combo_privacy_level.pack()

    label4 = tk.Label(root, text='Равные права доступа (полномочия) ко всей информации АС:')
    label4.pack()

    combo_power = ttk.Combobox(root, values=ReservedValuesInTables.POWER_VALUES)
    combo_power.pack()

    label5 = tk.Label(root, text='Режим обработки данных в АС:')
    label5.pack()

    combo_modes = ttk.Combobox(root, values=ReservedValuesInTables.MODE_VALUES)
    combo_modes.pack()

    label6 = tk.Label(root, text='Степень секретности данных:')
    label6.pack()

    combo_secrecy = ttk.Combobox(root, values=ReservedValuesInTables.SECRECY_VALUES)
    combo_secrecy.pack()

    # button = tk.Button(root, text='Вывести требования',
    #                    command=lambda: show_automated_system_requirements(combo_privacy_level.get(), combo_power.get(),
    #                                                                       combo_modes.get(), combo_secrecy.get()))
    # button.pack()

    button = tk.Button(root, text='Вывести все требования',
                       command=lambda: show_requirements(combo_significance_level.get(),
                                                         combo_scale.get(), combo_privacy_level.get(),
                                                         combo_power.get(),
                                                         combo_modes.get(), combo_secrecy.get()))
    button.pack()

    root.mainloop()


def main():
    prepare_data_from_order()
    prepare_data_from_guidance_document()
    create_window()


if __name__ == '__main__':
    main()
