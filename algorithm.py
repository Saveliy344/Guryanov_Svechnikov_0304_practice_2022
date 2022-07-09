'''Модуль создал Гурьянов Савелий Олегович 0304'''

import math
from random import randint, random
import tkinter as tk
import tkinter.ttk as ttk


def find_suitability(value, coeffs):
    result = 0
    for i in range(10):
        result += coeffs[i] * value ** i
    return result


def make_descendants(generation):
    partners = []
    descendants = []
    for i in range(len(generation)):
        index = randint(0, len(generation) - 1)
        print(f"Для {i} элемента поколения случайно выбран {index} партнёр.")
        partners.append(generation[index])
    for i in range(len(generation)):
        # Максимальная длина в каждой из строк пары, записанных в двоичном виде
        max_length = max(len(bin(generation[i])), len(bin(partners[i])))
        # В случайном месте формируется разрыв хромосомы
        gap = randint(0, max_length)
        # В процессе кроссинговера формируются два потомка
        if generation[i] > 0 and partners[i] > 0:
            descendants.append(generation[i] & (2 ** gap - 1) + partners[i] - partners[i] & (2 ** gap - 1))
            descendants.append(partners[i] & (2 ** gap - 1) + generation[i] - generation[i] & (2 ** gap - 1))
        else:
            sign = 1 if (generation[i] + partners[i]) > 0 else -1
            descendants.append(sign * (generation[i] & (2 ** gap - 1) + partners[i] - partners[i] & (2 ** gap - 1)))
            descendants.append(sign * (partners[i] & (2 ** gap - 1) + generation[i] - generation[i] & (2 ** gap - 1)))
    return descendants


def mutate(sequence, credibility):
    for index in range(len(sequence)):
        if random() < credibility:
            print(f"{index} элемент мутировал")
            # Случайным образом выбирается ген мутации
            gene = randint(0, len(bin(sequence[index])) - 1)
            sequence[index] ^= 2 ** gene


