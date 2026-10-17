import horario as HR

class Cancha:

  def __init__(self, id_cancha, nombre_cancha, precio, horario, tipo_cancha):
    self.id_cancha = id_cancha
    self.nombre_cancha = nombre_cancha
    self.precio = precio
    self.horario = horario  
    self.estado = True  
    self.tipo_cancha = tipo_cancha  

  def obtenerDisponibilidad(self):
    return self.estado

  def obtenerDisponibilidad_Hora(self):
    print(f"Horario asignado a la cancha: {self.horario}")
    return self.estado

  def actualizarEstado(self, nuevo_estado):
    self.estado = nuevo_estado
    print(
        f"El estado de la cancha {self.nombre_cancha} cambio a: {self.estado}"
    )