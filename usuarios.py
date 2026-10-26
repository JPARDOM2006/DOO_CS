import datetime


class Usuarios:
    def __init__(self, nombre, apellido, documento, telefono, correo, password):
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.telefono = telefono
        self.correo = correo
        self.password = password
        self.fecha_registro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def inicio_sesion(self):
        print("Ingreso a la sesión de usuario")


class Cliente(Usuarios):
    def __init__(self, nombre, apellido, documento, telefono, correo, password):
        super().__init__(nombre, apellido, documento, telefono, correo, password)

    def crear_reservas(self, sistema):
        # Llama a la función del sistema y se pasa a sí mismo como el cliente actual
        sistema.crear_reserva_sistema(self)

    def consultar_reservas(self, sistema):
        sistema.consultar_mis_reservas(self)

    def editar_reservas(self, sistema):
        sistema.editar_mis_reservas(self)

    def cancelar_reservas(self, sistema):
        sistema.cancelar_mis_reservas(self)


class Empleado(Usuarios):
    def __init__(self, nombre, apellido, documento, telefono, correo, password, cargo, salario, horario, direccion):
        super().__init__(nombre, apellido, documento, telefono, correo, password)
        self.cargo = cargo
        self.salario = salario
        self.horario = horario
        self.direccion = direccion

    def registrar_entrada(self):
        print(f"\n[!] Entrada registrada exitosamente para {self.nombre} a las {datetime.datetime.now().strftime('%H:%M')}")

    def registrar_salida(self):
        print(f"\n[!] Salida registrada exitosamente para {self.nombre} a las {datetime.datetime.now().strftime('%H:%M')}")

    def consultar_reservas(self, sistema):
        sistema.mostrar_todas_las_reservas()

    def actualizar_disponibilidad(self, sistema):
        sistema.actualizar_estado_cancha()

    def registrar_mantenimiento(self, sistema):
        sistema.registrar_mantenimiento_cancha()


class Administrador(Usuarios):
    def __init__(self, nombre, apellido, documento, telefono, correo, password, cargo, salario, direccion):
        super().__init__(nombre, apellido, documento, telefono, correo, password)
        self.cargo = cargo
        self.salario = salario
        self.direccion = direccion

    def registrar_cancha(self, sistema):
        sistema.crear_cancha_nueva()

    def gestionar_usuarios(self, sistema):
        print("Módulo de gestión de usuarios en desarrollo...")

    def gestionar_reportes(self, sistema):
        if hasattr(sistema, 'generar_reportes'):
            sistema.generar_reportes()
        else:
            print("Generando reportes financieros y de ocupación...")
