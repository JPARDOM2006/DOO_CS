class Mantenimiento:
    """Producto final del patrón Builder: una intervención de mantenimiento sobre una cancha."""

    # Registro en memoria de los mantenimientos creados (para el reporte administrativo)
    registro = []

    def __init__(self, id_cancha, fecha, hora_inicio, hora_final, motivo, estado="Programado"):
        self.id_cancha = id_cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.motivo = motivo
        self.estado = estado
        Mantenimiento.registro.append(self)

    def __str__(self):
        return (f"Mantenimiento de la cancha ID {self.id_cancha} programado el {self.fecha} "
                f"de {self.hora_inicio} a {self.hora_final} | Motivo: {self.motivo} | Estado: {self.estado}")

    def resumen(self):
        """Representa los datos de la intervención como un diccionario de consulta."""
        return {
            "id_cancha": self.id_cancha,
            "fecha": self.fecha,
            "hora_inicio": self.hora_inicio,
            "hora_final": self.hora_final,
            "motivo": self.motivo,
            "estado": self.estado,
        }


class MantenimientoBuilder:
    """Builder para construir objetos Mantenimiento."""

    def __init__(self):
        # Estructura temporal de Mantenimiento con valores por defecto
        self._temporal = Mantenimiento(
            id_cancha=None,
            fecha="",
            hora_inicio="",
            hora_final="",
            motivo="",
            estado="Programado",
        )

    def set_id_cancha(self, id_cancha):
        self._temporal.id_cancha = id_cancha
        return self

    def set_fecha(self, fecha):
        self._temporal.fecha = fecha
        return self

    def set_hora_inicio(self, hora_inicio):
        self._temporal.hora_inicio = hora_inicio
        return self

    def set_hora_final(self, hora_final):
        self._temporal.hora_final = hora_final
        return self

    def set_motivo(self, motivo):
        self._temporal.motivo = motivo
        return self

    def set_estado(self, estado):
        self._temporal.estado = estado
        return self

    def build(self):
        t = self._temporal
        if t.id_cancha is None:
            raise ValueError("[MantenimientoBuilder] Todos los campos son obligatorios.")
        if not str(t.fecha).strip() or not str(t.hora_inicio).strip() or not str(t.hora_final).strip() or not str(t.motivo).strip():
            raise ValueError("[MantenimientoBuilder] Todos los campos son obligatorios.")
        return Mantenimiento(
            id_cancha=t.id_cancha,
            fecha=str(t.fecha).strip(),
            hora_inicio=str(t.hora_inicio).strip(),
            hora_final=str(t.hora_final).strip(),
            motivo=str(t.motivo).strip(),
            estado=t.estado,
        )
