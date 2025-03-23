import tkinter as tk
from datetime import datetime, timedelta
import pytz

def obtener_horario_ny():
    tz_ny = pytz.timezone("America/New_York")
    ahora_ny = datetime.now(tz_ny)
    if ahora_ny.dst() != timedelta(0):  # Si está en horario de verano
        return (12, 30), (19, 0)
    else:
        return (13, 30), (20, 0)

def actualizar_tiempos():
    ahora = datetime.now(pytz.utc)
    bolsas["Nueva York"]["apertura"], bolsas["Nueva York"]["cierre"] = obtener_horario_ny()
    
    for bolsa, datos in bolsas.items():
        apertura_utc = ahora.replace(
            hour=datos['apertura'][0], minute=datos['apertura'][1], second=0, microsecond=0)
        cierre_utc = ahora.replace(
            hour=datos['cierre'][0], minute=datos['cierre'][1], second=0, microsecond=0)

        if ahora < apertura_utc:
            tiempo_restante = apertura_utc - ahora
            color_fondo = "#DE0606"  # Rojo si está cerrada
            color_texto = "#FFFF00"  # Amarillo
            mensaje = f"Abre en: {str(tiempo_restante).split('.')[0]}"
        elif apertura_utc <= ahora < cierre_utc:
            tiempo_restante = cierre_utc - ahora
            color_fondo = "#13d903"  # Verde si está abierta
            color_texto = "#FFFFFF"  # Blanco
            mensaje = f"Cierra en: {str(tiempo_restante).split('.')[0]}"
        else:
            apertura_siguiente = apertura_utc + timedelta(days=1)
            tiempo_restante = apertura_siguiente - ahora
            color_fondo = "#DE0606"  # Rojo si ya cerró
            color_texto = "#FFFF00"  # Amarillo
            mensaje = f"Abre en: {str(tiempo_restante).split('.')[0]}"

        etiquetas[bolsa].config(
            text=f"{bolsa}\n{mensaje}", bg=color_fondo, fg=color_texto)

    root.after(1000, actualizar_tiempos)

root = tk.Tk()
root.title("Horario de Bolsas")
root.configure(bg="#000000")

bolsas = {
    "Nueva York": {"apertura": (13, 30), "cierre": (20, 0)},  # Se actualizará dinámicamente
    "Londres": {"apertura": (8, 0), "cierre": (16, 30)},
    "Tokio": {"apertura": (0, 0), "cierre": (6, 0)},
    "Sídney": {"apertura": (22, 0), "cierre": (4, 0)}
}

etiquetas = {}
frame = tk.Frame(root, bg="#000000")
frame.pack(padx=20, pady=20)

for i, bolsa in enumerate(bolsas):
    etiqueta = tk.Label(frame, text=bolsa, font=("Arial", 14, "bold"), padx=15, pady=10, borderwidth=2, relief="solid")
    etiqueta.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
    etiquetas[bolsa] = etiqueta

actualizar_tiempos()
root.mainloop()
