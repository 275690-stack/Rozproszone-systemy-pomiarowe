import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Dodaliśmy ?limit=100, aby API domyślnie zwracało większą liczbę pomiarów
API_URL = "http://localhost:5001/measurements?limit=100"

class MeasurementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor Pomiarów: Temperatura i Ciśnienie")
        self.root.geometry("900x800") 

        # Przycisk do odświeżania danych
        self.refresh_btn = tk.Button(
            self.root, 
            text="Odśwież dane i wykresy", 
            command=self.update_plots, 
            font=("Arial", 12, "bold"), 
            bg="#4CAF50", 
            fg="white"
        )
        self.refresh_btn.pack(pady=10)

        # Tworzymy figurę z dwoma wykresami
        self.fig, (self.ax_temp, self.ax_press) = plt.subplots(2, 1, figsize=(9, 7), dpi=100)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Pierwsze pobranie danych
        self.update_plots()

    def fetch_data(self):
        """Pobiera dane z REST API backendu Flask."""
        try:
            response = requests.get(API_URL, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Błąd połączenia", f"Nie można pobrać danych z API:\n{e}")
            return []

    def update_plots(self):
        """Rozdziela dane i aktualizuje oba wykresy."""
        data = self.fetch_data()
        
        if not data:
            return

        # Odwracamy kolejność, aby czas szedł od lewej do prawej
        data.reverse()

        temp_times, temp_values = [], []
        press_times, press_values = [], []

        for row in data:
            timestamp = row.get("ts_ms") / 1000.0
            dt_object = datetime.fromtimestamp(timestamp)
            sensor_type = str(row.get("sensor")).lower()

            if "temp" in sensor_type:
                temp_times.append(dt_object)
                temp_values.append(row.get("value"))
            elif "press" in sensor_type or "ciśn" in sensor_type:
                press_times.append(dt_object)
                press_values.append(row.get("value"))

        # Czyszczenie starych wykresów
        self.ax_temp.clear()
        self.ax_press.clear()

        # --- WYKRES 1: TEMPERATURA ---
        if temp_times:
            self.ax_temp.plot(temp_times, temp_values, marker='o', linestyle='-', color='#d32f2f', label='Temperatura (°C)')
        
        self.ax_temp.set_title("Historia Pomiarów Temperatury", fontsize=12, fontweight='bold', color='#d32f2f')
        self.ax_temp.set_xlabel("Czas pomiaru (GG:MM:SS)", fontsize=10)
        self.ax_temp.set_ylabel("Wartość (°C)", fontsize=10)
        self.ax_temp.grid(True, linestyle='--', alpha=0.5)
        self.ax_temp.legend(loc="upper left")
        
        # Formatowanie czasu na osi X (GG:MM:SS)
        self.ax_temp.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        # --- WYKRES 2: CIŚNIENIE ---
        if press_times:
            self.ax_press.plot(press_times, press_values, marker='s', linestyle='-', color='#1976D2', label='Ciśnienie (hPa)')
        
        self.ax_press.set_title("Historia Pomiarów Ciśnienia", fontsize=12, fontweight='bold', color='#1976D2')
        self.ax_press.set_xlabel("Czas pomiaru (GG:MM:SS)", fontsize=10)
        self.ax_press.set_ylabel("Wartość (hPa)", fontsize=10)
        self.ax_press.grid(True, linestyle='--', alpha=0.5)
        self.ax_press.legend(loc="upper left")
        
        # Formatowanie czasu na osi X (GG:MM:SS)
        self.ax_press.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        # KLUCZOWA POPRAWKA: Wyłączenie zapisu naukowego i offsetu na osi Y (dla obu wykresów)
        self.ax_temp.ticklabel_format(style='plain', useOffset=False, axis='y')
        self.ax_press.ticklabel_format(style='plain', useOffset=False, axis='y')

        # Automatyczne obracanie etykiet czasu pod kątem, żeby się nie pokrywały
        self.fig.autofmt_xdate()
        
        # Zapobieganie nakładaniu się elementów wykresów
        self.fig.tight_layout()

        # Odświeżenie płótna
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MeasurementApp(root)
    root.mainloop()