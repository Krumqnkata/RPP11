"""ariane.py — полетът, който можеше да не завърши така.

Опростен модел на това, което се случва на борда на Ariane 5.
Задача 2.1: следвайте стъпките в README.md на урока.
"""

INT16_MIN = -32_768
INT16_MAX = 32_767
INT32_MIN = -2_147_483_648
INT32_MAX = 2_147_483_647

# Трите режима на поведение при препълване (стъпки 2, 3 и 4).
MODE_STOP = "stop"      # без прехващане: изключението спира полета
MODE_CLAMP = "clamp"    # стойността се ограничава до границата на 16 бита
MODE_WIDEN = "int32"    # преминаване към 32-битово цяло число
MODES = (MODE_STOP, MODE_CLAMP, MODE_WIDEN)


class OverflowAlarm(Exception):
    """Собствено изключение: стойността не се побира в bits бита."""

    def __init__(self, value, bits=16):
        super().__init__(f"Стойност {value:.1f} не се побира в {bits}-битово цяло")
        self.value = value
        self.bits = bits


def to_int16(value: float) -> int:
    """Преобразува 64-битово дробно число към 16-битово цяло със знак.

    Ако стойността е извън диапазона INT16_MIN..INT16_MAX,
    вдига OverflowAlarm.
    """
    if not INT16_MIN <= value <= INT16_MAX:
        raise OverflowAlarm(value)
    return int(value)


def to_int32(value: float) -> int:
    """Преобразува дробно число към 32-битово цяло със знак.

    Ако стойността е извън диапазона INT32_MIN..INT32_MAX,
    вдига OverflowAlarm с bits=32.
    """
    if not INT32_MIN <= value <= INT32_MAX:
        raise OverflowAlarm(value, bits=32)
    return int(value)


def clamp_to_int16(value: float) -> int:
    """Връща най-близката граница на 16-битовия диапазон за препълнена стойност."""
    return INT16_MAX if value > 0 else INT16_MIN


def convert(bh: float, mode: str) -> tuple:
    """Преобразува BH за автопилота според режима.

    Връща (стойност, предупреждение). Предупреждението е None, когато
    стойността се побира в 16 бита. В режим MODE_STOP препълването
    не се обработва и OverflowAlarm продължава нагоре.
    """
    try:
        return to_int16(bh), None
    except OverflowAlarm as alarm:
        if mode == MODE_CLAMP:
            return clamp_to_int16(alarm.value), f"{alarm} — ограничавам до границата"
        if mode == MODE_WIDEN:
            return to_int32(alarm.value), f"{alarm} — преминавам към 32 бита"
        raise


def horizontal_bias(t: float, acceleration: float) -> float:
    """Опростен модел на хоризонталното отклонение BH след t секунди."""
    return 0.5 * acceleration * t * t


def flight(rocket: str, acceleration: float, duration: int,
           mode: str = MODE_STOP) -> None:
    """Симулира полет от duration секунди и печата какво стига до автопилота."""
    if mode not in MODES:
        raise ValueError(f"Непознат режим '{mode}'. Възможни: {', '.join(MODES)}")
    print(f"\n--- Полет на {rocket} (режим: {mode}) ---")
    for t in range(1, duration + 1):
        bh = horizontal_bias(t, acceleration)
        value, warning = convert(bh, mode)
        if warning:
            print(f"  ВНИМАНИЕ: {warning}")
        print(f"  t={t:2d}s  BH={bh:10.1f}  -> към автопилота: {value}")
    print("  Полетът завърши успешно.")


if __name__ == "__main__":
    flight("Ariane 4", acceleration=45.0, duration=10)
    flight("Ariane 5", acceleration=900.0, duration=10, mode=MODE_CLAMP)
    flight("Ariane 5", acceleration=900.0, duration=10, mode=MODE_WIDEN)
    try:
        flight("Ariane 5", acceleration=900.0, duration=10, mode=MODE_STOP)
    except OverflowAlarm as alarm:
        print(f"  ПОЛЕТЪТ Е ПРЕКРАТЕН: {alarm}")
