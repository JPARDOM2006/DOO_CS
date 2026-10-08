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

#CREACION DE USUARIOS
    def crear_usuario(self):
        op = int(input("\nIngrese el tipo de usuario que desea crear: 1. Cliente 2. Empleado 3. Administrador: "))
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
            print("\nCliente creado exitosamente.")
            
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
            print("\nEmpleado creado exitosamente.")

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
            print("\nAdministrador creado exitosamente.")


#MODIFICACION DE USUARIOS ADMINISTRADORES
    def modificar_usuario_administradores(self):
        print("\nBIENVENIDO A LA MODIFICACION DE USUARIOS")
        op = int(input("Ingrese el tipo de usuario que desea modificar: 1. Cliente 2. Empleado 3. Administrador: "))

        if op == 1:
            nombre = input("\nIngrese el nombre del cliente que desea modificar: ")
            
            for cliente in self.lista_clientes:
                print("\nCliente encontrado: ", cliente.nombre, cliente.apellido, cliente.documento)
                opc = int(input("Ingrese el dato que desea modificar: 1. Nombre 2. Apellido 3. Documento 4. Telefono 5. Correo 6. Password: "))
                if opc == 1:
                    cliente.nombre = input("\nIngrese el nuevo nombre del cliente: ")
                if opc == 2:
                    cliente.apellido = input("\nIngrese el nuevo apellido del cliente: ")
                if opc == 3:
                    cliente.documento = input("\nIngrese el nuevo documento del cliente: ")
                if opc == 4:
                    cliente.telefono = input("\nIngrese el nuevo telefono del cliente: ")
                if opc == 5:
                    cliente.correo = input("\nIngrese el nuevo correo del cliente: ")
                if opc == 6:
                    cliente.password = input("\nIngrese el nuevo password del cliente: ")

        if op == 2:
            nombre = input("\nIngrese el nombre del empleado que desea modificar: ")
            
            for empleado in self.lista_empleados:
                print("\nEmpleado encontrado: ", empleado.nombre, empleado.apellido, empleado.documento)
                opc = int(input("Ingrese el dato que desea modificar: 1. Nombre 2. Apellido 3. Documento 4. Telefono 5. Correo 6. Password 7. Cargo 8. Salario 9. Horario 10. Direccion: "))
                if opc == 1:
                    empleado.nombre = input("\nIngrese el nuevo nombre del empleado: ")
                if opc == 2:
                    empleado.apellido = input("\nIngrese el nuevo apellido del empleado: ")
                if opc == 3:
                    empleado.documento = input("\nIngrese el nuevo documento del empleado: ")
                if opc == 4:
                    empleado.telefono = input("\nIngrese el nuevo telefono del empleado: ")
                if opc == 5:
                    empleado.correo = input("\nIngrese el nuevo correo del empleado: ")
                if opc == 6:
                    empleado.password = input("\nIngrese el nuevo password del empleado: ")
                if opc == 7:
                    empleado.cargo = input("\nIngrese el nuevo cargo del empleado: ")
                if opc == 8:
                    empleado.salario = input("\nIngrese el nuevo salario del empleado: ")
                if opc == 9:
                    empleado.horario = input("\nIngrese el nuevo horario del empleado: ")
                if opc == 10:
                    empleado.direccion = input("\nIngrese la nueva direccion del empleado: ")

        if op == 3:
            nombre = input("\nIngrese el nombre del administrador que desea modificar: ")
            
            for administrador in self.lista_administradores:
                print("\nAdministrador encontrado: ", administrador.nombre, administrador.apellido, administrador.documento)
                opc = int(input("Ingrese el dato que desea modificar: 1. Nombre 2. Apellido 3. Documento 4. Telefono 5. Correo 6. Password 7. Cargo 8. Salario 9. Direccion: "))
                if opc == 1:
                    administrador.nombre = input("\nIngrese el nuevo nombre del administrador: ")
                if opc == 2:
                    administrador.apellido = input("\nIngrese el nuevo apellido del administrador: ")
                if opc == 3:
                    administrador.documento = input("\nIngrese el nuevo documento del administrador: ")
                if opc == 4:
                    administrador.telefono = input("\nIngrese el nuevo telefono del administrador: ")
                if opc == 5:
                    administrador.correo = input("\nIngrese el nuevo correo del administrador: ")
                if opc == 6:
                    administrador.password = input("\nIngrese el nuevo password del administrador: ")
                if opc == 7:
                    administrador.cargo = input("\nIngrese el nuevo cargo del administrador: ")
                if opc == 8:
                    administrador.salario = input("\nIngrese el nuevo salario del administrador: ")
                if opc == 9:
                    administrador.direccion = input("\nIngrese la nueva direccion del administrador: ") 

