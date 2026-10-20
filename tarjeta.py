import metodo_pago as MP

class Tarjeta(MP.MetodoPago):
    def __init__(self, id_metodopago, tipo_pago, descripcion, id_tarjeta, tipo_tarjeta, titular, fecha_vencimiento, codigo_seguridad):
        super().__init__(id_metodopago, tipo_pago, descripcion)
        self.id_tarjeta = id_tarjeta
        self.tipo_tarjeta = tipo_tarjeta
        self.titular = titular
        self.fecha_vencimiento = fecha_vencimiento
        self.codigo_seguridad = codigo_seguridad

    def validarTarjeta(self):
        print(f"Validando tarjeta de {self.tipo_tarjeta} a nombre de {self.titular}...")
        return True