'''Модуль создал Гурьянов Савелий Олегович 0304'''

import math
from random import randint, random


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
        descendants.append(generation[i] & (2 ** gap - 1) + partners[i] - partners[i] & (2 ** gap - 1))
        descendants.append(partners[i] & (2 ** gap - 1) + generation[i] - generation[i] & (2 ** gap - 1))
    return descendants


def mutate(sequence, credibility):
    for index in range(len(sequence)):
        if random() < credibility:
            print(f"{index} элемент мутировал")
            # Случайным образом выбирается ген мутации
            gene = randint(0, len(bin(sequence[index])) - 1)
            sequence[index] ^= 2 ** gene


coeffs = list(map(float, input("Введите коэффициенты (начиная от x^0, заканчивая x^9) через пробел:").split()))
interval = list(map(int, (input("Введите интервал (2 числа, сначала меньшее):").split())))
population = float(input("Введите густоту начальной популяции (от 0 до 1):"))
p_mutation = float(input("Введите вероятность мутации:"))
generation = list(range(math.floor(interval[0]), math.ceil(interval[1]), int(1/population)))
stop = 0
while not stop == 1:
    print(f"Поколение: {generation}")
    descendants = make_descendants(generation)
    print(f"Потомки: {descendants}")
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
    if credibility > 0.5:
        stop = 1
        # финальный результат
        final_result = result
        print(f"Наиболее вероятный минимум: {find_suitability(float(final_result), coeffs)}.")