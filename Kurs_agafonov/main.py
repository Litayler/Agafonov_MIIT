import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from scipy.optimize import linprog
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Квалиметрия
class QualityAssessment:
    def __init__(self, data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.aircrafts = json.load(f)
        
        
        self.weights = {
            'fuel_consumption': 0.4,  
            'max_speed': 0.2,         
            'engine_lifespan': 0.3,   
            'noise_level': 0.1        
        }

    def calculate_quality(self):
        results = []
        
        max_speed = max(a['max_speed'] for a in self.aircrafts)
        max_lifespan = max(a['engine_lifespan'] for a in self.aircrafts)
        min_fuel = min(a['fuel_consumption'] for a in self.aircrafts)
        min_noise = min(a['noise_level'] for a in self.aircrafts)

        for ac in self.aircrafts:
            # Оценка каждого параметра от 0 до 1 (1 - идеально)
            #значение / эталон
            q_speed = ac['max_speed'] / max_speed
            q_lifespan = ac['engine_lifespan'] / max_lifespan
            #эталон / значение
            q_fuel = min_fuel / ac['fuel_consumption']
            q_noise = min_noise / ac['noise_level']

            
            quality = (self.weights['fuel_consumption'] * q_fuel +
                       self.weights['max_speed'] * q_speed +
                       self.weights['engine_lifespan'] * q_lifespan +
                       self.weights['noise_level'] * q_noise)
            
            results.append({'name': ac['name'], 'quality': quality})
        
        return pd.DataFrame(results).sort_values(by='quality', ascending=False)

#Регрессия
class RevenuePredictor:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.model = None
        self.X_test = None
        self.y_test = None
        self.y_pred = None

    def train_model(self):
        
        X = self.df[['passenger_count', 'is_international', 'aircraft_age', 'distance_km', 'season_high']]
        y = self.df['revenue_per_flight']

        
        X_train, self.X_test, y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

       
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        
        self.y_pred = self.model.predict(self.X_test)

    def get_metrics(self):
        mse = mean_squared_error(self.y_test, self.y_pred)
        r2 = r2_score(self.y_test, self.y_pred)
        return mse, r2

    def predict_revenue(self, features):
        
        return self.model.predict([features])[0]

#Оптимизация
class FlightOptimizer:
    def __init__(self):
        # Данные из таблицы
        self.costs = np.array([
            [150, 200, 180, 220], # Хаб A
            [170, 160, 190, 210], # Хаб B
            [200, 180, 170, 190]  # Хаб C
        ])
        # Пропускная способность хабов
        self.supply = [20, 15, 10]
        # Спрос аэропортов
        self.demand = [12, 8, 14, 6]

    def solve(self):
        
        c = self.costs.flatten()

        #
        A_eq = []
        b_eq = []
        for j in range(len(self.demand)):
            row = [0] * 12
            for i in range(len(self.supply)):
                row[i * 4 + j] = 1
            A_eq.append(row)
            b_eq.append(self.demand[j])

       
        A_ub = []
        b_ub = []
        for i in range(len(self.supply)):
            row = [0] * 12
            for j in range(len(self.demand)):
                row[i * 4 + j] = 1
            A_ub.append(row)
            b_ub.append(self.supply[i])

        # Решение
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='highs')
        
        if res.success:
            return res.x.reshape((3, 4)), res.fun
        else:
            return None, None

#Графический интерфейс 
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Авиакомпания - Аналитическая система")
        self.root.geometry("1000x700")

        self.qa = QualityAssessment('data/aircraft_specs.json')
        self.rp = RevenuePredictor('data/Aviation.csv')
        self.rp.train_model()
        self.fo = FlightOptimizer()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.create_quality_tab()
        self.create_prediction_tab()
        self.create_optimization_tab()

    def create_quality_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Оценка качества')
        
        # Таблица с результатами
        df = self.qa.calculate_quality()
        tree = ttk.Treeview(frame, columns=('name', 'quality'), show='headings')
        tree.heading('name', text='Модель')
        tree.heading('quality', text='Уровень качества')
        for _, row in df.iterrows():
            tree.insert('', 'end', values=(row['name'], f"{row['quality']:.4f}"))
        tree.pack(fill='x', padx=10, pady=10)

        # График
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(df['name'], df['quality'], color='skyblue')
        ax.set_xlabel('Уровень качества')
        ax.set_title('Сравнение технического уровня самолетов')
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def create_prediction_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Прогноз выручки')

        # Поля ввода
        labels = ['Пассажиры', 'Международный (0/1)', 'Возраст', 'Дистанция', 'Высокий сезон (0/1)']
        self.entries = []
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append(entry)
        
        # Кнопка
        btn = ttk.Button(frame, text="Рассчитать прогноз", command=self.on_predict)
        btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

        # Результат
        self.result_label = ttk.Label(frame, text="", font=('Arial', 12))
        self.result_label.grid(row=len(labels)+1, column=0, columnspan=2)

        # мметрики
        mse, r2 = self.rp.get_metrics()
        metrics_text = f"MSE: {mse:.2f}\nR2: {r2:.2f}"
        ttk.Label(frame, text=metrics_text, font=('Arial', 10)).grid(row=len(labels)+2, column=0, columnspan=2, pady=10)

    def on_predict(self):
        try:
            features = [float(e.get()) for e in self.entries]
            prediction = self.rp.predict_revenue(features)
            self.result_label.config(text=f"Прогноз выручки: {prediction:.2f} тыс. руб.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проверьте ввод: {e}")

    def create_optimization_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Оптимизация рейсов')

        # Кнопка для расчета
        btn = ttk.Button(frame, text="Рассчитать оптимальный план", command=self.on_optimize)
        btn.pack(pady=10)

        # ттекстовое поле для вывода
        self.opt_text = tk.Text(frame, height=15, width=80)
        self.opt_text.pack(padx=10, pady=10)

    def on_optimize(self):
        plan, total_cost = self.fo.solve()
        if plan is None:
            self.opt_text.insert('1.0', "Решение не найдено.")
            return
        
        text = "Оптимальный план полетов (кол-во рейсов):\n"
        text += "        X   Y   Z   W\n"
        hubs = ['A', 'B', 'C']
        airports = ['X', 'Y', 'Z', 'W']
        for i, hub in enumerate(hubs):
            text += f"Хаб {hub}: "
            for j in range(4):
                text += f"{plan[i][j]:.0f}  "
            text += "\n"
        text += f"\nОбщие минимальные затраты: {total_cost:.2f}\n"
        self.opt_text.delete('1.0', 'end')
        self.opt_text.insert('1.0', text)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()