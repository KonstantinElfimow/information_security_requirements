import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import csv

# url = 'https://fstec.ru/dokumenty/vse-dokumenty/prikazy/prikaz-fstek-rossii-ot-11-fevralya-2013-g-n-17'
#
# headers = {
#     'accept': '*/*',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
#                   'YaBrowser/23.3.1.895 Yowser/2.5 Safari/537.36 '
# }
#
# # Отключение проверки сертификата SSL
# requests.packages.urllib3.disable_warnings()
# req = requests.get(url, headers=headers, verify=False)
# src = req.text
#
# with open('index.html', mode='w', encoding='utf-8') as file:
#     file.write(src)

with open('index.html', mode='r', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'html.parser')

# all_rows = soup.find_all(class_='mzr-tc-group-item-href')

df_1 = pd.read_csv('information_security_class.csv', delimiter=';')
df_2 = pd.read_csv('security_class_requirements.csv', delimiter=';')


def show_security_class_requirements(*, significance_level: str, scale: str):
    root = tk.Tk()
    root.geometry('1000x1000')

    label = tk.Label(root, text='Требования по приказу №17 ФСТЭК России')
    label.pack()

    text = tk.Text(root)
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Создание вертикального скролла
    scrollbar = tk.Scrollbar(root, command=text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Связывание скролла с текстовым полем
    text.config(yscrollcommand=scrollbar.set)

    if significance_level not in ('УЗ 1', 'УЗ 2', 'УЗ 3') and scale not in (
            'федеральный', 'региональный', 'объектовый'):
        text.insert(tk.END, 'Введены неверные данные!')
    else:
        security_class = df_1.loc[df_1['уровень_значимости'] == significance_level, scale].values[0]
        requirements = (df_2.loc[df_2[security_class] == 1, ['номер_меры', 'мера_защиты']]).to_string()
        text.insert(tk.END,
                    'Ваш класс защищённости:\n{}\nТребования к системе:\n{}'.format(security_class, requirements))

    button_back = tk.Button(root, text='Назад', command=root.destroy)
    button_back.pack()

    root.mainloop()


def create_window():
    root = tk.Tk()
    root.geometry('500x300')

    main_label = tk.Label(root, text='Информационная система')
    main_label.pack()

    label1 = tk.Label(root, text='Выберите уровень значимости:')
    label1.pack()

    # Создание вертикального скролла
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    significance_levels = ['УЗ 1', 'УЗ 2', 'УЗ 3']
    combo1 = ttk.Combobox(root, values=significance_levels)
    combo1.pack()

    label2 = tk.Label(root, text='Выберите масштаб:')
    label2.pack()

    scales = ['федеральный', 'региональный', 'объектовый']
    combo2 = ttk.Combobox(root, values=scales)
    combo2.pack()

    button = tk.Button(root, text='Вывести требования',
                       command=lambda: show_security_class_requirements(significance_level=
                                                                        combo1.get(),
                                                                        scale=combo2.get()))
    button.pack()

    root.mainloop()


def main():
    create_window()


if __name__ == '__main__':
    main()
