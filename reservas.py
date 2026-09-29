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
        self.lista_administradores=[]

    def crear_usuario(self):
        op = int(input("Ingrese el tipo de usuario que desea crear: 1. Cliente 2. Empleado 3. Administrador: "))
        if op == 1:
            nombre= input("Ingrese el nombre: ")
            apellido= input("Ingrese el apellido: ")
            documento= input("Ingrese el documento: ")
            telefono= input("Ingrese el telefono: ")
            correo= input("Ingrese el correo: ")
            password= input("Ingrese el password: ")
            
            nuevo_cliente= US.Cliente(nombre,apellido,documento,telefono,correo,password)
            self.lista_clientes.append(nuevo_cliente)
            print("Cliente creado exitosamente.")
            
        if op == 2:
            nombre= input("Ingrese el nombre: ")
            apellido= input("Ingrese el apellido: ")
            documento= input("Ingrese el documento: ")
            telefono= input("Ingrese el telefono: ")
            correo= input("Ingrese el correo: ")
            password= input("Ingrese el password: ")
            cargo= input("Ingrese el cargo: ")
            salario= input("Ingrese el salario: ")
            horario= input("Ingrese el horario: ")
            direccion= input("Ingrese la direccion: ")

            nuevo_empleado= US.Empleado(nombre,apellido,documento,telefono,correo,password, cargo,salario,horario,direccion)
            self.lista_empleados.append(nuevo_empleado)
            print("Empleado creado exitosamente.")

        if op == 3:
            nombre= input("Ingrese el nombre: ")
            apellido= input("Ingrese el apellido: ")
            documento= input("Ingrese el documento: ")
            telefono= input("Ingrese el telefono: ")
            correo= input("Ingrese el correo: ")
            password= input("Ingrese el password: ")
            cargo= input("Ingrese el cargo: ")
            salario= input("Ingrese el salario: ")
            direccion= input("Ingrese la direccion: ")

            nuevo_administrador= US.Administrador(nombre,apellido,documento,telefono,correo,password,cargo,salario,direccion)
            self.lista_administradores.append(nuevo_administrador)
            print("Administrador creado exitosamente.")

    def modificar_usuario(self):
        
        opc = int(input("Ingrese el tipo de usuario que desea modificar: 1. Cliente 2. Empleado 3. Administrador: "))
        if len(self.lista_clientes) == 0:
            print("No hay clientes registrados.")
            return

    def eliminar_usuario(self):
        pass

    def generar_reportes(self):
        pass

    def ingresar_usuario(self):
        user = input("Ingrese su correo o nombre, ingresados en el registro: ")
        password = input("Ingrese su contraseña: ")
        if user in [cliente.correo for cliente in self.lista_clientes] or user in [cliente.nombre for cliente in self.lista_clientes]:
            print("Usuario encontrado.")
            if password in [cliente.password for cliente in self.lista_clientes]:
                print("Contraseña correcta. Bienvenido.")
            else:
                print("Contraseña incorrecta.")
                return self.menu() 
        else:
            print("Usuario no encontrado.")
            return self.menu() 
    
    def menu(self):

        while True:
            print("1. Crear usuario")
            print("2. Ingresar como usuario")
            print("3. Mostrar el nombre de los clientes registrados")
            opc = int(input("Ingrese una opción: "))
            if opc == 1:
                self.crear_usuario()

            elif opc == 2:
                self.ingresar_usuario()

            elif opc=="3":
                for i in self.lista_clientes:
                    print(i.nombre)

if __name__ == "__main__":
    a = Principal() 
    a.menu()