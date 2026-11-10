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


class CanchaBuilder:
  """Builder (Method Chaining) para construir objetos Cancha."""

  def __init__(self):
    self._id_cancha = None
    self._nombre = None
    self._tipo_superficie = None
    self._precio_hora = None
    self._estado = None
    self._horario = None

  def set_id(self, id_cancha):
    self._id_cancha = id_cancha
    return self

  def set_nombre(self, nombre):
    self._nombre = nombre
    return self

  def set_tipo_superficie(self, tipo_superficie):
    self._tipo_superficie = tipo_superficie
    return self

  def set_precio_hora(self, precio_hora):
    self._precio_hora = precio_hora
    return self

  def set_estado(self, estado):
    self._estado = estado
    return self

  def set_horario(self, horario):
    self._horario = horario
    return self

  def build(self):
    if self._id_cancha is None:
      raise ValueError("[Builder] La cancha necesita un ID válido.")
    if not self._nombre or not str(self._nombre).strip():
      raise ValueError("[Builder] La cancha necesita un nombre válido.")
    if not self._tipo_superficie or not str(self._tipo_superficie).strip():
      raise ValueError("[Builder] La cancha necesita un tipo de superficie válido.")
    try:
      precio_hora = float(self._precio_hora)
    except (TypeError, ValueError):
      precio_hora = None
    if precio_hora is None or precio_hora < 0:
      raise ValueError("[Builder] La cancha necesita un precio por hora válido.")
    cancha = Cancha(
      id_cancha=self._id_cancha,
      nombre_cancha=str(self._nombre).strip(),
      precio=precio_hora,
      horario=str(self._horario).strip() if self._horario else "",
      tipo_cancha=str(self._tipo_superficie).strip(),
    )
    cancha.estado = self._estado if self._estado is not None else "Disponible"
    return cancha