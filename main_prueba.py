from cancha import Cancha
from establecimiento import Establecimiento
from horario import Horario
from reservas import Reservas
from tarifa import Tarifa
import usuarios as US
from efectivo import Efectivo
from tarjeta import Tarjeta
from tranferencia import Transferencia
from pago import Pago

class Principal:
    def __init__(self):
        # --- DATOS DEL ESTABLECIMIENTO ---
        self.establecimiento = Establecimiento(
            id_establecimiento=1,
            nombre_establecimiento="Complejo Deportivo El Golazo",
            ubicación="Av. Principal Calle 100",
        )
        
        # --- LISTAS DEL SISTEMA ---
        self.lista_canchas = []
        self.lista_clientes = []
        self.lista_reservas = []
        self.lista_empleados = []
        self.lista_administradores = []

    # ==========================================
    # LOGICA DE CANCHAS Y RESERVAS (Integrada)
    # ==========================================
    def registrar_cancha_prueba(self):
        print("\n--- Configurando Cancha y Tarifa de Prueba ---")
        tarifa_base = Tarifa(
            id_tarifa=1, valor_hora=50000, dias_semana="Fines de semana",
            valor_dia=10000, valor_ubicacion=5000, valor_tipo_jornada=15000,
        )
        cancha_nueva = Cancha(
            id_cancha=101, nombre_cancha="Cancha Sintética 1",
            precio=tarifa_base.calcular_tarifa(), horario="08:00 - 22:00", tipo_cancha="Fútbol 5",
        )
        self.establecimiento.agregar_cancha(cancha_nueva)
        print("Cancha y tarifa añadidas correctamente al establecimiento.")

    def ver_canchas(self):
        print(f"\n--- Establecimiento: {self.establecimiento.nombre_establecimiento} ---")
        print(f"Ubicación: {self.establecimiento.ubicación}")
        if not self.establecimiento.lista_canchas:
            print("No hay canchas registradas todavía (Pide a un Admin que registre una).")
            return False
        for can in self.establecimiento.lista_canchas:
            print(f"• Cancha: {can.nombre_cancha} | Tipo: {can.tipo_cancha} | Precio Base: ${can.precio:,.2f}")
        return True

    def crear_reserva_sistema(self, cliente_actual):
        print("\n--- Creando Nueva Reserva ---")
        if not self.ver_canchas():
            return

        id_res = len(self.lista_reservas) + 1
        fecha_apt = input("\nFecha apartada (YYYY-MM-DD): ")
        h_inicio = input("Hora de inicio (Ej: 18:00): ")
        h_final = input("Hora final (Ej: 19:00): ")
        dur = float(input("Duración en horas (Ej: 1.0): "))

        # Tomamos el precio de la primera cancha como ejemplo
        precio_hora = self.establecimiento.lista_canchas[0].precio

        nueva_reserva = Reservas(
            id_reserva=id_res, fecha_apartada=fecha_apt, hora_inicio=h_inicio,
            hora_final=h_final, duracion=dur, estado="Pendiente",
            total_reserva=0.0, abono=0.0,
        )
        
        nueva_reserva.calcular(precio_hora)
        print(f"\nEl total de la reserva es: ${nueva_reserva.total_reserva:,.2f}")
        abono_ingresado = float(input("Ingrese el valor del abono a pagar ahora: "))
        
        # --- INTEGRACIÓN DE LAS CLASES DE PAGO ---
        print("\n--- SELECCIONE UN MÉTODO DE PAGO ---")
        print("1. Efectivo")
        print("2. Tarjeta")
        print("3. Transferencia")
        opc_pago = int(input("Ingrese el método de pago (1/2/3): "))

        pago_valido = False
        comprobante_ingresado = "N/A"

        if opc_pago == 1:
            monto_rec = float(input("\nIngrese el monto recibido en efectivo: "))
            # Instanciamos la clase Efectivo
            pago_efectivo = Efectivo(id_metodopago=1, tipo_pago="Efectivo", descripcion="Pago en caja", 
                                     id_efectivo=len(self.lista_pagos)+1, monto_recibido=monto_rec, 
                                     cambio=0.0, estado="Pendiente")
            
            pago_valido = pago_efectivo.validarPago(abono_ingresado)
            comprobante_ingresado = f"EFECTIVO-{id_res}"
            
        elif opc_pago == 2:
            tipo_tarjeta = input("\nTipo de tarjeta (Visa/Mastercard): ")
            titular = input("Nombre del titular: ")
            vencimiento = input("Fecha de vencimiento (MM/AA): ")
            cvv = input("Código de seguridad: ")
            
            # Instanciamos la clase Tarjeta
            pago_tarjeta = Tarjeta(id_metodopago=2, tipo_pago="Tarjeta", descripcion="Pago en datáfono", 
                                   id_tarjeta=len(self.lista_pagos)+1, tipo_tarjeta=tipo_tarjeta, 
                                   titular=titular, fecha_vencimiento=vencimiento, codigo_seguridad=cvv)
            
            pago_valido = pago_tarjeta.validarTarjeta()
            comprobante_ingresado = input("Ingrese el número de comprobante (voucher) del datáfono: ")
            
        elif opc_pago == 3:
            banco = input("\nBanco de origen: ")
            estado_trans = "completada" # Para el ejercicio asumimos que pasó exitosamente
            
            # Instanciamos la clase Transferencia
            pago_transferencia = Transferencia(id_metodopago=3, tipo_pago="Transferencia", descripcion="Transferencia bancaria", 
                                               id_transferencia=len(self.lista_pagos)+1, banco_origen=banco, 
                                               fecha=fecha_apt, valor=abono_ingresado, estado=estado_trans)
            
            pago_valido = pago_transferencia.validarTransferencia()
            comprobante_ingresado = input("Ingrese el número de comprobante de la transferencia: ")
            
        else:
            print("Opción de pago inválida.")
            return

        # --- VALIDACIÓN FINAL ---
        if not pago_valido:
            print("\n El pago no pudo ser validado. Cancelando el proceso de reserva...")
            return
        nueva_reserva.abono = abono_ingresado

        nuevo_pago = Pago(
            fecha_pago=fecha_apt,
            valor=abono_ingresado,
            comprobante=comprobante_ingresado,
            estado="Registrado"
        )
        
        nuevo_pago.registrar_Pago()
        nuevo_pago.reserva_reconfirmada(nueva_reserva)
        
        saldo_pendiente = nuevo_pago.calcularTotal(nueva_reserva)
        print(f"\nSaldo pendiente de la reserva: ${saldo_pendiente:,.2f}")

        self.lista_pagos.append(nuevo_pago)
        self.lista_reservas.append(nueva_reserva)
        print(f"✓ Reserva creada con éxito para {cliente_actual.nombre}.")

    # ==========================================
    # CRUD DE USUARIOS 
    # ==========================================
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
            
        elif op == 2:
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

        elif op == 3:
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

    def modificar_usuario_administradores(self):
        # ... (Tu código de modificar_usuario_administradores queda igual)
        print("Modificando administrador...")

    def modificar_usuario_clientes(self, cliente_actual):
        print("\nBIENVENIDO A LA MODIFICACION DE USUARIOS")
        opc = int(input("Ingrese el dato que desea modificar: 1. Nombre 2. Apellido 3. Telefono 4. Correo 5. Password 6. Cancelar: "))

        if opc == 1:
            cliente_actual.nombre = input("\nIngrese el nuevo nombre: ")
            print("\nNombre modificado exitosamente.")
        elif opc == 2:
            cliente_actual.apellido = input("Ingrese el nuevo apellido: ")
            print("\nApellido modificado exitosamente.")
        elif opc == 3:
            cliente_actual.telefono = input("Ingrese el nuevo telefono: ")
            print("\nTelefono modificado exitosamente.")
        elif opc == 4:
            cliente_actual.correo = input("Ingrese el nuevo correo: ")
            print("\nCorreo modificado exitosamente.")
        elif opc == 5:
            cliente_actual.password = input("Ingrese el nuevo password: ")
            print("\nPassword modificado exitosamente.")

    def eliminar_usuario(self):
        # ... (Tu código de eliminar_usuario queda igual)
        print("Eliminando usuario...")

    # ==========================================
    # LOGIN Y REDIRECCIÓN
    # ==========================================
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
            print("Usuario o contraseña incorrecta.")
        
    def redirigir_rol(self, usuario, rol):
        if rol == "cliente":
            self.menu_cliente(usuario)
        elif rol == "empleado":
            self.menu_empleado(usuario)
        elif rol == "administrador":
            self.menu_administrador(usuario)
            
    # ==========================================
    # FUNCIONES DE GESTIÓN DE RESERVAS (Para conectar con usuarios.py)
    # ==========================================
    def consultar_mis_reservas(self, cliente):
        print(f"\n--- RESERVAS DE {cliente.nombre.upper()} ---")
        encontradas = False
        for res in self.lista_reservas:
            # Validamos si la reserva pertenece a este cliente verificando la lista_clinte
            if hasattr(res, 'cliente_asignado') and res.cliente_asignado.documento == cliente.documento:
                print(f"ID: {res.id_reserva} | Fecha: {res.fecha_apartada} | Horario: {res.hora_inicio} a {res.hora_final} | Estado: {res.estado}")
                encontradas = True
        
        if not encontradas:
            print("No tienes reservas registradas actualmente.")

    def cancelar_mis_reservas(self, cliente):
        self.consultar_mis_reservas(cliente)
        id_cancelar = int(input("\nIngrese el ID de la reserva que desea cancelar (0 para salir): "))
        if id_cancelar == 0: return

        for res in self.lista_reservas:
            if hasattr(res, 'cliente_asignado') and res.cliente_asignado.documento == cliente.documento:
                if res.id_reserva == id_cancelar:
                    res.estado = "Cancelada"
                    print("✓ Reserva cancelada exitosamente.")
                    return
        print("ID de reserva no encontrado o no pertenece a tu cuenta.")

    def editar_mis_reservas(self, cliente):
        self.consultar_mis_reservas(cliente)
        id_editar = int(input("\nIngrese el ID de la reserva a editar (0 para salir): "))
        if id_editar == 0: return

        for res in self.lista_reservas:
            if hasattr(res, 'cliente_asignado') and res.cliente_asignado.documento == cliente.documento and res.id_reserva == id_editar:
                print("1. Modificar fecha")
                print("2. Modificar horario")
                opc = int(input("¿Qué deseas editar?: "))
                if opc == 1:
                    res.fecha_apartada = input("Nueva fecha (YYYY-MM-DD): ")
                elif opc == 2:
                    res.hora_inicio = input("Nueva hora de inicio: ")
                    res.hora_final = input("Nueva hora final: ")
                print("✓ Reserva actualizada.")
                return
        print("Reserva no encontrada.")

    # ==========================================
    # FUNCIONES DE EMPLEADO (Canchas y control general)
    # ==========================================
    def mostrar_todas_las_reservas(self):
        print("\n--- TODAS LAS RESERVAS DEL SISTEMA ---")
        if not self.lista_reservas:
            print("No hay reservas en el sistema.")
        for res in self.lista_reservas:
            cliente_nom = res.cliente_asignado.nombre if hasattr(res, 'cliente_asignado') else "Desconocido"
            print(f"Reserva #{res.id_reserva} | Cliente: {cliente_nom} | Fecha: {res.fecha_apartada} | Estado: {res.estado}")

    def actualizar_estado_cancha(self):
        self.ver_canchas()
        id_c = int(input("\nIngrese el ID de la cancha a actualizar: "))
        for can in self.establecimiento.lista_canchas:
            if can.id_cancha == id_c:
                nuevo = input("Ingrese el nuevo estado (Disponible/Ocupada/Mantenimiento): ")
                can.actualizarEstado(nuevo)
                return
        print("Cancha no encontrada.")

    def registrar_mantenimiento_cancha(self):
        self.ver_canchas()
        id_c = int(input("\nIngrese el ID de la cancha en mantenimiento: "))
        for can in self.establecimiento.lista_canchas:
            if can.id_cancha == id_c:
                can.actualizarEstado("Mantenimiento")
                print(f"✓ La cancha '{can.nombre_cancha}' ahora está inhabilitada por mantenimiento.")
                return
        print("Cancha no encontrada.")

    # ==========================================
    # MENUS ESPECIFICOS POR ROL
    # ==========================================
    def menu_cliente(self, cliente_actual):
        while True:
            print(f"\n--- MENU CLIENTE: {cliente_actual.nombre} ---")
            print("1. Ver canchas disponibles")
            print("2. Crear reserva")
            print("3. Consultar mis reservas")
            print("4. Editar mis reservas")
            print("5. Cancelar reservas")
            print("6. Modificar mi perfil")
            print("7. Cerrar sesión")

            opc = int(input("Ingrese una opción: "))

            if opc == 1:
                self.ver_canchas()
            elif opc == 2:
                self.crear_reserva_sistema(cliente_actual)
            elif opc == 3:
                print("Consultando reservas...")
            elif opc == 4:
                print("Editando reservas...")
            elif opc == 5:
                print("Cancelando reservas...")
            elif opc == 6:
                self.modificar_usuario_clientes(cliente_actual)
            elif opc == 7:
                print("Cerrando sesión...")
                break

    def menu_empleado(self, empleado_actual):
        while True:
            print(f"\n--- MENU EMPLEADO: {empleado_actual.nombre} ---")
            print("1. Registro entrada")
            print("2. Registrar salida")
            print("3. Consultar reservas del sistema")
            print("4. Actualizar disponibilidad")
            print("5. Registrar mantenimiento")
            print("6. Cerrar sesión")

            opc = int(input("Ingrese una opción: "))

            if opc == 6:
                print("Cerrando sesión...")
                break
            # Resto de validaciones...

    def menu_administrador(self, administrador_actual):
        while True:
            print(f"\n--- MENU ADMINISTRADOR: {administrador_actual.nombre} ---")
            print("1. Crear usuario en el sistema")
            print("2. Modificar usuario")
            print("3. Eliminar usuario")
            print("4. Generar reportes")
            print("5. Registrar cancha y tarifa (Configuración)")
            print("6. Ver canchas registradas")
            print("7. Cerrar sesión")

            opc = int(input("Ingrese una opción: "))
            
            if opc == 1:
                self.crear_usuario()
            elif opc == 2:
                self.modificar_usuario_administradores()
            elif opc == 3:
                self.eliminar_usuario()
            elif opc == 4:
                print("Generando reportes...")
            elif opc == 5:
                self.registrar_cancha_prueba()
            elif opc == 6:
                self.ver_canchas()
            elif opc == 7:
                print("Cerrando sesión...")
                break

    # ==========================================
    # MENU PRINCIPAL (Raíz)
    # ==========================================
    def menu(self):
        while True:
            print("\n========================================")
            print("   SISTEMA DE ALQUILER DE CANCHAS       ")
            print("========================================")
            print("1. Crear usuario (Registro rápido)")
            print("2. Ingresar al sistema (Login)")
            print("3. Mostrar clientes registrados")
            print("4. Salir del programa")
            
            opc = int(input("Ingrese una opción: "))
            
            if opc == 1:
                self.crear_usuario()
            elif opc == 2:
                self.ingresar_usuario()
            elif opc == 3:
                for i in self.lista_clientes:
                    print(f"Cliente: {i.nombre} {i.apellido} - Tel: {i.telefono}")
            elif opc == 4:
                print("Saliendo del sistema...")
                break

if __name__ == "__main__":
    app = Principal() 
    app.menu()