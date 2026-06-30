import sqlite3

class GestorBaseDatos:
    def __init__(self, nombre_db="misiones.db"):
        self.nombre_db = nombre_db
        self.crear_tabla()

    def conectar(self):
        """Crea y retorna la conexión a la base de datos"""
        return sqlite3.connect(self.nombre_db)

    def crear_tabla(self):
        """Crea la tabla de misiones """
        conexion = self.conectar()
        cursor = conexion.cursor()
        
        # agregamos la columna 'dificultad' text para que coincida con logica/mision.py
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS misiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarea TEXT NOT NULL,
                fecha_limite TEXT,
                recompensa INTEGER,
                estado TEXT DEFAULT 'activa',
                dificultad TEXT DEFAULT 'Media'
            )
        ''')
        conexion.commit()
        conexion.close()

    def agregar_mision(self, tarea, fecha_limite, recompensa, dificultad="Media", estado="activa"):
        """Guarda una nueva misión con todos sus atributos en la base de datos"""
        conexion = self.conectar()
        cursor = conexion.cursor()
        
        cursor.execute('''
            INSERT INTO misiones (tarea, fecha_limite, recompensa, dificultad, estado) 
            VALUES (?, ?, ?, ?, ?)
        ''', (tarea, fecha_limite, recompensa, dificultad, estado))
        
        conexion.commit()
        conexion.close()

    def obtener_todas(self):
        """Recupera todas las misiones guardadas"""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM misiones")
        datos = cursor.fetchall()
        conexion.close()
        return datos
    
    def obtener_activas(self):
        """Recupera solo las activas"""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM misiones WHERE estado='activa'")
        datos = cursor.fetchall()
        conexion.close()
        return datos
    
    def obtener_completadas(self):
        """misiones de estado 'completada'"""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM misiones WHERE estado='completada'")
        datos = cursor.fetchall()
        conexion.close()
        return datos
    
    def exportar_misiones_a_texto(self, ruta_archivo):
    #Exporta todas las misiones a un archivo de texto 
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()

            cursor.execute("SELECT tarea, fecha_limite, recompensa, dificultad, estado FROM misiones")
            misiones = cursor.fetchall()

            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write("=== HISTORIAL DE MISIONES ===\n\n")

                if not misiones:
                    f.write("No hay misiones registradas.\n")
                else:
                    for i, mis in enumerate(misiones, 1):
                        f.write(f"Misión #{i}\n")
                        f.write(f"  Tarea: {mis[0]}\n")
                        f.write(f"  Fecha: {mis[1]}\n")
                        f.write(f"  XP: {mis[2]}\n")
                        f.write(f"  Dificultad: {mis[3]}\n")
                        f.write(f"  Estado: {mis[4]}\n")
                        f.write("-" * 30 + "\n")

            conexion.close()
            return True

        except Exception as e:
            print(f"[ERROR] No se pudo exportar: {e}")
            return False
        
    def marcar_completada(self, nombre):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE misiones SET estado='completada' WHERE nombre=?", (nombre,))
        self.conn.commit()