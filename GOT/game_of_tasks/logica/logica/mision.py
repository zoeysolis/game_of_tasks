class Mision:
    def __init__(self, nombre, dificultad="Media", xp=None, estado="activa", id_mision=None):
        """
        Constructor de la clase Mision
        Modela una tarea del estudiante como una aventura de un juego RPG
        """
        self.id = id_mision
        self.nombre = nombre
        self.dificultad = dificultad
        self.estado = estado # Puede ser "activa" o "completada"
        
        # Gamificación automática: Si no se especifica XP, se calcula según la dificultad
        if xp is None or xp == 0:
            self.xp = self.calcular_xp_automatico()
        else:
            self.xp = xp

    def calcular_xp_automatico(self):
        """Asigna una recompensa de experiencia basada en la dificultad de la misión, por default siemmpre es media"""
        if self.dificultad == "Fácil":
            return 25
        elif self.dificultad == "Media":
            return 50
        elif self.dificultad == "Difícil":
            return 100
        return 50 # Valor por defecto

    def completar(self):
        """Cambia el estado de la misión a completada"""
        self.estado = "completada"

    def a_tupla(self):
        """
        Convierte el objeto en una tupla
        Esto es para enviarlo directamente a la base de datos
        """
        return (self.nombre, self.xp, self.dificultad, self.estado)

    def __str__(self):
        """Representación en texto del objeto """
        return f"Misión RPG: [{self.estado.upper()}] {self.nombre} ({self.dificultad}) - Recompensa: {self.xp} XP"