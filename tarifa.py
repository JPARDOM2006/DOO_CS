class Tarifa:

    def __init__(self, horario):
        self.horario = horario

    def calcular_tarifa(self):
        total = self.horario.valor_h
        # Evaluar si es fin de semana para aplicar recargo por día
        dias = str(self.horario.dias_semana).lower()
        tipo_dia = str(self.horario.tipo_dia).lower()
        if "sábado" in dias or "sabado" in dias or "domingo" in dias or "fin de semana" in dias or "festivo" in tipo_dia or "fin de semana" in tipo_dia:
            total += self.horario.valor_d
        # Evaluar si la franja es nocturna para aplicar recargo
        jornada = str(self.horario.jornada).lower()
        if "noche" in jornada or "nocturna" in jornada or "nocturno" in jornada:
            total += self.horario.valor_d
        return total
