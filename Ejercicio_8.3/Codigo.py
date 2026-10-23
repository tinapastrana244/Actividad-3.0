import math
import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox


# ---------------- Modelo ----------------
class FiguraGeometrica(ABC):
    @abstractmethod
    def volumen(self): ...

    @abstractmethod
    def superficie(self): ...


class Cilindro(FiguraGeometrica):
    def __init__(self, radio, altura):
        self.radio, self.altura = radio, altura

    def volumen(self):
        return math.pi * self.radio ** 2 * self.altura

    def superficie(self):
        return 2 * math.pi * self.radio * (self.radio + self.altura)


class Esfera(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio

    def volumen(self):
        return 4 / 3 * math.pi * self.radio ** 3

    def superficie(self):
        return 4 * math.pi * self.radio ** 2


class Piramide(FiguraGeometrica):
    """Pirámide de base cuadrada: apotema = altura de cada cara lateral."""

    def __init__(self, base, altura, apotema):
        self.base, self.altura, self.apotema = base, altura, apotema

    def volumen(self):
        return self.base ** 2 * self.altura / 3

    def superficie(self):
        return self.base ** 2 + 2 * self.base * self.apotema


class Cubo(FiguraGeometrica):
    def __init__(self, lado):
        self.lado = lado

    def volumen(self):
        return self.lado ** 3

    def superficie(self):
        return 6 * self.lado ** 2


class Prisma(FiguraGeometrica):
    def __init__(self, largo, ancho, altura):
        self.largo, self.ancho, self.altura = largo, ancho, altura

    def volumen(self):
        return self.largo * self.ancho * self.altura

    def superficie(self):
        return 2 * (self.largo * self.ancho + self.largo * self.altura + self.ancho * self.altura)


# ---------------- Dibujos (Canvas 150x150) ----------------
COLOR = "#1f4e79"      # trazos visibles
COLOR_OCULTO = "#7f9bb5"  # trazos ocultos (punteados)
TAM = 150


def _linea(c, puntos, oculta=False):
    """Dibuja una polilínea; las ocultas van punteadas y en tono claro."""
    if oculta:
        c.create_line(*puntos, fill=COLOR_OCULTO, dash=(4, 3))
    else:
        c.create_line(*puntos, fill=COLOR, width=2)


def _elipse(c, cx, cy, rx, ry, mitad=None):
    """Elipse completa o solo su mitad 'frontal'/'trasera' (para dar volumen)."""
    caja = (cx - rx, cy - ry, cx + rx, cy + ry)
    if mitad is None:
        c.create_oval(*caja, outline=COLOR, width=2)
    elif mitad == "frontal":
        c.create_arc(*caja, start=180, extent=180, style="arc", outline=COLOR, width=2)
    else:
        c.create_arc(*caja, start=0, extent=180, style="arc", outline=COLOR_OCULTO, dash=(4, 3))


def _caja(c, x, y, ancho, alto, prof):
    """Paralelepípedo en perspectiva oblicua con esquina frontal-inferior-izquierda en (x, y)."""
    dx, dy = prof * 0.5, prof * 0.5          # desplazamiento de la cara trasera
    f = [(x, y), (x + ancho, y), (x + ancho, y - alto), (x, y - alto)]       # cara frontal
    t = [(px + dx, py - dy) for px, py in f]                                 # cara trasera
    # aristas ocultas: las que salen de la esquina trasera-inferior-izquierda
    _linea(c, [*t[0], *t[1]], oculta=True)
    _linea(c, [*t[0], *t[3]], oculta=True)
    _linea(c, [*f[0], *t[0]], oculta=True)
    # aristas visibles
    _linea(c, [*f[0], *f[1], *f[2], *f[3], *f[0]])
    _linea(c, [*f[3], *t[3], *t[2], *t[1], *f[1]])
    _linea(c, [*f[2], *t[2]])


def dibujar_cilindro(c):
    cx, rx, ry = TAM / 2, 38, 12
    arriba, abajo = 28, 118
    _elipse(c, cx, arriba, rx, ry)
    _linea(c, [cx - rx, arriba, cx - rx, abajo])
    _linea(c, [cx + rx, arriba, cx + rx, abajo])
    _elipse(c, cx, abajo, rx, ry, "frontal")
    _elipse(c, cx, abajo, rx, ry, "trasera")


def dibujar_esfera(c):
    cx = cy = TAM / 2
    r = 56
    c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=COLOR, width=2)
    _elipse(c, cx, cy, r, 16, "frontal")      # ecuador
    _elipse(c, cx, cy, r, 16, "trasera")
    c.create_line(cx, cy, cx + r, cy, fill=COLOR, width=2)  # radio
    c.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, fill=COLOR, outline=COLOR)


