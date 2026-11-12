"""analiz.py — чистата логика за продажбите в бюфета.

Функциите тук само приемат и връщат данни. Не знаят нищо за файлове
и за печатане, затова могат да се проверят без нито един файл на диска.

Една продажба е речник: {"data": "2026-10-12", "produkt": "банан",
"broy": 14, "cena": 1.20}.
"""
import datetime

DAYS = ["понеделник", "вторник", "сряда", "четвъртък", "петък", "събота", "неделя"]
FIELDS_PER_LINE = 4


def parse_sales(lines: list) -> tuple:
    """Превръща редовете „дата | продукт | брой | цена“ в списък от продажби.

    Връща (продажби, проблеми). Празните редове и редовете с # се
    прескачат. Повреден ред не спира разбора: за него в „проблеми“
    се добавя съобщение с номера на реда.
    """
    sales, problems = [], []
    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != FIELDS_PER_LINE:
            problems.append(f"Ред {number}: очаквах {FIELDS_PER_LINE} полета, "
                            f"а са {len(parts)} — пропускам")
            continue
        date, product, count, price = parts
        try:
            sale = {"data": date, "produkt": product,
                    "broy": int(count), "cena": float(price)}
        except ValueError:
            problems.append(f"Ред {number}: '{count}' или '{price}' не е число — пропускам")
            continue
        sales.append(sale)
    return sales, problems


def revenue_by(sales: list, key: str) -> dict:
    """Оборотът, групиран по полето key ("produkt" или "data")."""
    result = {}
    for sale in sales:
        result[sale[key]] = result.get(sale[key], 0) + sale["broy"] * sale["cena"]
    return result


def sorted_by_revenue(revenue: dict) -> list:
    """Двойките (име, оборот), подредени от най-големия оборот към най-малкия."""
    return sorted(revenue.items(), key=lambda pair: -pair[1])


def weekday_name(date: str) -> str:
    """Денят от седмицата на български за дата във вида ГГГГ-ММ-ДД."""
    return DAYS[datetime.date.fromisoformat(date).weekday()]


def best_day(revenue_by_day: dict):
    """Датата с най-голям оборот; при равенство — по-ранната. None при липса на данни."""
    return max(sorted(revenue_by_day), key=revenue_by_day.get, default=None)


def units_by_product(sales: list) -> dict:
    """Колко броя са продадени от всеки продукт."""
    units = {}
    for sale in sales:
        units[sale["produkt"]] = units.get(sale["produkt"], 0) + sale["broy"]
    return units


def best_seller(units: dict):
    """Продуктът с най-много продадени бройки. None при липса на данни."""
    return max(units, key=units.get, default=None)


def average_units(units: dict) -> float:
    """Средно продадени бройки на продукт. 0, ако няма продукти."""
    if not units:
        return 0
    return sum(units.values()) / len(units)


def total_revenue(sales: list) -> float:
    """Общият оборот от всички продажби."""
    return sum(sale["broy"] * sale["cena"] for sale in sales)


def report_lines(total: float, by_product: dict, by_day: dict) -> list:
    """Редовете на седмичния отчет — готови за запис във файл."""
    lines = ["ОТЧЕТ ЗА СЕДМИЦАТА", f"Общ оборот: {total:.2f} лв.", "", "По продукти:"]
    for product, revenue in sorted_by_revenue(by_product):
        lines.append(f"  {product}: {revenue:.2f} лв.")
    lines += ["", "По дни:"]
    for date in sorted(by_day):
        lines.append(f"  {date}: {by_day[date]:.2f} лв.")
    return lines


if __name__ == "__main__":
    # Проверките работят, без на диска да има какъвто и да е файл.
    test_lines = [
        "# дата | продукт | брой | цена",
        "2026-10-12 | банан | 10 | 1.50",
        "",
        "2026-10-12 | вода | 4 | 1.00",
        "2026-10-13 | банан | 2 | 1.50",
        "2026-10-13 | вода | 18",              # 3 полета
        "2026-10-13 | сандвич | пет | 3.80",   # броят не е число
    ]
    test_sales, test_problems = parse_sales(test_lines)

    # 1. повредените редове се пропускат и се съобщават с номера си
    assert len(test_sales) == 3 and len(test_problems) == 2
    assert test_problems[0].startswith("Ред 6:") and test_problems[1].startswith("Ред 7:")
    # 2. оборот по продукти и по дни
    assert revenue_by(test_sales, "produkt") == {"банан": 18.0, "вода": 4.0}
    assert revenue_by(test_sales, "data") == {"2026-10-12": 19.0, "2026-10-13": 3.0}
    # 3. най-добър ден и ден от седмицата
    assert best_day(revenue_by(test_sales, "data")) == "2026-10-12"
    assert weekday_name("2026-10-12") == "понеделник"
    # 4. най-продаван продукт, средни бройки и общ оборот
    test_units = units_by_product(test_sales)
    assert best_seller(test_units) == "банан"
    assert average_units(test_units) == 8.0
    assert total_revenue(test_sales) == 22.0
    # 5. без нито една продажба нищо не гърми
    assert parse_sales([]) == ([], [])
    assert best_day({}) is None and best_seller({}) is None
    assert average_units({}) == 0 and total_revenue([]) == 0
    print("analiz.py: всички проверки минаха.")
