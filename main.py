import os
import wx
from gui.ventana_principal import VentanaPrincipal
from logica.base_datos import GestorBaseDatos

def asegurar_entorno():
    # Buscamos la ruta de la carpeta exacta donde está guardado este archivo main.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construimos la ruta a game_of_tasks/gui/img
    ruta_img = os.path.join(base_dir, "gui", "img")
    
    if not os.path.exists(ruta_img):
        os.makedirs(ruta_img)
        print(f"[SISTEMA] Se creó la carpeta faltante en: {ruta_img}")
        print("[SISTEMA] Recordá colocar la imagen 'avatar.png' dentro de ella para visualizarla en el perfil.")

def lanzar_aplicacion():
    # verificación e inicialización
    asegurar_entorno()
    
    # Inicializamos el motor gráfico de wxPython
    # False evita que redirija la salida de la terminal a una ventana flotante externa 
    app = wx.App(False) 
    
    print("[SISTEMA] Conectando con el Gestor de Base de Datos SQLite...")
    db = GestorBaseDatos() # crea las tablas si no existen
    
    print("[SISTEMA] Inicializando Ventana Principal (Game of Tasks)...")
    ventana = VentanaPrincipal(None, "Game of Tasks — Dashboard de Productividad", db)
    
    print("[SISTEMA] Aplicación corriendo con éxito.")
    app.MainLoop()

if __name__ == "__main__":
    # Esta condición asegura que el programa solo corra si se ejecuta directamente este archivo
    lanzar_aplicacion()