def dibujar_piramide(c):
    # base cuadrada en perspectiva y vértice sobre su centro
    fl, fr = (25, 118), (95, 118)           # borde frontal de la base
    bl, br = (55, 92), (125, 92)            # borde trasero de la base
    cx = (fl[0] + br[0]) / 2
    cy = (fl[1] + br[1]) / 2
    apice = (cx, 18)
    _linea(c, [*bl, *br], oculta=True)
    _linea(c, [*fl, *bl], oculta=True)
    _linea(c, [*apice, *bl], oculta=True)
    _linea(c, [*fl, *fr, *br])
    for v in (fl, fr, br):
        _linea(c, [*apice, *v])
    # altura (punteada) desde el vértice hasta el centro de la base
    _linea(c, [*apice, cx, cy], oculta=True)


def dibujar_cubo(c):
    _caja(c, 22, 125, 70, 70, 50)


def dibujar_prisma(c):
    _caja(c, 14, 122, 88, 52, 44)


# ---------------- Interfaz ----------------
class VentanaFigura(tk.Toplevel):
    """Ventana genérica: recibe campos, clase de la figura y función de dibujo."""

    def __init__(self, padre, titulo, campos, clase, dibujo):
        super().__init__(padre)
        self.title(titulo)
        self.resizable(False, False)
        self.clase = clase
        self.entradas = []

        izq = tk.Frame(self, padx=15, pady=15)
        izq.pack(side="left")
        for fila, nombre in enumerate(campos):
            tk.Label(izq, text=f"{nombre} (cm):", anchor="w", width=14).grid(row=fila, column=0, pady=3)
            e = tk.Entry(izq, width=15)
            e.grid(row=fila, column=1, pady=3)
            self.entradas.append(e)
        tk.Button(izq, text="Calcular", width=14, command=self.calcular).grid(
            row=len(campos), column=1, pady=8)
        self.lbl_vol = tk.Label(izq, text="Volumen (cm3): ", anchor="w")
        self.lbl_vol.grid(row=len(campos) + 1, column=0, columnspan=2, sticky="w")
        self.lbl_sup = tk.Label(izq, text="Superficie (cm2): ", anchor="w")
        self.lbl_sup.grid(row=len(campos) + 2, column=0, columnspan=2, sticky="w")

        lienzo = tk.Canvas(self, width=150, height=150, bg="white")
        lienzo.pack(side="right", padx=15, pady=15)
        dibujo(lienzo)

    def calcular(self):
        try:
            valores = [float(e.get()) for e in self.entradas]
            if any(v <= 0 for v in valores):
                raise ValueError
            figura = self.clase(*valores)
        except ValueError:
            messagebox.showerror("Error", "Campo vacío, no numérico o no positivo.", parent=self)
            return
        self.lbl_vol.config(text=f"Volumen (cm3): {figura.volumen():.2f}")
        self.lbl_sup.config(text=f"Superficie (cm2): {figura.superficie():.2f}")


class VentanaPrincipal(tk.Tk):
    FIGURAS = [
        ("Cilindro", ["Radio", "Altura"], Cilindro, dibujar_cilindro),
        ("Esfera", ["Radio"], Esfera, dibujar_esfera),
        ("Pirámide", ["Base", "Altura", "Apotema"], Piramide, dibujar_piramide),
        ("Cubo", ["Lado"], Cubo, dibujar_cubo),
        ("Prisma", ["Largo", "Ancho", "Altura"], Prisma, dibujar_prisma),
    ]

    def __init__(self):
        super().__init__()
        self.title("Figuras geométricas")
        self.resizable(False, False)
        marco = tk.Frame(self, padx=20, pady=30)
        marco.pack()
        for nombre, campos, clase, dibujo in self.FIGURAS:
            tk.Button(marco, text=nombre, width=11,
                      command=lambda n=nombre, c=campos, k=clase, d=dibujo:
                      VentanaFigura(self, n, c, k, d)).pack(side="left", padx=5)


if __name__ == "__main__":
    VentanaPrincipal().mainloop()
