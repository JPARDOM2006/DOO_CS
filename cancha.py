class Cancha:
    def __init__(self, id_cancha, nombre_cancha, tipo_superficie, capacidad, tiene_techado, estado="Disponible"):
        self.id_cancha = id_cancha
        self.nombre_cancha = nombre_cancha
        self.tipo_superficie = tipo_superficie
        self.capacidad = capacidad
        self.tiene_techado = tiene_techado
        self.estado = estado  