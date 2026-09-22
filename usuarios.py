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

usuario_1 = Usuarios("Juan", "Pardo", 1012339187, 3213959007, "j.@gmail.com", "02", "J", "5")

usuario_1.registro()