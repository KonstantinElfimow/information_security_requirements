import tkinter as tk
from tkinter import ttk
import pandas as pd


def show_security_class(root: tk.Tk, *, significance_level: str, scale: str):
    if any(isinstance(child, tk.Text) for child in root.winfo_children()):
        for child in root.winfo_children():
            if isinstance(child, tk.Text):
                child.config(yscrollcommand=None)
                child.destroy()
                break

    text = tk.Text(root)
    text.pack(fill=tk.BOTH, expand=True)

    if significance_level not in ('УЗ 1', 'УЗ 2', 'УЗ 3') and scale not in ('Федеральный', 'Региональный', 'Объектовый'):
        text.insert(tk.END, "Введены неверные данные!")
    else:
        df = pd.read_csv('information_security_class.csv')
        security_class = df.loc[df['Уровень значимости информации'] == significance_level, scale].values[0]
        text.insert(tk.END, "Ваш класс защищённости: {}".format(security_class))


def create_window():
    root = tk.Tk()
    root.geometry('500x500')

    label1 = tk.Label(root, text="Выберите уровень значимости:")
    label1.pack()

    # Создание вертикального скролла
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    security_classes = ['УЗ 1', 'УЗ 2', 'УЗ 3']
    combo1 = ttk.Combobox(root, values=security_classes)
    combo1.pack()

    label2 = tk.Label(root, text="Выберите масштаб:")
    label2.pack()

    scales = ['Федеральный', 'Региональный', 'Объектовый']
    combo2 = ttk.Combobox(root, values=scales)
    combo2.pack()

    # label3 = tk.Label(root, text="Введите текст 3:")
    # label3.pack()
    #
    # entry3 = tk.Entry(root)
    # entry3.pack()

    button = tk.Button(root, text="Вывести текст", command=lambda: show_security_class(root, significance_level=combo1.get(),
                                                                                       scale=combo2.get()))
    button.pack()

    # button_next = tk.Button(root, text="Далее", command=next_form)
    # button_next.pack()

    root.mainloop()


# def next_form():
#     root = tk.Tk()
#
#     label = tk.Label(root, text="Новая форма")
#     label.pack()
#
#     button_back = tk.Button(root, text="Назад", command=root.destroy)
#     button_back.pack()
#
#     root.mainloop()


def main():
    create_window()


if __name__ == '__main__':
    main()
