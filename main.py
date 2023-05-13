import tkinter as tk
from tkinter import ttk
import pandas as pd


df_1 = pd.read_csv('information_security_class.csv', delimiter=';')
df_2 = pd.read_csv('security_class_requirements.csv', delimiter=';')


def show_security_class_requirements(root: tk.Tk, *, significance_level: str, scale: str):
    if any(isinstance(child, tk.Text) for child in root.winfo_children()):
        for child in root.winfo_children():
            if isinstance(child, tk.Text):
                child.destroy()
                break

    text = tk.Text(root)
    text.pack(fill=tk.BOTH, expand=True)

    if significance_level not in ('УЗ 1', 'УЗ 2', 'УЗ 3') and scale not in ('федеральный', 'региональный', 'объектовый'):
        text.insert(tk.END, 'Введены неверные данные!')
    else:
        security_class = df_1.loc[df_1['уровень_значимости'] == significance_level, scale].values[0]

        requirements = (df_2.loc[df_2[security_class] == 1, ['номер_меры', 'мера_защиты']]).to_string()
        text.insert(tk.END, 'Ваш класс защищённости:\n{}\nТребования к системе:\n{}'.format(security_class, requirements))


def create_window():
    root = tk.Tk()
    root.geometry('500x500')
    
    main_label = tk.Label(root, text='По приказу №17 ФСТЭК России\n')
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

    button = tk.Button(root, text='Вывести текст', command=lambda: show_security_class_requirements(root,
                                                                                                    significance_level=combo1.get(),
                                                                                                    scale=combo2.get()))
    button.pack()

    # button_next = tk.Button(root, text='Далее', command=next_form)
    # button_next.pack()

    root.mainloop()


# def next_form():
#     root = tk.Tk()
#
#     label = tk.Label(root, text='Новая форма')
#     label.pack()
#
#     button_back = tk.Button(root, text='Назад', command=root.destroy)
#     button_back.pack()
#
#     root.mainloop()


def main():
    create_window()


if __name__ == '__main__':
    main()
