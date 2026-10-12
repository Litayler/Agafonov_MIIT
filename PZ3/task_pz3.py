import matplotlib.pyplot as plt
import numpy as np

electric_scooters = {
    "Ninebot Max G30": {"Скорость": 30, "Запас хода": 65, "Мощность": 350, "Батарея": 15, "Нагрузка": 100},
    "Kugoo Kirin M5":  {"Скорость": 55, "Запас хода": 60, "Мощность": 1000, "Батарея": 21, "Нагрузка": 150},
    "Xiaomi Mi Pro 2": {"Скорость": 25, "Запас хода": 45, "Мощность": 300, "Батарея": 12.8, "Нагрузка": 100},
    "Halten RS-02":    {"Скорость": 40, "Запас хода": 50, "Мощность": 800, "Батарея": 18, "Нагрузка": 130}
}

models = list(electric_scooters.keys())
char_names = ["Скорость", "Запас хода", "Мощность", "Батарея", "Нагрузка"]

char_data = [[electric_scooters[m][c] for c in char_names] for m in models]

# ФУНКЦИИ ===

def get_normal(data):
    """Нормализация относительно первого образца (базового)"""
    base = data[0]
    return [[val / base[i] for i, val in enumerate(row)] for row in data]

def get_quality(normal_data):
    """Расчёт коэффициента Ks (среднее арифметическое)"""
    return [sum(row) / len(row) for row in normal_data]

def create_bar(names, values):
    """Гистограмма Ks"""
    best = names[np.argmax(values)]
    colors = ['gold' if m == best else 'skyblue' for m in names]
    
    plt.figure(figsize=(9, 5))
    bars = plt.bar(names, values, color=colors, edgecolor='black')
    plt.xlabel("Модель электросамоката", fontsize=12)
    plt.ylabel("Коэффициент Ks", fontsize=12)
    plt.title("Уровень технического совершенства\n(база - Ninebot Max G30)", fontsize=14)
    
    for bar, val in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                 f'{val:.3f}', ha='center', fontweight='bold')
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.show()

def create_radial(models, names, normal_data):
    """Лепестковая диаграмма для ВСЕХ моделей с адаптивным радиусом"""
    closed_data = [row + [row[0]] for row in normal_data]
    angles = np.linspace(0, 2 * np.pi, len(names), endpoint=False).tolist()
    angles += angles[:1]

    max_val = max(max(row) for row in normal_data)
    radius_limit = max_val * 1.2  # запас для визуального комфорта

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection="polar"))

    colors = ['blue', 'gold', 'green', 'red']
    
    for i in range(len(closed_data)):
        ax.plot(angles, closed_data[i], "o-", linewidth=2, 
                label=models[i], color=colors[i % len(colors)], markersize=6)
        ax.fill(angles, closed_data[i], alpha=0.1, color=colors[i % len(colors)])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(names, fontsize=10)
    
    ax.set_ylim(0, radius_limit)
    
    ax.set_yticks(np.linspace(0, radius_limit, 5))
    ax.set_yticklabels([f'{v:.1f}' for v in np.linspace(0, radius_limit, 5)], 
                       fontsize=8, color='gray')
    
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.05), fontsize=9)
    plt.title("Сравнение относительных характеристик всех моделей", pad=30, fontsize=14)
    plt.tight_layout()
    plt.show()

#РАСЧЁТЫ ===
normalized = get_normal(char_data)
ks_values = get_quality(normalized)

print("="*50)
print("РЕЗУЛЬТАТЫ РАСЧЕТА Ks")
print("="*50)
for m, k in zip(models, ks_values):
    print(f"{m}: {k:.3f}")

best_model = models[np.argmax(ks_values)]
print(f"\n✅ ЛУЧШИЙ САМОКАТ: {best_model} (Ks = {max(ks_values):.3f})")
print("="*50)

# ВИЗУАЛИЗАЦИЯ ===
create_bar(models, ks_values)
create_radial(models, char_names, normalized)