import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RandomWalkApp:
    def __init__(self, master):
        self.master = master
        master.title("Симулятор случайных блужданий")
        master.geometry("600x700")

        # Стиль
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))

        # Создание виджетов
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для параметров
        params_frame = ttk.LabelFrame(self.master, text="Параметры блуждания")
        params_frame.pack(padx=10, pady=10, fill='x')

        # Измерения
        ttk.Label(params_frame, text="Количество измерений:").pack()
        self.dimensions_var = tk.IntVar(value=2)
        dimensions_combo = ttk.Combobox(params_frame, textvariable=self.dimensions_var, 
                                        values=[1, 2, 3], state="readonly", width=10)
        dimensions_combo.pack()

        # Количество шагов
        ttk.Label(params_frame, text="Количество шагов:").pack()
        self.steps_var = tk.IntVar(value=1000)
        steps_entry = ttk.Entry(params_frame, textvariable=self.steps_var, width=20)
        steps_entry.pack()

        # Кнопка запуска
        simulate_button = ttk.Button(params_frame, text="Смоделировать", command=self.simulate_walk)
        simulate_button.pack(pady=10)

        # Фрейм для результатов
        self.results_frame = ttk.LabelFrame(self.master, text="Результаты")
        self.results_frame.pack(padx=10, pady=10, fill='both', expand=True)

    def simulate_walk(self):
        # Очистка предыдущих результатов
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        try:
            # Параметры симуляции
            dimensions = self.dimensions_var.get()
            num_steps = self.steps_var.get()

            # Создание и симуляция блуждания
            walk = RandomWalk(num_steps, dimensions)
            path = walk.simulate()
            stats = walk.calculate_stats()

            # Отображение статистики
            self.display_stats(stats)

            # Создание графика
            self.create_plot(path, dimensions)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def display_stats(self, stats):
        # Вывод статистики
        stats_text = (
            f"Начальная позиция: {stats['start_position']}\n"
            f"Конечная позиция: {stats['final_position']}\n"
            f"Общее расстояние: {stats['total_distance']:.2f}"
        )
        ttk.Label(self.results_frame, text=stats_text, wraplength=500).pack(pady=10)

    def create_plot(self, path, dimensions):
        # Создание графика в зависимости от измерений
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if dimensions == 1:
            ax.plot(path)
            ax.set_title('Случайное блуждание в 1D')
            ax.set_xlabel('Шаг')
            ax.set_ylabel('Позиция')
        
        elif dimensions == 2:
            ax.plot(path[:, 0], path[:, 1])
            ax.set_title('Случайное блуждание в 2D')
            ax.set_xlabel('X координата')
            ax.set_ylabel('Y координата')
        
        elif dimensions == 3:
            fig = plt.figure(figsize=(6, 4))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(path[:, 0], path[:, 1], path[:, 2])
            ax.set_title('Случайное блуждание в 3D')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

        # Встраивание графика в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.results_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True)
        canvas.draw()

class RandomWalk:
    def __init__(self, num_steps=1000, dimensions=2):
        self.num_steps = num_steps
        self.dimensions = dimensions
        self.path = np.zeros((num_steps, dimensions))
    
    def simulate(self):
        steps = np.random.choice([-1, 1], size=(self.num_steps, self.dimensions))
        self.path = np.cumsum(steps, axis=0)
        return self.path
    
    def calculate_stats(self):
        final_position = self.path[-1]
        total_distance = np.linalg.norm(final_position)
        
        return {
            'start_position': self.path[0],
            'final_position': final_position,
            'total_distance': total_distance
        }

def main():
    root = tk.Tk()
    app = RandomWalkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()