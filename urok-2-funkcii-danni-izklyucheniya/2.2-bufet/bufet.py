"""bufet.py — училищният бюфет: речници, функции и йерархия от изключения.

Задача 2.2: разширете модула с функциите от README.md на урока.
"""

STOCK = {
    "банан":   {"cena": 1.20, "kolichestvo": 10},
    "кроасан": {"cena": 2.50, "kolichestvo": 4},
    "вода":    {"cena": 0.90, "kolichestvo": 25},
    "сандвич": {"cena": 3.80, "kolichestvo": 0},
}


class BufetError(Exception):
    """Базово изключение на бюфета — всички останали наследяват него."""


class UnknownProduct(BufetError):
    pass


class NotEnoughStock(BufetError):
    def __init__(self, name, wanted, available):
        super().__init__(f"Искаш {wanted} бр. '{name}', а има само {available} бр.")
        self.name, self.wanted, self.available = name, wanted, available


def sell(stock: dict, name: str, quantity: int) -> float:
    """Продава quantity броя от name. Връща сумата."""
    if name not in stock:
        raise UnknownProduct(f"Няма продукт '{name}' в бюфета")
    if quantity <= 0:
        raise ValueError("Количеството трябва да е положително цяло число")
    item = stock[name]
    if item["kolichestvo"] < quantity:
        raise NotEnoughStock(name, quantity, item["kolichestvo"])
    item["kolichestvo"] -= quantity
    return round(item["cena"] * quantity, 2)


def receipt(stock: dict, order: list) -> tuple:
    """Обработва поръчка. Връща (сума, редове на бележката, проблеми)."""
    total, lines, problems = 0.0, [], []
    for name, quantity in order:
        try:
            price = sell(stock, name, quantity)
        except BufetError as err:
            problems.append(str(err))
        except ValueError as err:
            problems.append(f"Невалидно количество за '{name}': {err}")
        else:
            total += price
            lines.append(f"{name:10s} x{quantity:2d} = {price:6.2f} лв.")
    return round(total, 2), lines, problems


def low_stock(stock: dict, threshold: int = 5) -> list:
    """Имена на продуктите, които трябва да се доставят."""
    return sorted(name for name, item in stock.items()
                  if item["kolichestvo"] <= threshold)


TEACHER_DISCOUNT = 0.10  # 10% отстъпка за учители


class PriceError(BufetError):
    """Цената на продукт е нулева или отрицателна."""

    def __init__(self, name, cena):
        super().__init__(f"Невалидна цена {cena:.2f} лв. за '{name}': "
                         "цената трябва да е положителна")
        self.name, self.cena = name, cena


def deliver(stock: dict, name: str, quantity: int, cena=None) -> int:
    """Доставя quantity броя от name. Връща новата наличност.

    За нов продукт цената е задължителна: без цена вдига UnknownProduct,
    при цена <= 0 вдига PriceError. При quantity <= 0 вдига ValueError.
    Цената на вече съществуващ продукт не се променя.
    """
    if quantity <= 0:
        raise ValueError("Количеството трябва да е положително цяло число")
    if name not in stock:
        if cena is None:
            raise UnknownProduct(f"'{name}' е нов продукт — доставката му изисква цена")
        if cena <= 0:
            raise PriceError(name, cena)
        stock[name] = {"cena": cena, "kolichestvo": 0}
    stock[name]["kolichestvo"] += quantity
    return stock[name]["kolichestvo"]


def apply_discount(total: float, is_teacher: bool) -> float:
    """Връща сумата след отстъпката за учители, закръглена до стотинка."""
    if is_teacher:
        total = total * (1 - TEACHER_DISCOUNT)
    return round(total, 2)


def daily_report(stock: dict) -> dict:
    """Връща дневния отчет на бюфета като речник.

    "obshta_stoynost" — стойността на цялата наличност,
    "nay_skap"        — името на най-скъпия продукт (None при празен бюфет),
    "izcherpani"      — броят на продуктите с наличност 0.
    """
    total_value = sum(item["cena"] * item["kolichestvo"] for item in stock.values())
    most_expensive = max(stock, key=lambda name: stock[name]["cena"], default=None)
    sold_out = sum(1 for item in stock.values() if item["kolichestvo"] == 0)
    return {
        "obshta_stoynost": round(total_value, 2),
        "nay_skap": most_expensive,
        "izcherpani": sold_out,
    }


def delivery_result(stock: dict, name: str, quantity: int, cena=None) -> str:
    """Опитва доставка и връща ред за отчета — успех или причината за отказа."""
    try:
        available = deliver(stock, name, quantity, cena)
    except PriceError as err:
        return f"ОТКАЗАНА (цена {err.cena}): {err}"
    except UnknownProduct as err:
        return f"ОТКАЗАНА (непознат продукт): {err}"
    except ValueError as err:
        return f"ОТКАЗАНА (количество {quantity}) за '{name}': {err}"
    return f"приета: '{name}' +{quantity} бр., наличност {available} бр."


if __name__ == "__main__":
    order = [("банан", 2), ("кроасан", 1), ("сандвич", 1),
             ("пица", 1), ("вода", -3), ("вода", 2)]
    total, lines, problems = receipt(STOCK, order)

    print("КАСОВА БЕЛЕЖКА")
    for line in lines:
        print("  " + line)
    print(f"  ОБЩО: {total:.2f} лв.")

    if problems:
        print("\nНЕИЗПЪЛНЕНИ ПОЗИЦИИ:")
        for problem in problems:
            print(f"  - {problem}")

    print(f"\nЗА ДОСТАВКА: {', '.join(low_stock(STOCK))}")

    # ЗАДАЧА 2.2: сценарии с новите функции. Последните три доставки
    # предизвикват три различни изключения, но програмата продължава.
    deliveries = [
        ("сандвич", 8, None),      # 1. съществуващ продукт
        ("йогурт", 12, 1.60),      # 2. нов продукт с цена
        ("сок", 6, None),          # 3. нов продукт без цена -> UnknownProduct
        ("мляко", 10, -1.00),      # 4. отрицателна цена     -> PriceError
        ("банан", 0, None),        # 5. нулево количество    -> ValueError
    ]
    print("\nДОСТАВКИ")
    for name, quantity, cena in deliveries:
        print(f"  - {delivery_result(STOCK, name, quantity, cena)}")

    # 6. отстъпка за учител върху сумата от бележката
    print(f"\nСУМА ЗА УЧЕНИК: {apply_discount(total, False):.2f} лв.")
    print(f"СУМА ЗА УЧИТЕЛ: {apply_discount(total, True):.2f} лв.")

    # 7. дневен отчет
    report = daily_report(STOCK)
    print("\nДНЕВЕН ОТЧЕТ")
    print(f"  Стойност на наличността: {report['obshta_stoynost']:.2f} лв.")
    print(f"  Най-скъп продукт: {report['nay_skap']}")
    print(f"  Изчерпани продукти: {report['izcherpani']}")

    # 8. празен бюфет не чупи отчета
    print(f"  Отчет за празен бюфет: {daily_report({})}")