def algorithm(accuracy, first_coeffs, interval, population, p_mutation):
    interval = (math.ceil(interval[0] / accuracy), math.floor(interval[1]) / accuracy)
    flag = 1
    coeffs = [first_coeffs[i] * accuracy ** i for i in range(len(first_coeffs))]
    if not (interval[0] < 0 and interval[1] > 0):
        if interval[0] < 0:
            if interval[1] <= 0:
                coeffs = [coeffs[index] * (-1) ** index for index in range(len(coeffs))]
                interval = (-interval[1], -interval[0])
                flag = -1
        generation = list(range(math.floor(interval[0]), math.ceil(interval[1]), int(math.ceil(1 / population))))
        stop = 0
        counter = 0
        prog_window = tk.Tk()
        prog_window.title('Визуализация')
        prog_window.configure(bg='white')
        main_frame = tk.Frame(prog_window, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=1)
        canvas = tk.Canvas(main_frame, bg='white')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview, bg='white')
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        population_frame = tk.Frame(canvas, background='white')
        canvas.create_window((0, 0), window=population_frame, anchor="center")
        while stop != 1 and counter != 1000:
            lbl1 = tk.Label(population_frame, text="Поколение", font=("Arial Bold", 30), bg='white', anchor=tk.CENTER)
            lbl1.pack()
            heads1 = ['Особь', 'Приспособленность']
            table1 = ttk.Treeview(population_frame, show='headings', height=4)
            table1['columns'] = heads1
            for header in heads1:
                table1.heading(header, text=header, anchor="center")
                table1.column(header, anchor="center")
            for row in ([el, find_suitability(el, coeffs)] for el in generation):
                table1.insert('', tk.END, values=row)
            table1.pack(expand=tk.YES, fill=tk.BOTH)
            print(f"Поколение: {generation}")
            descendants = make_descendants(generation)
            print(f"Потомки: {descendants}")
            print(descendants.count(1))
            mutate(descendants, p_mutation)
            sequence = generation + descendants
            print(f"Последовательность родителей и потомков: {sequence}")
            suitabilities = []  # расчёт приспособленностей
            for element in sequence:
                # удаляются элементы за пределами интервала
                if element < interval[0] or element > interval[1]:
                    sequence.remove(element)
                suitabilities.append(find_suitability(element, coeffs))
            suitabilities.sort(key=lambda x: x)
            suitabilities = suitabilities[:len(suitabilities) // 3 + len(suitabilities) % 3:]
            generation = []
            for element in sequence:
                result = find_suitability(element, coeffs)
                if result in suitabilities:
                    generation.append(element)
                    suitabilities.remove(result)
            c = dict()
            for element in sequence:
                c[str(element)] = c.get(str(element), 0) + 1
            result = max(c.items(), key=lambda item: item[1])[0]
            credibility = c[result] / len(sequence)
            # остановка - когда более 50% хромосом совпадают
            counter += 1
            if credibility > 0.5:
                stop = 1
                # финальный результат
                final_result = result
                print(f"Наиболее вероятный минимум: {find_suitability(float(flag * final_result), coeffs)} в точке "
                      f"{float(final_result) * accuracy}.")
                lbl2 = tk.Label(prog_window, text=f"Наиболее вероятный минимум: "
                                                  f"{find_suitability(float(final_result), coeffs)} в точке "
                                                  f"{float(flag * final_result) * accuracy}.",
                                font=("Arial Bold", 30), bg='white')
                lbl2.pack()
                prog_window.mainloop()
    else:
        save_coeffs = coeffs
        save_interval = interval
        coeffs = [coeffs[index] / (-1) ** index for index in range(len(coeffs))]
        interval = (0, -interval[0])
        generation = list(range(math.floor(interval[0]), math.ceil(interval[1]), int(math.ceil(1 / population))))
        stop = 0
        counter = 0
        prog_window = tk.Tk()
        prog_window.title('Визуализация')
        prog_window.configure(bg='white')
        main_frame = tk.Frame(prog_window, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=1)
        canvas = tk.Canvas(main_frame, bg='white')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview, bg='white')
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        population_frame = tk.Frame(canvas, background='white')
        canvas.create_window((0, 0), window=population_frame, anchor="center")
        while stop != 1 and counter != 1000:
            lbl1 = tk.Label(population_frame, text="Поколение", font=("Arial Bold", 30), bg='white', anchor=tk.CENTER)
            lbl1.pack()
            heads1 = ['Особь', 'Приспособленность']
            table1 = ttk.Treeview(population_frame, show='headings', height=4)
            table1['columns'] = heads1
            for header in heads1:
                table1.heading(header, text=header, anchor="center")
                table1.column(header, anchor="center")
            for row in ([el, find_suitability(el, coeffs)] for el in generation):
                table1.insert('', tk.END, values=row)
            table1.pack(expand=tk.YES, fill=tk.BOTH)
            print(f"Поколение: {generation}")
            descendants = make_descendants(generation)
            print(f"Потомки: {descendants}")
            print(descendants.count(1))
            mutate(descendants, p_mutation)
            sequence = generation + descendants
            print(f"Последовательность родителей и потомков: {sequence}")
            suitabilities = []  # расчёт приспособленностей
            for element in sequence:
                # удаляются элементы за пределами интервала
                if element < interval[0] or element > interval[1]:
                    sequence.remove(element)
                suitabilities.append(find_suitability(element, coeffs))
            suitabilities.sort(key=lambda x: x)
            suitabilities = suitabilities[:len(suitabilities) // 3 + len(suitabilities) % 3:]
            generation = []
            for element in sequence:
                result = find_suitability(element, coeffs)
                if result in suitabilities:
                    generation.append(element)
                    suitabilities.remove(result)
            c = dict()
            for element in sequence:
                c[str(element)] = c.get(str(element), 0) + 1
            result = max(c.items(), key=lambda item: item[1])[0]
            credibility = c[result] / len(sequence)
            # остановка - когда более 50% хромосом совпадают
            counter += 1
            if credibility > 0.5:
                stop = 1
                save_result = result
                save_value = find_suitability(float(save_result), coeffs)
        if counter == 1000:
            save_result = result
            save_value = find_suitability(float(save_result), coeffs)
        counter = 0
        stop = 0
        coeffs = save_coeffs
        interval = (0, save_interval[1])
        while stop != 1 and counter != 1000:
            lbl1 = tk.Label(population_frame, text="Поколение", font=("Arial Bold", 30), bg='white', anchor=tk.CENTER)
            lbl1.pack()
            heads1 = ['Особь', 'Приспособленность']
            table1 = ttk.Treeview(population_frame, show='headings', height=4)
            table1['columns'] = heads1
            for header in heads1:
                table1.heading(header, text=header, anchor="center")
                table1.column(header, anchor="center")
            for row in ([el, find_suitability(el, coeffs)] for el in generation):
                table1.insert('', tk.END, values=row)
            table1.pack(expand=tk.YES, fill=tk.BOTH)
            print(f"Поколение: {generation}")
            descendants = make_descendants(generation)
            print(f"Потомки: {descendants}")
            print(descendants.count(1))
            mutate(descendants, p_mutation)
            sequence = generation + descendants
            print(f"Последовательность родителей и потомков: {sequence}")
            suitabilities = []  # расчёт приспособленностей
            for element in sequence:
                # удаляются элементы за пределами интервала
                if element < interval[0] or element > interval[1]:
                    sequence.remove(element)
                suitabilities.append(find_suitability(element, coeffs))
            suitabilities.sort(key=lambda x: x)
            suitabilities = suitabilities[:len(suitabilities) // 3 + len(suitabilities) % 3:]
            generation = []
            for element in sequence:
                result = find_suitability(element, coeffs)
                if result in suitabilities:
                    generation.append(element)
                    suitabilities.remove(result)
            c = dict()
            for element in sequence:
                c[str(element)] = c.get(str(element), 0) + 1
            result = max(c.items(), key=lambda item: item[1])[0]
            credibility = c[result] / len(sequence)
            # остановка - когда более 50% хромосом совпадают
            counter += 1
            if credibility > 0.5:
                stop = 1
                # финальный результат
                final_result = result
                if find_suitability(float(final_result), coeffs) < save_value:
                    print(f"Наиболее вероятный минимум: {find_suitability(float(final_result), coeffs)} в точке "
                          f"{float(final_result) * accuracy}.")
                    lbl2 = tk.Label(prog_window, text=f"Наиболее вероятный минимум: "
                                                      f"{find_suitability(float(final_result), coeffs)} в точке "
                                                      f"{float(final_result) * accuracy}.",
                                    font=("Arial Bold", 30), bg='white')
                    lbl2.pack()
                else:
                    print(f"Наиболее вероятный минимум: {find_suitability(-float(save_result), coeffs)} в точке "
                          f"{-float(save_result) * accuracy}.")
                    lbl2 = tk.Label(prog_window, text=f"Наиболее вероятный минимум: "
                                                      f"{find_suitability(-float(save_result), coeffs)} в точке"
                                                      f" {-float(save_result) * accuracy}.",
                                    font=("Arial Bold", 30), bg='white')
                    lbl2.pack()
                prog_window.mainloop()
