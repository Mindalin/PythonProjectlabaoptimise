import numpy as np

# Функция для поиска симплекс-решения
def simplex_method(c, A, b):
    # Количество переменных и ограничений
    n_variables = len(c)
    n_constraints = len(b)

    # Создаем симплекс-таблицу
    tableau = np.zeros((n_constraints + 1, n_variables + n_constraints + 1))

    # Заполняем таблицу коэффициентами
    tableau[:-1, :n_variables] = A
    tableau[:-1, n_variables:n_variables + n_constraints] = np.eye(n_constraints)
    tableau[:-1, -1] = b
    tableau[-1, :n_variables] = -c

    while True:
        # Проверка на оптимальность (если все коэффициенты в последней строке >= 0)
        if all(tableau[-1, :-1] >= 0):
            break

        # Находим разрешающий столбец (индекс минимального элемента в последней строке)
        pivot_col = np.argmin(tableau[-1, :-1])

        # Находим разрешающую строку по критерию минимального отношения
        ratios = []
        for i in range(n_constraints):
            if tableau[i, pivot_col] > 0:
                ratios.append(tableau[i, -1] / tableau[i, pivot_col])
            else:
                ratios.append(float('inf'))

        pivot_row = np.argmin(ratios)

        # Если нет допустимых решений
        if ratios[pivot_row] == float('inf'):
            raise ValueError("Задача не имеет допустимого решения.")

        # Выполняем преобразование строки
        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row] /= pivot_element

        for i in range(n_constraints + 1):
            if i != pivot_row:
                tableau[i] -= tableau[i, pivot_col] * tableau[pivot_row]

    # Возвращаем оптимальное значение функции и значения переменных
    solution = np.zeros(n_variables)
    for i in range(n_constraints):
        basic_var = np.where(tableau[i, :n_variables] == 1)[0]
        if len(basic_var) == 1:
            solution[basic_var[0]] = tableau[i, -1]

    optimal_value = tableau[-1, -1]
    return optimal_value, solution

# Пример ввода
if __name__ == "__main__":
    # Коэффициенты целевой функции (цель: максимизация)
    c = np.array([60, 40, 50])  # 3x1 + 2x2 + 4x3

    # Коэффициенты ограничений
    A = np.array([
        [3, 2, 0],
        [2, 1, 5],
        [4, 8, 4]
    ])

    # Правая часть ограничений
    b = np.array([900, 640, 1000])

    optimal_value, solution = simplex_method(c, A, b)
    print(f"Оптимальное значение функции: {optimal_value}")
    print(f"Значения переменных: {solution}")

