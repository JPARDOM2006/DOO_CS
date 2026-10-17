class Establecimiento:
  def __init__(self, id_establecimiento, nombre_establecimiento, ubicación):
    self.id_establecimiento = id_establecimiento
    self.nombre_establecimiento = nombre_establecimiento
    self.ubicación = ubicación
    self.lista_canchas = []

  def agregar_cancha(self, nueva_cancha):
    self.lista_canchas.append(nueva_cancha)
    print(f"Cancha {nueva_cancha.nombre_cancha} agregada con exito.")