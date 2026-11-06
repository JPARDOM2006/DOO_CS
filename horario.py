class Horario:

    def __init__(self, id_horario, dias_semana, tipo_dia, jornada, hora_inicio, hora_final, valor_h, valor_d):
        self.id_horario = id_horario
        self.dias_semana = dias_semana
        self.tipo_dia = tipo_dia
        self.jornada = jornada
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.valor_h = valor_h
        self.valor_d = valor_d

    def calcular_horario(self):
        return f"Horario {self.hora_inicio} a {self.hora_final} - Valor hora: {self.valor_h}, Valor día: {self.valor_d}"
