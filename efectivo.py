import metodo_pago as MP

class Efectivo(MP.MetodoPago):
    def __init__(self, id_metodopago, tipo_pago, descripcion, id_efectivo, monto_recibido, cambio, estado):
        super().__init__(id_metodopago, tipo_pago, descripcion)
        self.id_efectivo = id_efectivo
        self.monto_recibido = monto_recibido
        self.cambio = cambio
        self.estado = estado

    def calcularCambio(self, total_pago):
        self.cambio = self.monto_recibido - total_pago
        print(f"Cambio calculado: {self.cambio}")
        return self.cambio

    def validarPago(self, total_pago):
        if self.monto_recibido >= total_pago:
            self.estado = "Aprobado"
            self.calcularCambio(total_pago)
            print("Pago en efectivo validado correctamente.")
            return True
        else:
            self.estado = "Insuficiente"
            print("El monto recibido es menor al total del pago.")
            return False