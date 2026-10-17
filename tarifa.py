class Tarifa:

  def __init__(self, id_tarifa, valor_hora, dias_semana, valor_dia, valor_ubicacion, valor_tipo_jornada ):
    
    self.id_tarifa = id_tarifa
    self.valor_hora = valor_hora
    self.dias_semana = dias_semana
    self.valor_dia = valor_dia
    self.valor_ubicacion = valor_ubicacion
    self.valor_tipo_jornada = valor_tipo_jornada

  def calcular_tarifa(self):
    total = (
        self.valor_hora
        + self.valor_dia
        + self.valor_ubicacion
        + self.valor_tipo_jornada
    )
    return total