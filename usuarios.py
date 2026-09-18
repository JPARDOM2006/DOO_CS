class usuarios:
    def _init__(self, nombre, apellido, documento, telefono, correo, fecha_registro):
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.telefono = telefono
        self.correo = correo
        self.fecha_registro = fecha_registro

    def inicio_sesion(self):
        print("Ingreso a la sesion de usuario")
        name = str(input("Ingrese su nombre de usuario: "))
        password = str(input("Ingrese su contraseña: "))