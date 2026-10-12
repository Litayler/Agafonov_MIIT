# Задача 6.3
# Пользователь вводит строку. Посчитайте и выведите количество
# гласных букв (a, e, i, o, u) в строке — отдельно для строчных и заглавных букв.

text = input("Введите строку: ")


vowels_lower = "aeiou"
vowels_upper = "AEIOU"


lower_count = 0
upper_count = 0


for char in text:
    if char in vowels_lower:
        lower_count += 1
    elif char in vowels_upper:
        upper_count += 1

print("Результат:")
print("Строчные гласные (a, e, i, o, u):", lower_count)
print("Заглавные гласные (A, E, I, O, U):", upper_count)