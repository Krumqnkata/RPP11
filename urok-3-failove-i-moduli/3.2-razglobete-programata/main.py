"""main.py — анализ на продажбите в училищния бюфет за една седмица.

Тук само се сглобява: chetene.py чете и записва, analiz.py смята,
а main.py печата. Изходът е същият като на vsichko.py.
"""
from pathlib import Path

import analiz
import chetene

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "prodazhbi.txt"
REPORT_FILE = HERE / "otchet.txt"


def main() -> None:
    """Чете продажбите, вика анализа и печата резултатите."""
    print("АНАЛИЗ НА ПРОДАЖБИТЕ В БЮФЕТА")
    try:
        lines = chetene.read_lines(DATA_FILE)
    except FileNotFoundError:
        print(f"Няма такъв файл: {DATA_FILE}")
        return

    sales, problems = analiz.parse_sales(lines)
    for problem in problems:
        print(f"  {problem}")
    print(f"Заредени {len(sales)} продажби, пропуснати {len(problems)} реда.")
    if not sales:
        print("Няма нито една валидна продажба — няма какво да се анализира.")
        return

    by_product = analiz.revenue_by(sales, "produkt")
    print("\nОБОРОТ ПО ПРОДУКТИ")
    for product, revenue in analiz.sorted_by_revenue(by_product):
        print(f"  {product:10s} {revenue:8.2f} лв.")

    by_day = analiz.revenue_by(sales, "data")
    print("\nОБОРОТ ПО ДНИ")
    for date in sorted(by_day):
        print(f"  {date}  {analiz.weekday_name(date):11s}{by_day[date]:8.2f} лв.")
    print(f"  Най-добър ден: {analiz.best_day(by_day)}")

    units = analiz.units_by_product(sales)
    best = analiz.best_seller(units)
    print(f"\nНАЙ-ПРОДАВАН ПРОДУКТ: {best} ({units[best]} бр.)")
    print(f"Средно продадени бройки на продукт: {analiz.average_units(units):.1f}")

    total = analiz.total_revenue(sales)
    print(f"\nОБЩ ОБОРОТ: {total:.2f} лв.")
    chetene.save_lines(REPORT_FILE, analiz.report_lines(total, by_product, by_day))
    print(f"Отчетът е записан в {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
