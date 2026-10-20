import metodo_pago as MP

class Transferencia(MP.MetodoPago):

    def __init__(self, id_metodopago, tipo_pago, descripcion, id_transferencia, banco_origen, fecha, valor, estado):
        super().__init__(id_metodopago, tipo_pago, descripcion)
        self.id_trasferencia = id_transferencia
        self.fecha = fecha
        self.valor = valor 
        self.estado = estado

    def validarTransferencia(self):
        print (f"Validando trasferencia desde {self.banco_origen} por un valor de {self.valor}.Estado actual: {self.estado}")

        if self.estado == "completada":
            print("trasferencia valida con exito ")
            return True
        else:
            print("La trasferencia no se puedo completar o esta pendiente ")
            return False
