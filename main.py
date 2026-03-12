from services.order_operations import (
    get_orders_sum_by_user,
    get_sold_products_count,
    all_orders_for_last_period
)
from services.product_operations import (
    create_product,
    get_products_by_category,
    get_available_categories
)
from services.purchase import purchase_creation


def show_menu():
    print("\nПродуктовий магазин\n")
    print("1. Додати новий товар на склад")
    print("2. Переглянути товари за категорією")
    print("3. Створити нове замовлення")
    print("4. Звіт: Статистика продажів (ТОП товарів)")
    print("5. Звіт: Сума покупок користувача")
    print("6. Звіт: Список оформлених замовлень за період")
    print("0. Вихід")
    print("=" * 30)


def interactive_purchase():
    """Helper function for interactive purchase"""
    user = input("Введіть ім'я покупця: ")
    basket = {}

    while True:
        prod_name = input("Назва товару (або 'ок' для закінчення оформлення): ").lower()
        if prod_name == 'ok' or prod_name == 'ок':
            break

        try:
            count = int(input(f"Кількість для '{prod_name}': "))
            if count <= 0:
                print("Кількість має бути більшою за 0")
                continue
            basket[prod_name] = basket.get(prod_name, 0) + count
        except ValueError:
            print("Будь ласка, введіть число")

    if basket:
        try:
            order = purchase_creation(user, basket)
            print(f"\nЗамовлення успішно створено!")
            print(f"Загальна сума: {order['total_price']} грн")
        except Exception as e:
            print(f"Помилка створення замовлення: {e}")
    else:
        print("Кошик порожній")


def main():
    while True:
        show_menu()
        choice = input("Оберіть пункт меню: ")

        try:
            if choice == "1":
                name = input("Назва товару: ")
                while True:
                    try:
                        price = float(input("Ціна: "))
                        count = int(input("Початкова кількість: "))
                        if price > 0 or count > 0:
                            break
                        print("Значення має бути більшим за 0")
                    except ValueError:
                        print("Будь ласка, введіть числове значення")
                category = input("Категорія: ")
                create_product(name, price, category, count)
                print(f"Товар '{name}' успішно додано")

            elif choice == "2":
                print("Список категорій")
                for cat in get_available_categories():
                    print(f"{cat}")
                category = input("Яка категорія вас цікавить? ")
                prods = get_products_by_category(category)
                print(f"\nТовари в категорії '{category}':")
                for prod in prods:
                    print(f"- {prod['name']}: {prod['price']} грн (в наявності: {prod['stock_count']})")

            elif choice == "3":
                interactive_purchase()

            elif choice == "4":
                days = int(input("За скільки останніх днів показати звіт? "))
                stats = get_sold_products_count(days)
                print(f"\nТОП продажів за останні {days} дн.:")
                for item in stats:
                    print(f"{item['product']}: {item['total_sold']} шт.")

            elif choice == "5":
                user = input("Введіть ім'я користувача для перевірки: ")
                total = get_orders_sum_by_user(user)
                if total:
                    print(f"Користувач {user} всього витратив: {total[0]['total_sum']} грн")
                else:
                    print("У цього користувача ще немає покупок")

            elif choice == "6":
                days = int(input("За скільки останніх днів показати замовлення? "))
                orders = all_orders_for_last_period(days)
                print(f"\nСписок замовлень за останні {days} дн.:")
                if not orders:
                    print("Замовлень не знайдено")
                for order in orders:
                    print(f"№{order['order_number']}\n"
                          f"Дата: {order['date']}\n"
                          f"Користувач: {order['user']}\n"
                          f"Сума: {order['total_price']} грн\n")

            elif choice == "0":
                print("Роботу завершено. Гарного дня!")
                break
            else:
                print("Невірний вибір. Спробуйте ще раз")

        except Exception as e:
            print(f"Сталася помилка: {e}")


if __name__ == '__main__':
    main()
