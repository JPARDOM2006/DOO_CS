class Establecimiento:
  def __init__(self, id_establecimiento, nombre_establecimiento, ubicación):
    self.id_establecimiento = id_establecimiento
    self.nombre_establecimiento = nombre_establecimiento
    self.ubicación = ubicación
    self.lista_canchas = []

  def agregar_cancha(self, nueva_cancha):
    self.lista_canchas.append(nueva_cancha)
    print(f"Cancha {nueva_cancha.nombre_cancha} agregada con exito.")


class EstablecimientoBuilder:
  """Builder (Method Chaining) para construir objetos Establecimiento."""

  def __init__(self):
    self._id_establecimiento = 1
    self._nombre = None
    self._direccion = None
    self._telefono = ""
    self._horario = ""

  def set_id_establecimiento(self, id_establecimiento):
    self._id_establecimiento = id_establecimiento
    return self

  def set_nombre(self, nombre):
    self._nombre = nombre
    return self

  def set_direccion(self, direccion):
    self._direccion = direccion
    return self

  def set_telefono(self, telefono):
    self._telefono = telefono
    return self

  def set_horario(self, horario):
    self._horario = horario
    return self

  def build(self):
    if not self._nombre or not str(self._nombre).strip():
      raise ValueError("[Builder] El establecimiento necesita un nombre válido.")
    if not self._direccion or not str(self._direccion).strip():
      raise ValueError("[Builder] El establecimiento necesita una dirección válida.")
    establecimiento = Establecimiento(
      id_establecimiento=self._id_establecimiento,
      nombre_establecimiento=str(self._nombre).strip(),
      ubicación=str(self._direccion).strip(),
    )
    establecimiento.telefono = str(self._telefono).strip()
    establecimiento.horario = str(self._horario).strip()
    return establecimiento