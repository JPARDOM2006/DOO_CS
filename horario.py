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


class HorarioBuilder:
    """Builder (Method Chaining) para construir objetos Horario."""

    def __init__(self):
        self._id_horario = 0
        self._hora_inicio = None
        self._hora_fin = None
        self._dias_operacion = None
        self._tipo_dia = None
        self._jornada = None
        self._valor_h = None
        self._valor_d = None

    def set_hora_inicio(self, hora_inicio):
        self._hora_inicio = hora_inicio
        return self

    def set_hora_fin(self, hora_fin):
        self._hora_fin = hora_fin
        return self

    def set_dias_operacion(self, dias_operacion):
        self._dias_operacion = dias_operacion
        return self

    def set_id_horario(self, id_horario):
        self._id_horario = id_horario
        return self

    def set_tipo_dia(self, tipo_dia):
        self._tipo_dia = tipo_dia
        return self

    def set_jornada(self, jornada):
        self._jornada = jornada
        return self

    def set_valor_hora(self, valor_h):
        self._valor_h = valor_h
        return self

    def set_recargo_dia(self, valor_d):
        self._valor_d = valor_d
        return self

    def build(self):
        if not self._hora_inicio or not str(self._hora_inicio).strip():
            raise ValueError("[Builder] El horario necesita una hora de inicio válida.")
        if not self._hora_fin or not str(self._hora_fin).strip():
            raise ValueError("[Builder] El horario necesita una hora de cierre válida.")
        if not self._dias_operacion or not str(self._dias_operacion).strip():
            raise ValueError("[Builder] El horario necesita días de operación definidos.")
        return Horario(
            id_horario=self._id_horario,
            dias_semana=str(self._dias_operacion).strip(),
            tipo_dia=str(self._tipo_dia).strip() if self._tipo_dia else "Normal",
            jornada=str(self._jornada).strip() if self._jornada else "Diurna",
            hora_inicio=str(self._hora_inicio).strip(),
            hora_final=str(self._hora_fin).strip(),
            valor_h=self._valor_h if self._valor_h is not None else 0.0,
            valor_d=self._valor_d if self._valor_d is not None else 0.0,
        )
