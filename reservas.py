import usuarios as US
import cancha as CA



class Reservas:
    def __init__(self,fecha_apartada, hora_inicio, hora_final, duracion, estado, total_reserva, abono):
        self.fecha_apartada = fecha_apartada
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.duracion = duracion
        self. estado = estado
        self.total_reserva = total_reserva
        self.abono = abono

        

class Principal:
    def __init__(self):
        self.lista_canchas=[]
        self.lista_clientes=[]
        self.lista_reservas=[]
        self.lista_empleados=[]
        self.administradores=[]


    def menu(self):

        while True:
            print("1. Crear usuario")
            opc = int(input("Ingrese una opción: "))

            if opc=="1":
                op = int(input("Ingrese el tipo de usuario que desea crear: 1. Cliente 2. Empleado 3. Administrador: "))
                if op == 1:
                    nombre= input("Ingrese el nombre: ")
                    apellido= input("Ingrese el apellido: ")
                    documento= input("Ingrese el documento: ")
                    telefono= input("Ingrese el telefono: ")
                    correo= input("Ingrese el correo: ")
                    fecha_registro= input("Ingrese el fecha_registro: ")
                    user= input("Ingrese el user: ")
                    password= input("Ingrese el password: ")

                    nuevo_cliente= US.Cliente(nombre,apellido,documento,telefono,correo,fecha_registro,user,password)
                    self.lista_clientes.append(nuevo_cliente)
                    
                if op == 2:
                    nombre= input("Ingrese el nombre: ")
                    apellido= input("Ingrese el apellido: ")
                    documento= input("Ingrese el documento: ")
                    telefono= input("Ingrese el telefono: ")
                    correo= input("Ingrese el correo: ")
                    fecha_registro= input("Ingrese el fecha_registro: ")
                    user= input("Ingrese el user: ")
                    password= input("Ingrese el password: ")
                    cargo= input("Ingrese el cargo: ")
                    salario= input("Ingrese el salario: ")
                    horario= input("Ingrese el horario: ")
                    direccion= input("Ingrese la direccion: ")

                    nuevo_empleado= US.Empleado(nombre,apellido,documento,telefono,correo,fecha_registro,user,password)
                    self.lista_empleados.append(nuevo_empleado)

                if op == 3:
                    nombre= input("Ingrese el nombre: ")
                    apellido= input("Ingrese el apellido: ")
                    documento= input("Ingrese el documento: ")
                    telefono= input("Ingrese el telefono: ")
                    correo= input("Ingrese el correo: ")
                    fecha_registro= input("Ingrese el fecha_registro: ")
                    user= input("Ingrese el user: ")
                    password= input("Ingrese el password: ")
                    cargo= input("Ingrese el cargo: ")
                    salario= input("Ingrese el salario: ")
                    direccion= input("Ingrese la direccion: ")

                    nuevo_administrador= US.Administrador(nombre,apellido,documento,telefono,correo,fecha_registro,user,password,cargo,salario,direccion)
                    self.administradores.append(nuevo_administrador)

            elif opc=="2":
                for i in self.lista_clientes:
                    print(i.nombre)

    if __name__  == "__main__":
        a = principal()
        a.menu()