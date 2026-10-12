# Задача 6.4
# Пользователь вводит строку. Замените все повторяющиеся подряд
# идущие символы на один и выведите результат.

text = input("Введите строку: ")

if len(text) == 0:
    result = ""
else:
    result = text[0]
    
    for i in range(1, len(text)):
        if text[i] != text[i - 1]:
            result += text[i]

print("Результат:", result)