#MODIFICACION DE USUARIOS CLIENTES
    def modificar_usuario_clientes(self, cliente_actual):
        print("\nBIENVENIDO A LA MODIFICACION DE USUARIOS")
        opc = int(input("Ingrese el dato que desea modificar: 1. Nombre 2. Apellido 3. Telefono 4. Correo 5. Password 6. Volver al menu: "))

        if opc == 1:
            nuevo_nombre = input("\nIngrese el nuevo nombre del cliente: ")
            cliente_actual.nombre = nuevo_nombre
            print("\nNombre modificado exitosamente.")
        if opc == 2:
            nuevo_apellido = input("Ingrese el nuevo apellido del cliente: ")
            cliente_actual.apellido = nuevo_apellido
            print("\nApellido modificado exitosamente.")
        if opc == 3:
            nuevo_telefono = input("Ingrese el nuevo telefono del cliente: ")
            cliente_actual.telefono = nuevo_telefono
            print("\nTelefono modificado exitosamente.")
        if opc == 4:
            nuevo_correo = input("Ingrese el nuevo correo del cliente: ")
            cliente_actual.correo = nuevo_correo
            print("\nCorreo modificado exitosamente.")
        if opc == 5:
            nuevo_password = input("Ingrese el nuevo password del cliente: ")
            cliente_actual.password = nuevo_password
            print("\nPassword modificado exitosamente.")
        if opc == 6:
            return self.menu()

    def eliminar_usuario(self):
        print("\nBIENVENIDO A LA ELIMINACION DE USUARIOS")
        op = int(input("Ingrese el tipo de usuario que desea eliminar: 1. Cliente 2. Empleado 3. Administrador: "))

        if op == 1:
            nombre = input("\nIngrese el nombre del cliente que desea eliminar: ")
            for cliente in self.lista_clientes:
                if cliente.nombre == nombre:
                    self.lista_clientes.remove(cliente)
                    print("\nCliente eliminado exitosamente.")
                    break
            else:
                print("\nCliente no encontrado.")

        if op == 2:
            nombre = input("\nIngrese el nombre del empleado que desea eliminar: ")
            for empleado in self.lista_empleados:
                if empleado.nombre == nombre:
                    self.lista_empleados.remove(empleado)
                    print("\nEmpleado eliminado exitosamente.")
                    break
            else:
                print("\nEmpleado no encontrado.")

        if op == 3:
            nombre = input("\nIngrese el nombre del administrador que desea eliminar: ")
            for administrador in self.lista_administradores:
                if administrador.nombre == nombre:
                    self.lista_administradores.remove(administrador)
                    print("\nAdministrador eliminado exitosamente.")
                    break
            else:
                print("\nAdministrador no encontrado.")


    def ingresar_usuario(self):
        print("\nBIENVENIDO AL INGRESO DE USUARIOS")
        user = input("\nIngrese su correo o nombre, ingresados en el registro: ")
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
                    print(f"Usuario y contraseña correcta : {usuario_logueado} ")
                    self.redirigir_rol(usuario_logueado, rol)
                    break

        if not usuario_logueado:
            for administrador in self.lista_administradores:
                if (administrador.correo == user or administrador.nombre == user) and administrador.password == password:
                    usuario_logueado = administrador
                    rol = "administrador"
                    print(f"Usuario y contraseña correcta : {usuario_logueado} ")
                    self.redirigir_rol(usuario_logueado, rol)
                    break

        if usuario_logueado:
            print(f"Usuario y contraseña correcta : {usuario_logueado.nombre} ")
            self.redirigir_rol(usuario_logueado, rol)
        else:
            print("Usuario o contraseña incorrecta, digite de nuevo su nombre y contraseña")
            return self.menu()
        

#REDIRECCION DE USUARIO SEGUN SU ROL
    def redirigir_rol(self, usuario, rol):
        if rol == "cliente":
            return self.menu_cliente(usuario)
        elif rol == "empleado":
            return self.menu_empleado(usuario)
        elif rol == "administrador":
            return self.menu_administrador(usuario)
        
#MENU SEGUN ROLES
    def menu_cliente(self, cliente_actual):
        while True:
            print("\nBIENVENIDO AL MENU CLIENTE")
            print("La lista de opciones es la siguiente: ")
            print("1. Crear reservas")
            print("2. Consultar reservas")
            print("3. Editar reservas")
            print("4. Cancelar reservas")
            print("5. Modificar usuario")

            opc = int(input("Ingrese una opción: "))

            if opc == 1:
                cliente_actual.crear_reservas()
            elif opc == 2:
                cliente_actual.consultar_reservas()
            elif opc == 3:
                cliente_actual.editar_reservas()
            elif opc == 4:
                cliente_actual.cancelar_reservas()
            elif opc == 5:
                self.modificar_usuario_clientes()

    def menu_empleado(self, empleado_actual):
        while True:
            print("\nBIENVENIDO AL MENU EMPLEADO")
            print("1. Registro entrada")
            print("2. Registrar salida")
            print("3. Consultar reservas")
            print("4. Actualizar disponibilidad")
            print("5. Registrar mantenimiento")

            opc = int(input("Ingrese una opción: "))

            if opc == 1:
                empleado_actual.registrar_entrada()
            if opc == 2:
                empleado_actual.registrar_salida()
            if opc == 3:
                empleado_actual.consultar_reservas()
            if opc == 4:
                empleado_actual.actualizar_disponibilidad()
            if opc == 5:
                empleado_actual.registrar_mantenimiento()

    def menu_administrador(self, administrador_actual):
        while True:
            print("\nBIENVENIDO AL MENU ADMINISTRADOR")
            print("1. Crear usuario")
            print("2. Modificar usuario")
            print("3. Eliminar usuario")
            print("4. Generar reportes")

            opc = int(input("Ingrese una opción: "))
            
            if opc == 1:
                self.crear_usuario()
            elif opc == 2:
                self.modificar_usuario_administradores()
            elif opc == 3:
                self.eliminar_usuario()
            elif opc == 4:
                self.generar_reportes()

    def menu(self):

        while True:
            print("\nBIENVENIDO AL MENU PRINCIPAL")
            print("1. Crear usuario")
            print("2. Ingresar como usuario")
            print("3. Mostrar el nombre de los clientes registrados")
            opc = int(input("Ingrese una opción: "))
            if opc == 1:
                self.crear_usuario()

            elif opc == 2:
                self.ingresar_usuario()

            elif opc==3:
                for i in self.lista_clientes:
                    print("\n", i.nombre, i.apellido, i.telefono)

if __name__ == "__main__":
    a = Principal() 
    a.menu()