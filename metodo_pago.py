class MetodoPago:
    def __init__(self, id_metodopago, tipo_pago, descripcion):
        self.id_metodopago = id_metodopago
        self.tipo_pago = tipo_pago
        self.descripcion = descripcion

    def validar(self):
        print(f"Validando método de pago genérico (ID: {self.id_metodopago})...")
        return True


class MetodoPagoBuilder:
    """Builder (Method Chaining) para construir objetos MetodoPago."""

    def __init__(self):
        self._id_pago = None
        self._monto = None
        self._tipo = None
        self._fecha = None
        self._descripcion = None

    def set_id_pago(self, id_pago):
        self._id_pago = id_pago
        return self

    def set_monto(self, monto):
        self._monto = monto
        return self

    def set_tipo(self, tipo):
        self._tipo = tipo
        return self

    def set_fecha(self, fecha):
        self._fecha = fecha
        return self

    def set_descripcion(self, descripcion):
        self._descripcion = descripcion
        return self

    def build(self):
        if self._id_pago is None:
            raise ValueError("[Builder] El método de pago necesita un ID.")
        if not self._tipo or not str(self._tipo).strip():
            raise ValueError("[Builder] El método de pago necesita un tipo válido.")
        pago = MetodoPago(
            id_metodopago=self._id_pago,
            tipo_pago=str(self._tipo).strip(),
            descripcion=str(self._descripcion).strip() if self._descripcion and str(self._descripcion).strip() else str(self._tipo).strip(),
        )
        pago.monto = self._monto if self._monto is not None else 0.0
        pago.fecha = str(self._fecha).strip() if self._fecha else ""
        return pago