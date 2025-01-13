import numpy as np

# Функция для нормализации данных
def normalize(data):
    normalized_data = np.zeros_like(data, dtype=float)
    # Нормализация: год выпуска - максимизация, цена - минимизация
    normalized_data[:, 0] = (data[:, 0] - np.min(data[:, 0])) / (np.max(data[:, 0]) - np.min(data[:, 0]))
    normalized_data[:, 1] = (np.max(data[:, 1]) - data[:, 1]) / (np.max(data[:, 1]) - np.min(data[:, 1]))
    return normalized_data

# Функция для нахождения множества Парето
def find_pareto(data):
    pareto_set = []
    for i, point in enumerate(data):
        dominated = False
        for other in data:
            if all(other >= point) and any(other > point):
                dominated = True
                break
        if not dominated:
            pareto_set.append(i)
    return pareto_set

# Функция для метода последовательных уступок
def concession_method(data, k):
    # Сортируем по важности первого критерия (год выпуска)
    sorted_indices = np.argsort(-data[:, 0])
    sorted_data = data[sorted_indices]

    # Ищем по второму критерию среди оставшихся
    best_index = np.argmin(sorted_data[:, 1])
    return sorted_indices[best_index]

# Основная программа
if __name__ == "__main__":
    # Чтение данных из файла
    filename = "cars.txt"
    cars = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            cars.append((int(parts[0]), int(parts[1]), float(parts[2])))  # Номер, год выпуска, цена

    cars = np.array(cars)
    ids = cars[:, 0]
    data = cars[:, 1:]

    # Нормализация данных
    normalized_data = normalize(data)
    print("Нормализованные оценки автомобилей:")
    for i, norm_vals in zip(ids, normalized_data):
        print(f"Автомобиль {i}: Год выпуска: {norm_vals[0]:.2f}, Цена: {norm_vals[1]:.2f}")

    # Нахождение множества Парето
    pareto_indices = find_pareto(normalized_data)
    pareto_cars = ids[pareto_indices]
    print("\nМножество Парето (номера предложений):", pareto_cars)

    # Решение методом последовательных уступок
    k = 0.7
    best_car_index = concession_method(normalized_data, k)
    best_car_id = ids[best_car_index]
    print(f"\nЛучший автомобиль по методу последовательных уступок: {best_car_id}")
