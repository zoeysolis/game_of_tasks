import sqlite3

class GestorBaseDatos:
    def __init__(self, nombre_db="misiones.db"):
        self.nombre_db = nombre_db
        self.crear_tabla()

    def conectar(self):
        return sqlite3.connect(self.nombre_db)

    def crear_tabla(self):
        """Crea la tabla de misiones"""
        conexion = self.conectar()
        cursor = conexion.cursor()
        
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

    def agregar_mision(self, tarea, fecha_limite, recompensa, dificultad):
        """Nueva misióne"""
        try:
            conexion_local = self.conectar() 
            cursor = conexion_local.cursor()
            
            # Guardamos el estado inicial 
            cursor.execute('''
                INSERT INTO misiones (tarea, fecha_limite, recompensa, dificultad, estado)
                VALUES (?, ?, ?, ?, 'activa')
            ''', (tarea, fecha_limite, recompensa, dificultad))
            
            conexion_local.commit()
            conexion_local.close()
            print("[BASE DE DATOS] Misión agregada con éxito.")
        except Exception as e:
            print(f"[ERROR BD] No se pudo agregar la misión: {e}")

    def obtener_todas(self):
        """Recupera todas las misiones guardadas"""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM misiones")
        datos = cursor.fetchall()
        conexion.close()
        return datos
    
    def marcar_completada(self, tarea):
        """Cambia el estado de una misión"""
        try:
            conexion_local = self.conectar() # Usamos self.conectar()
            cursor = conexion_local.cursor()
            
            # Ponemos el estado en completada en formato texto
            cursor.execute('''
                UPDATE misiones 
                SET estado = 'completada' 
                WHERE tarea = ?
            ''', (tarea,))
            
            conexion_local.commit()
            conexion_local.close()
            print(f"[BASE DE DATOS] Misión '{tarea}' marcada como completada.")
        except Exception as e:
            print(f"[ERROR BD] No se pudo completar la misión: {e}")

    def obtener_misiones_futuras(self):
        """Busca todas las misiones activas con fecha límite posterior a la de hoy"""
        from datetime import datetime
        try:
            conexion_local = self.conectar()
            cursor = conexion_local.cursor()
            
            cursor.execute("SELECT tarea, fecha_limite, recompensa, dificultad FROM misiones WHERE estado = 'activa'")
            todas_activas = cursor.fetchall()
            conexion_local.close()
            
            ahora = datetime.now()
            futuras = []
            
            for m in todas_activas:
                try:
                    fecha_mision = datetime.strptime(m[1], "%Y-%m-%d %H:%M:%S")
                    if fecha_mision > ahora:
                        futuras.append(m)
                except Exception:
                    continue
                    
            return futuras
        except Exception as e:
            print(f"[ERROR BD] No se pudieron obtener misiones futuras: {e}")
            return []

    def exportar_misiones_a_texto(self, ruta_archivo):
        """Exporta todas las misiones a un archivo de texto"""
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