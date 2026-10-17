import tarifa as TF


class Horario:

  def __init__(self, id_horario, dias_semana, tipo_dia, jornada, hora_inicio, hora_final, tarifa: TF.Tarifa = None ):
    
    self.id_horario = id_horario
    self.dias_semana = dias_semana
    self.tipo_dia = tipo_dia
    self.jornada = jornada
    self.hora_inicio = hora_inicio
    self.hora_final = hora_final
    self.tarifa = tarifa

  def calcular_horario(self):
    if self.tarifa:
      return (
          f"Horario {self.hora_inicio} a {self.hora_final} - Valor:"
          f" {self.tarifa.calcular_tarifa()}"
      )
    return f"Horario {self.hora_inicio} a {self.hora_final}"