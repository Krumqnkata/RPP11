# Среден успех
# Програмата пита колко оценки има, после ги чете една по една
# и казва средния успех и с какво е.

n = int(input("Колко оценки имаш? "))
ocenki = []
for i in range(n):
    o = int(input("Оценка " + str(i + 1) + ": "))
    ocenki.append(o)

sredno = sum(ocenki) / n
print("Среден успех:", round(sredno, 2))

if sredno >= 5.50:
    print("Отличен")
elif sredno >= 4.50:
    print("Много добър")
elif sredno >= 3.50:
    print("Добър")
elif sredno >= 3:
    print("Среден")
else:
    print("Слаб")
