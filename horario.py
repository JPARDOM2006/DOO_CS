class Horario:
    def __init__(self, nombre_cancha, precio, horario, estado, tipo_cancha):
        self.nombre_cancha = nombre_cancha
        self.precio = precio
        self.horario = horario
        self.estado = estado
        self.tipo_cancha = tipo_cancha

    def __str__(self):
        return f"{self.nombre_cancha} {self.precio} {self.horario} {self.horario} {self.tipo_cancha}"

cancha_1 = Horario("Bosa Estacion", 200000, "7:00 AM - 9:00 PM", "Abierta", "Futbol 5")

print(cancha_1)