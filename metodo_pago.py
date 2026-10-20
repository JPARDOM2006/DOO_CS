class MetodoPago:
    def __init__(self, id_metodopago, tipo_pago, descripcion):
        self.id_metodopago = id_metodopago
        self.tipo_pago = tipo_pago
        self.descripcion = descripcion

    def validar(self):
        print(f"Validando método de pago genérico (ID: {self.id_metodopago})...")
        return True