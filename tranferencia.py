import metodo_pago as MP


class Transferencia(MP.MetodoPago):

    def __init__(self, id_metodopago, tipo_pago, descripcion, id_transferencia, banco_origen, fecha, valor, estado):
        super().__init__(id_metodopago, tipo_pago, descripcion)
        self.id_trasferencia = id_transferencia
        self.banco_origen = banco_origen
        self.fecha = fecha
        self.valor = valor
        self.estado = estado

    def validarTransferencia(self):
        print(f"Validando trasferencia desde {self.banco_origen} por un valor de {self.valor}. Estado actual: {self.estado}")

        if self.estado == "completada":
            print("trasferencia valida con exito ")
            return True
        else:
            print("La trasferencia no se puedo completar o esta pendiente ")
            return False


class TransferenciaBuilder(MP.MetodoPagoBuilder):
    """Builder (Method Chaining) de Transferencia; extiende MetodoPagoBuilder."""

    def __init__(self):
        super().__init__()
        self._banco_origen = None
        self._numero_cuenta = None
        self._comprobante = None

    def set_banco_origen(self, banco_origen):
        self._banco_origen = banco_origen
        return self

    def set_numero_cuenta(self, numero_cuenta):
        self._numero_cuenta = numero_cuenta
        return self

    def set_comprobante(self, comprobante):
        self._comprobante = comprobante
        return self

    def build(self):
        if not self._banco_origen or not str(self._banco_origen).strip():
            raise ValueError("[Builder] La transferencia necesita un banco de origen válido.")
        transferencia = Transferencia(
            id_metodopago=self._id_pago if self._id_pago is not None else 3,
            tipo_pago=str(self._tipo).strip() if self._tipo else "Transferencia",
            descripcion=str(self._descripcion).strip() if self._descripcion and str(self._descripcion).strip() else "Transferencia bancaria",
            id_transferencia=1,
            banco_origen=str(self._banco_origen).strip(),
            fecha=str(self._fecha).strip() if self._fecha else "",
            valor=self._monto if self._monto is not None else 0.0,
            estado="completada",
        )
        transferencia.numero_cuenta = str(self._numero_cuenta).strip() if self._numero_cuenta else ""
        transferencia.comprobante = str(self._comprobante).strip() if self._comprobante else ""
        return transferencia
