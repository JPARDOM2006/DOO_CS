class Cancha:
    def __init__(self, nombre_cancha, precio, horario, estado, tipo_cancha):
        self.nombre_cancha = nombre_cancha
        self.precio = precio
        self.horario = horario
        self.estado = estado
        self.tipo_cancha = tipo_cancha

cancha_1 = Cancha("Cancha Bosa Recreo", 200000, "7:00 AM - 9:00 PM", "Abierta", "Futbol 5")

print(cancha_1.nombre_cancha, cancha_1.tipo_cancha, cancha_1.estado, cancha_1.horario)
        