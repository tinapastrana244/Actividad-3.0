import math
import tkinter as tk
from tkinter import messagebox


class RegistroNotas:
    """Guarda cinco notas y calcula sus estadísticas."""

    def __init__(self, notas):
        self.notas = list(notas)

    def promedio(self):
        return sum(self.notas) / len(self.notas)

    def desviacion(self):
        p = self.promedio()
        return math.sqrt(sum((n - p) ** 2 for n in self.notas) / len(self.notas))

    def mayor(self):
        return max(self.notas)

    def menor(self):
        return min(self.notas)


class VentanaNotas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Notas del estudiante")
        self.resizable(False, False)
        self.entradas = []
        self._crear_widgets()

    def _crear_widgets(self):
        marco = tk.Frame(self, padx=20, pady=15)
        marco.pack()
        for i in range(5):
            tk.Label(marco, text=f"Nota {i + 1}:", anchor="w", width=10).grid(row=i, column=0, pady=3)
            e = tk.Entry(marco, width=18)
            e.grid(row=i, column=1, pady=3)
            self.entradas.append(e)

        botones = tk.Frame(marco)
        botones.grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(botones, text="Calcular", width=10, command=self.calcular).pack(side="left", padx=5)
        tk.Button(botones, text="Limpiar", width=10, command=self.limpiar).pack(side="left", padx=5)

        # Resultados en la parte inferior de la ventana
        self.lbl_prom = tk.Label(marco, text="Promedio: ", anchor="w", width=30)
        self.lbl_desv = tk.Label(marco, text="Desviación estándar: ", anchor="w", width=30)
        self.lbl_may = tk.Label(marco, text="Nota mayor: ", anchor="w", width=30)
        self.lbl_men = tk.Label(marco, text="Nota menor: ", anchor="w", width=30)
        for fila, lbl in enumerate((self.lbl_prom, self.lbl_desv, self.lbl_may, self.lbl_men), start=6):
            lbl.grid(row=fila, column=0, columnspan=2, pady=2)

    def calcular(self):
        notas = []
        for i, e in enumerate(self.entradas, start=1):
            texto = e.get().strip().replace(",", ".")
            if texto == "":
                messagebox.showwarning("Alerta", f"Falta la nota {i}. Las cinco notas son obligatorias.")
                e.focus()
                return
            try:
                notas.append(float(texto))
            except ValueError:
                messagebox.showerror("Error", f"La nota {i} no es un valor numérico.")
                e.focus()
                return
        r = RegistroNotas(notas)
        self.lbl_prom.config(text=f"Promedio: {r.promedio():.2f}")
        self.lbl_desv.config(text=f"Desviación estándar: {r.desviacion():.2f}")
        self.lbl_may.config(text=f"Nota mayor: {r.mayor():.1f}")
        self.lbl_men.config(text=f"Nota menor: {r.menor():.1f}")

    def limpiar(self):
        for e in self.entradas:
            e.delete(0, tk.END)
        for lbl, t in ((self.lbl_prom, "Promedio: "), (self.lbl_desv, "Desviación estándar: "),
                       (self.lbl_may, "Nota mayor: "), (self.lbl_men, "Nota menor: ")):
            lbl.config(text=t)


if __name__ == "__main__":
    VentanaNotas().mainloop()
