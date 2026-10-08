class Usuarios:
    def __init__(self, nombre, apellido, documento, telefono, correo, fecha_registro, name, password):
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.telefono = telefono
        self.correo = correo
        self.fecha_registro = fecha_registro
        self.name = name
        self.password = password
        self.lista = []

    def inicio_sesion(self):
        print("Ingreso a la sesion de usuario")
        nombre = str(input("Ingrese su nombre de usuario: "))
        password = str(input("Ingrese su contraseña: "))

    def registro(self):
        nombre = input("Ingrese su nombre: ")
        apellido = input("Ingrese su apellido: ")
        documento = input("Ingrese su numero de documento: ")
        telefono = input("Ingrese su numero de telefono: ")
        correo = input("Ingrese su correo electronico: ")
        password = input("Ingrese su contraseña: ")

        usuario = [nombre, apellido, documento, telefono, correo, password]
        self.lista.append(usuario)
        for _ in usuario:
            print(_) 


class Cliente(Usuarios):
    def __init__(self, nombre, apellido, documento, telefono, correo, password):
        super().__init__(nombre, apellido, documento, telefono, correo, password)

    def crear_usuario(self):
        nombre = str(input("Ingrese su nombre de usuario: "))

    def crear_reservas(self):
        pass

    def editar_reservas(self):
        pass

    def cancelar_reservas(self):
        pass    


class Empleado(Usuarios):
    def __init__(self, nombre, apellido, documento, telefono, correo, password, cargo, salario, horario, direccion):
        super().__init__(nombre, apellido, documento, telefono, correo, password)
        self.cargo = cargo
        self.salario = salario
        self.horario = horario
        self.direccion = direccion
        self.lista_empleado = []

    def registrar_entrada(self):
        nombre = input("Ingrese su nombre: ")
        if nombre in self.lista:
            print("Bienvenido, puede ingresar")
        else:
            print("No se encuentra registrado en el sistema, digite de nuevo su nombre")

    def registrar_salida(self):
        nombre = input("Ingrese su nombre: ")
        if nombre in self.lista:
            print("Gracias por su visita, puede salir")
        else:
            print("No se encuentra registrado en el sistema, digite de nuevo su nombre")

    def consultar_reservas(self):
        print("Consultando reservas...")

    def actualizar_disponibilidad(self):
        print("Actualizando disponibilidad...")

    def registrar_mantenimiento(self):
        print("Registrando mantenimiento...")


class Administrador(Usuarios):
    def __init__(self, nombre, apellido, documento, telefono, correo, password, cargo, salario, direccion):
        super().__init__(nombre, apellido, documento, telefono, correo, password)
        self.cargo = cargo
        self.salario = salario
        self.direccion = direccion

    def gestionar_usuarios(self):
        print("Gestionando usuarios...")

    def gestionar_reportes(self):
        print("Gestionando reportes...")

    def crear_usuarios(self):
        print("Creando usuarios...")