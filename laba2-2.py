def print_tableau(tableau):
    """
    Печатает текущую таблицу симплекс-метода.
    """
    for row in tableau:
        print("\t".join(f"{x:.2f}" for x in row))
    print()

def pivot_operation(tableau, pivot_row, pivot_col):
    """
    Выполняет операцию выбора опорного элемента (pivot) и пересчета таблицы.
    :param tableau: текущая симплекс-таблица
    :param pivot_row: индекс строки с опорным элементом
    :param pivot_col: индекс столбца с опорным элементом
    """
    pivot_value = tableau[pivot_row][pivot_col]

    # Делим всю строку на значение в опорном элементе
    tableau[pivot_row] = [x / pivot_value for x in tableau[pivot_row]]

    # Обновляем остальные строки
    for i, row in enumerate(tableau):
        if i != pivot_row:
            row_factor = row[pivot_col]
            tableau[i] = [x - row_factor * y for x, y in zip(row, tableau[pivot_row])]

def simplex_method():
    """
    Реализация симплекс-метода для задачи линейного программирования.
    Возвращает оптимальное решение и значение целевой функции.
    """
    # Коэффициенты целевой функции (Z = 60P1 + 40P2 + 50P3)
    c = [60, 40, 50]

    # Матрица ограничений
    A = [
        [3, 2, 0],  # Ограничение на сырье S1
        [2, 1, 4],  # Ограничение на сырье S2
        [4, 8, 4],  # Ограничение на сырье S3
    ]

    # Правая часть ограничений (запасы сырья)
    b = [900, 640, 1000]

    # Построение начальной симплекс-таблицы
    tableau = []

    # Добавляем строки ограничений с базисными переменными
    for i in range(len(A)):
        tableau.append(A[i] + [1 if i == j else 0 for j in range(len(A))] + [b[i]])


    # Добавляем строку целевой функции
    tableau.append([-x for x in c] + [0] * (len(A) + 1) + [0])

    # Печатаем начальную таблицу
    print("Начальная симплекс-таблица:")
    print_tableau(tableau)

    # Симплекс-алгоритм
    while True:
        # Шаг 1. Определяем столбец для ввода в базис (поиск минимального значения в последней строке)
        last_row = tableau[-1]
        pivot_col = min(range(len(last_row) - 1), key=lambda x: last_row[x])

        if last_row[pivot_col] >= 0:
            break  # Все коэффициенты в строке целевой функции >= 0, оптимум найден

        # Шаг 2. Определяем строку для исключения из базиса (метод минимального отношения)
        pivot_row = -1
        min_ratio = float("inf")

        for i in range(len(tableau) - 1):
            if tableau[i][pivot_col] > 0:
                ratio = tableau[i][-1] / tableau[i][pivot_col]
                if ratio < min_ratio:
                    min_ratio = ratio
                    pivot_row = i

        if pivot_row == -1:
            raise Exception("Задача не имеет конечного решения.")

        # Шаг 3. Выполняем операцию поворота
        pivot_operation(tableau, pivot_row, pivot_col)

        # Печатаем текущую таблицу
        print("Текущая симплекс-таблица:")
        print_tableau(tableau)

    # Оптимальное значение целевой функции
    optimal_value = tableau[-1][-1]

    # Найдем оптимальные значения переменных
    solution = [0] * len(c)
    for i in range(len(tableau) - 1):
        for j in range(len(c)):
            if tableau[i][j] == 1 and all(tableau[k][j] == 0 for k in range(len(tableau) - 1) if k != i):
                solution[j] = tableau[i][-1]

    return solution, optimal_value

# Запуск симплекс-метода
solution, optimal_value = simplex_method()

# Вывод результата
print("Оптимальное решение:")
print(f"P1 = {solution[0]:.2f}, P2 = {solution[1]:.2f}, P3 = {solution[2]:.2f}")
print(f"Максимальная прибыль: Z = {optimal_value:.2f}")