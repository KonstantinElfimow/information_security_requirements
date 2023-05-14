import io
import os
import tkinter as tk
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


def pull_html(url: str, file_path: str) -> bool:
    # Отключение проверки сертификата SSL
    requests.packages.urllib3.disable_warnings()
    req = requests.get(url, headers=headers, verify=False)
    src = req.text

    with open(file_path, mode='w', encoding='utf-8') as html_file:
        html_file.write(src)
    return True


def write_csv(file_path: str, columns: list, data: list) -> bool:
    with open(file_path, mode='w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(columns)
        writer.writerows(data)
    return True


file_path_isc = 'data/information_security_class.csv'
file_path_scr = 'data/security_class_requirements.csv'


def prepare_data_from_order():
    url = 'https://fstec.ru/dokumenty/vse-dokumenty/prikazy/prikaz-fstek-rossii-ot-11-fevralya-2013-g-n-17'

    file_path_html_order = 'index_order.html'
    if not os.path.isfile(file_path_html_order):
        pull_html(url, file_path_html_order)

    if not os.path.isfile(file_path_isc) or not os.path.isfile(file_path_scr):
        with open(file_path_html_order, mode='r', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        tables = soup.find_all('table', class_='sltable')

        if not os.path.isfile(file_path_isc):
            table_isc = tables[0]
            table_rows = table_isc.find('tbody').find_all('tr')

            columns = ['уровень_значимости', 'федеральный', 'региональный', 'объектовый']

            data = []
            for row in table_rows:
                attr_values = row.find_all('td')

                v1 = attr_values[0].text.replace(' ', ' ').strip()
                v2 = attr_values[1].text.strip()
                v3 = attr_values[2].text.strip()
                v4 = attr_values[3].text.strip()

                data.append([v1, v2, v3, v4])

            write_csv(file_path_isc, columns, data)

        if not os.path.isfile(file_path_scr):
            table_scr = tables[1]
            table_rows = table_scr.find('tbody').find_all('tr')

            columns = ['номер_меры', 'мера_защиты', 'К3', 'К2', 'К1']

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

            write_csv(file_path_scr, columns, data)


file_path_req_class_1 = 'data/requirements_class_1.csv'
file_path_req_class_2 = 'data/requirements_class_2.csv'
file_path_req_class_3 = 'data/requirements_class_3.csv'


def prepare_data_from_guidance_document():
    url = 'https://fstec.ru/dokumenty/vse-dokumenty/spetsialnye-normativnye-dokumenty/rukovodyashchij-dokument-ot-30' \
          '-marta-1992-g-3 '

    file_path_html_document = 'index_document.html'
    if not os.path.isfile(file_path_html_document):
        pull_html(url, file_path_html_document)

    if not os.path.isfile(file_path_req_class_1) or not os.path.isfile(file_path_req_class_2) or not os.path.isfile(file_path_req_class_3):
        with open(file_path_html_document, mode='r', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        tables = soup.find_all('table', class_='sltable')

        if not os.path.isfile(file_path_req_class_3):
            table_req_class_3 = tables[0]
            table_rows = table_req_class_3.find('tbody').find_all('tr')

            columns = ['подсистемы_и_требования', '3Б', '3А']

            data = []
            for row in table_rows[2:]:
                attr_values = row.find_all('td')

                v1 = attr_values[0].text.replace(' ', ' ').strip()
                v2_attr = attr_values[1].text.replace(' ', ' ').strip()
                v2 = True if v2_attr == '+' else False if v2_attr == '-' else None
                v3_attr = attr_values[2].text.replace(' ', ' ').strip()
                v3 = True if v3_attr == '+' else False if v3_attr == '-' else None

                data.append([v1, v2, v3])

            write_csv(file_path_req_class_3, columns, data)

        if not os.path.isfile(file_path_req_class_2):
            table_req_class_2 = tables[1]
            table_rows = table_req_class_2.find('tbody').find_all('tr')

            columns = ['подсистемы_и_требования', '2Б', '2А']

            data = []
            for row in table_rows[2:]:
                attr_values = row.find_all('td')

                v1 = attr_values[0].text.replace(' ', ' ').strip()
                v2_attr = attr_values[1].text.replace(' ', ' ').strip()
                v2 = True if v2_attr == '+' else False if v2_attr == '-' else None
                v3_attr = attr_values[2].text.replace(' ', ' ').strip()
                v3 = True if v3_attr == '+' else False if v3_attr == '-' else None

                data.append([v1, v2, v3])

            write_csv(file_path_req_class_2, columns, data)

        if not os.path.isfile(file_path_req_class_1):
            table_req_class_1 = tables[2]
            table_rows = table_req_class_1.find('tbody').find_all('tr')

            columns = ['подсистемы_и_требования', '1Д', '1Г', '1В', '1Б', '1А']

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

            write_csv(file_path_req_class_1, columns, data)


def show_security_class_requirements(df_isc: pd.DataFrame, df_scr: pd.DataFrame, significance_level: str, scale: str):
    root = tk.Tk()

    root.attributes('-fullscreen', True)

    label = tk.Label(root, text='Требования по приказу №17 ФСТЭК России')
    label.pack()

    text = tk.Text(root, padx=15, pady=15)
    text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    if significance_level not in ('УЗ 1', 'УЗ 2', 'УЗ 3') and scale not in (
            'федеральный', 'региональный', 'объектовый'):
        text.insert(tk.END, 'Введены неверные данные!')
    else:
        security_class = df_isc.loc[df_isc['уровень_значимости'] == significance_level, scale].values[0]
        requirements = (df_scr.loc[df_scr[security_class], ['номер_меры', 'мера_защиты']])

        stringIO = io.StringIO()
        for index, row in requirements.iterrows():
            number_measure = row['номер_меры']
            protective_measure = row['мера_защиты']
            stringIO.write('- {}: {}\n'.format(number_measure, protective_measure))

        text.insert(tk.END,
                    'Ваш класс защищённости:\n{}\nТребования к системе:\n{}'.format(security_class,
                                                                                    stringIO.getvalue()))

    button_back = tk.Button(root, text='Назад', command=root.destroy)
    button_back.pack(side=tk.LEFT, fill=tk.Y)

    root.mainloop()


def create_window():
    df_isc = pd.read_csv(file_path_isc, delimiter=';')
    df_scr = pd.read_csv(file_path_scr, delimiter=';')

    df_req_class_1 = pd.read_csv(file_path_req_class_1, delimiter=';', keep_default_na=False, na_values='')
    df_req_class_2 = pd.read_csv(file_path_req_class_2, delimiter=';', keep_default_na=False, na_values='')
    df_req_class_3 = pd.read_csv(file_path_req_class_3, delimiter=';', keep_default_na=False, na_values='')

    root = tk.Tk()

    # Get the width and height of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates of the top-left corner of the window
    x = (screen_width - root.winfo_reqwidth() - 400) / 2
    y = (screen_height - root.winfo_reqheight() - 400) / 2

    # Set the position of the window
    root.geometry('600x400+%d+%d' % (x, y))

    main_label = tk.Label(root, text='Информационная система')
    main_label.pack()

    label1 = tk.Label(root, text='Выберите уровень значимости:')
    label1.pack()

    significance_levels = ['УЗ 1', 'УЗ 2', 'УЗ 3']
    combo_significance_level = ttk.Combobox(root, values=significance_levels)
    combo_significance_level.pack()

    label2 = tk.Label(root, text='Выберите масштаб:')
    label2.pack()

    scales = ['федеральный', 'региональный', 'объектовый']
    combo_scale = ttk.Combobox(root, values=scales)
    combo_scale.pack()

    button = tk.Button(root, text='Вывести требования',
                       command=lambda: show_security_class_requirements(df_isc, df_scr, combo_significance_level.get(),
                                                                        combo_scale.get()))
    button.pack()

    label3 = tk.Label(root, text='\nНаличие в АС информации различного уровня конфиденциальности:')
    label3.pack()

    privacy_levels = ['один', 'различный']
    combo_privacy_level = ttk.Combobox(root, values=privacy_levels)
    combo_privacy_level.pack()

    label4 = tk.Label(root, text='Уровень полномочий субъектов доступа АС на доступ к конфиденциальной информации:')
    label4.pack()

    powers = ['']
    combo_power = ttk.Combobox(root, values=powers)
    combo_power.pack()

    label5 = tk.Label(root, text='Режим обработки данных в АС:')
    label5.pack()

    modes = ['индивидуальный', 'коллективный']
    combo_modes = ttk.Combobox(root, values=modes)
    combo_modes.pack()

    root.mainloop()


def main():
    prepare_data_from_order()
    prepare_data_from_guidance_document()
    create_window()


if __name__ == '__main__':
    main()
