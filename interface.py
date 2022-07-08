from tkinter import Tk, Label, Button, Entry, messagebox

from algorithm import algorithm

GLOBAL_DATA = {}


def find_global_minimum():
    data = {}
    try:
        first_coeffs = list(map(float, (Ent_0.get(), Ent_1.get(), Ent_2.get(), Ent_3.get(), Ent_4.get(), Ent_5.get(),
                                        Ent_6.get(), Ent_7.get(), Ent_8.get(), Ent_9.get())))
    except ValueError:
        messagebox.showinfo("Ошибка ввода коэффициентов", "Все коэффициенты должны быть числами.")
        return
    try:
        interval = (int(Ent_10a.get()), int(Ent_10b.get()))
    except ValueError:
        messagebox.showinfo("Ошибка ввода интервала", "Неверно введён интервал.")
        return
    try:
        accuracy = float(Ent_13.get())
    except ValueError:
        messagebox.showinfo("Ошибка ввода точности", "Точность должна быть числом.")
        return
    try:
        p_mutation = float(Ent_11.get())
    except ValueError:
        messagebox.showinfo("Ошибка ввода вероятности мутации", "Вероятность мутации должна быть числом.")
        return
    try:
        population = float(Ent_12.get())
    except ValueError:
        messagebox.showinfo("Ошибка ввода густоты популяции", "Густота популяции должна быть числом.")
        return
    if accuracy < 0 or accuracy > 1:
        messagebox.showinfo("Ошибка точности", "Точность должна принимать значение от 0 до 1.")
        return
    if interval[0] >= interval[1]:
        messagebox.showinfo("Неправильный интервал", "Левое значение интервала должно быть меньше правого.")
        return
    if population < 0 or population > 1:
        messagebox.showinfo("Ошибка гусоты популяции", "Гусотота популяции должна принимать значение от 0 до 1.")
        return
    data["first_coeffs"] = first_coeffs
    data["interval"] = interval
    data["accuracy"] = accuracy
    data["p_mutation"] = p_mutation
    data["population"] = population
    algorithm(**data)


window = Tk()
window.title("Into")
lbl = Label(window, text="Ввод Данных", font=("Arial Bold", 30))
lbl_0 = Label(window, text="a0", font=("Arial Bold", 25))
lbl_1 = Label(window, text="a1", font=("Arial Bold", 25))
lbl_2 = Label(window, text="a2", font=("Arial Bold", 25))
lbl_3 = Label(window, text="a3", font=("Arial Bold", 25))
lbl_4 = Label(window, text="a4", font=("Arial Bold", 25))
lbl_5 = Label(window, text="a5", font=("Arial Bold", 25))
lbl_6 = Label(window, text="a6", font=("Arial Bold", 25))
lbl_7 = Label(window, text="a7", font=("Arial Bold", 25))
lbl_8 = Label(window, text="a8", font=("Arial Bold", 25))
lbl_9 = Label(window, text="a9", font=("Arial Bold", 25))
lbl_10a = Label(window, text="Интервал Поиска", font=("Arial Bold", 25))
lbl_10b = Label(window, text="-", font=("Arial Bold", 25))
lbl_11 = Label(window, text="Вероятность Мутации", font=("Arial Bold", 25))
lbl_12 = Label(window, text="Густота популяции", font=("Arial Bold", 25))
lbl_13 = Label(window, text="Точность нахождения минимума", font=("Arial Bold", 25))
btn_1 = Button(window, text="Через Файл", font=("Arial", 20), width=20, height=1)
btn_2 = Button(window, text="Через Графический Интерфейс", font=("Arial", 20), width=30, height=1)
btn_3 = Button(window, text="Найти Глобальный Минимум", font=("Arial Bold", 20), width=30, height=1,
               command=find_global_minimum)
Ent_0 = Entry(window)
Ent_1 = Entry(window)
Ent_2 = Entry(window)
Ent_3 = Entry(window)
Ent_4 = Entry(window)
Ent_5 = Entry(window)
Ent_6 = Entry(window)
Ent_7 = Entry(window)
Ent_8 = Entry(window)
Ent_9 = Entry(window)
Ent_10a = Entry(window)
Ent_10b = Entry(window)
Ent_11 = Entry(window)
Ent_12 = Entry(window)
Ent_13 = Entry(window)

lbl.grid(row=0, column=0, columnspan=7)

btn_1.grid(row=2, column=0, columnspan=3, stick='e')
btn_2.grid(row=2, column=3, columnspan=5)
btn_3.grid(row=15, column=0, columnspan=7)

lbl_0.grid(row=3, column=0)
lbl_1.grid(row=4, column=0)
lbl_2.grid(row=5, column=0)
lbl_3.grid(row=6, column=0)
lbl_4.grid(row=7, column=0)
lbl_5.grid(row=3, column=2, stick="e")
lbl_6.grid(row=4, column=2, stick="e")
lbl_7.grid(row=5, column=2, stick="e")
lbl_8.grid(row=6, column=2, stick="e")
lbl_9.grid(row=7, column=2, stick="e")
lbl_10a.grid(row=3, column=4, columnspan=3, stick="we")
lbl_10b.grid(row=4, column=5)
lbl_11.grid(row=5, column=4, columnspan=3)
lbl_12.grid(row=7, column=4, columnspan=3)
lbl_13.grid(row=9, column=4, columnspan=3)

Ent_0.grid(row=3, column=1, stick="w")
Ent_1.grid(row=4, column=1, stick="w")
Ent_2.grid(row=5, column=1, stick="w")
Ent_3.grid(row=6, column=1, stick="w")
Ent_4.grid(row=7, column=1, stick="w")
Ent_5.grid(row=3, column=3, stick="w")
Ent_6.grid(row=4, column=3, stick="w")
Ent_7.grid(row=5, column=3, stick="w")
Ent_8.grid(row=6, column=3, stick="w")
Ent_9.grid(row=7, column=3, stick="w")
Ent_10a.grid(row=4, column=4)
Ent_10b.grid(row=4, column=6)
Ent_11.grid(row=6, column=4, columnspan=3)
Ent_12.grid(row=8, column=4, columnspan=3)
Ent_13.grid(row=10, column=4, columnspan=3)

window.mainloop()
