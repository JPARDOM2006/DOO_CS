class Reservas:
    def __init__(self, fecha_apartada, hora_inicio, hora_final, duracion, estado, total_reserva, abono):
        self.fecha_apartada = fecha_apartada
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.duracion = duracion
        self.estado = estado
        self.total_reserva = total_reserva
        self.abono = abono

    def calcular(self, tarifa_hora):
        self.total_reserva = self.duracion * tarifa_hora
        print(f"Total de la reserva: {self.total_reserva}")

    def calcular_excedente(self):
        return self.total_reserva - self.abono

    def fecha(self):
        print(f"Fecha apartada: {self.fecha_apartada}")

    def horario(self):
        print(f"Horario: {self.hora_inicio} - {self.hora_final}")

    def consultar_estado(self):
        print(f"Estado de la reserva: {self.estado}")

    def reserva_confirmada(self):
        if self.abono >= self.total_reserva * 0.5:
            self.estado = "Confirmada"
            print("Reserva confirmada")
        else:
            print("La reserva no se puede confirmar, falta el abono")

    def calcular_abono(self, porcentaje=0.5):
        self.abono = self.total_reserva * porcentaje
        print(f"Abono requerido: {self.abono}")

    def validar_disponibilidad(self, hora_inicio, hora_fin, reservas_existentes):
        """
        Valida si el horario solicitado está disponible.
        reservas_existentes: lista de tuplas/dicts con (hora_inicio, hora_fin) de reservas confirmadas.
        Retorna True si está disponible, False si hay colisión.
        """
        try:
            # Normalizar horas nuevas a objetos time para comparación
            fmt = "%I:%M %p"
            try:
                nuevo_ini = datetime.datetime.strptime(str(hora_inicio).strip(), fmt)
                nuevo_fin = datetime.datetime.strptime(str(hora_fin).strip(), fmt)
            except ValueError:
                # Intentar formato 24h
                fmt24 = "%H:%M"
                nuevo_ini = datetime.datetime.strptime(str(hora_inicio).strip(), fmt24)
                nuevo_fin = datetime.datetime.strptime(str(hora_fin).strip(), fmt24)

            for res in reservas_existentes:
                # res puede ser (hora_inicio, hora_final) o dict
                if isinstance(res, (tuple, list)):
                    r_ini_str, r_fin_str = res[0], res[1]
                else:
                    r_ini_str = res.get('hora_inicio')
                    r_fin_str = res.get('hora_final')

                try:
                    r_ini = datetime.datetime.strptime(str(r_ini_str).strip(), fmt)
                    r_fin = datetime.datetime.strptime(str(r_fin_str).strip(), fmt)
                except ValueError:
                    try:
                        fmt24 = "%H:%M"
                        r_ini = datetime.datetime.strptime(str(r_ini_str).strip(), fmt24)
                        r_fin = datetime.datetime.strptime(str(r_fin_str).strip(), fmt24)
                    except ValueError:
                        continue  # Si no se puede parsear, ignorar esa reserva

                # Colisión: (Inicio_nuevo < Fin_existente) and (Fin_nuevo > Inicio_existente)
                if (nuevo_ini < r_fin) and (nuevo_fin > r_ini):
                    return False
            return True
        except Exception:
            # En caso de error de parsing, permitir (validación laxa) o denegar; mejor denegar por seguridad
            return False


import datetime
