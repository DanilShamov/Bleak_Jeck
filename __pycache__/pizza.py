# Создаём модуль
def make_pizza(size, *toppings):
    """Выводит описание пиццы"""
    print(f" Делаем {size} см пиццу с следующими топингами:")
    for topping in toppings:
        print(topping)
