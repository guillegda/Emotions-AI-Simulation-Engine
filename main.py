# main.py
from interface import InterfaceApp

if __name__ == "__main__":
    app = InterfaceApp()
    # Genera una ventana de texto
    # Esta ventana permite al usuario introducir un texto y que la API devuelva un texto formato json
    app.mainloop()