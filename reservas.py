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
            print("\nBIENVENIDO A LA CREACION DE USUARIO DE CLIENTES")
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
            print("\nBIENVENIDO A LA CREACION DE USUARIO DE EMPLEADOS")
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
            print("\nBIENVENIDO A LA CREACION DE USUARIO DE ADMINISTRADORES")
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
        

    def ingresar_usuario(self):
        user = input("Ingrese su correo o nombre, ingresados en el registro: ")
        password = input("Ingrese su contraseña: ")

        usuario_logueado = None
        rol = ""

        for cliente in self.lista_clientes:
            if (cliente.correo == user or cliente.nombre == user) and cliente.password == password:
                usuario_logueado = cliente
                rol = "cliente"
                break

        if not usuario_logueado:
            for empleado in self.lista_empleados:
                if (empleado.correo == user or empleado.nombre == user) and empleado.password == password:
                    usuario_logueado = empleado
                    rol = "empleado"
                    break

        if not usuario_logueado:
            for administrador in self.lista_administradores:
                if (administrador.correo == user or administrador.nombre == user) and administrador.password == password:
                    usuario_logueado = administrador
                    rol = "administrador"
                    break

        if usuario_logueado:
            print(f"Usuario y contraseña correcta : {usuario_logueado.nombre} ")
            self.redirigir_rol(usuario_logueado, rol)
        else:
            print(f"Usuario o contraseña incorrecta, {usuario_logueado.nombre}")
            return self.menu()

    def redirigir_rol(self, usuario, rol):
        if rol == "cliente":
            return self.menu_cliente(usuario)
        elif rol == "empleado":
            return self.menu_empleado(usuario)
        elif rol == "administrador":
            return self.menu_administrador(usuario)
        

    def menu_cliente(self, cliente_actual):
        while True:
            print("\nBIENVENIDO AL MENU CLIENTE")
            print("La lista de opciones es la siguiente: ")
            print("1. Crear reservas")
            print("2. Consultar reservas")
            print("3. Editar reservas")
            print("4. Cancelar reservas")

    def menu_empleado(self, empleado_actual):
        while True:
            print("\nBIENVENIDO AL MENU EMPLEADO")
            print("1. Registro entrada")
            print("2. Registrar salida")
            print("3. Consultar reservas")
            print("4. Actualizar disponibilidad")
            print("5. Registrar mantenimiento")

    def menu_administrador(self, administrador_actual):
        while True:
            print("\nBIENVENIDO AL MENU ADMINISTRADOR")
            print("1. Crear usuario")
            print("2. Modificar usuario")
            print("3. Eliminar usuario")
            print("4. Generar reportes")


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