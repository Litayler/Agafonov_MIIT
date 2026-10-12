# Задача 6.5
# Пользователь вводит два слова. Проверьте, являются ли они анаграммами друг друга (состоят из одних и тех же букв в разном порядке).

word1 = input("Введите первое слово: ")
word2 = input("Введите второе слово: ")

word1_lower = word1.lower()
word2_lower = word2.lower()


is_anagram = sorted(word1_lower) == sorted(word2_lower)

print(is_anagram)

