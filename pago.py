class Pago():
    def __init__(self, fecha_pago, valor, comprobante, estado):
        self.fecha_pago = fecha_pago
        self.valor = valor
        self.comprobante = comprobante
        self.estado = estado

    def registrar_Pago(self):
        print(f"Pago registrado por {self.valor} el {self.fecha_pago}")

    def verificar_Pago(self):
        return self.valor > 0 and self.comprobante != ""

    def calcularTotal(self, reserva):
        return reserva.total_reserva - reserva.abono

    def fecha_final(self):
        print(f"Fecha del pago: {self.fecha_pago}")

    def horario_final(self):
        print("Horario final del pago registrado")

    def estado_final(self):
        print(f"Estado del pago: {self.estado}")

    def reserva_reconfirmada(self, reserva):
        if self.verificar_Pago():
            reserva.estado = "Confirmada"
            print("Reserva reconfirmada con el pago")
        else:
            print("El pago no es válido, no se puede reconfirmar")
        