class Empleado:
    def __init__(self, cargo, salario, horario, direccion):
        self.cargo = cargo
        self.salario = salario
        self.horario = horario
        self.direccion = direccion
        self.lista = []


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