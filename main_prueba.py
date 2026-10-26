from cancha import Cancha
from establecimiento import Establecimiento
from reservas import Reservas
from tarifa import Tarifa
import usuarios as US
from efectivo import Efectivo
from tarjeta import Tarjeta
from tranferencia import Transferencia
from pago import Pago
import sqlite3
import datetime
from base_datos import inicializar_base_datos, DB_NAME


class Principal:
    def __init__(self):
        inicializar_base_datos()
        self._crear_establecimiento_defecto()
        self.establecimiento = Establecimiento(
            id_establecimiento=1,
            nombre_establecimiento="Complejo Deportivo El Golazo",
            ubicación="Av. Principal Calle 100",
        )
        self.cargar_canchas_desde_db()

    def _crear_establecimiento_defecto(self):
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM establecimientos")
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute(
                    "INSERT INTO establecimientos (nombre_establecimiento, ubicacion) VALUES (?, ?)",
                    ("Complejo Deportivo El Golazo", "Av. Principal Calle 100"),
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
        finally:
            if conn:
                conn.close()

    def cargar_canchas_desde_db(self):
        self.establecimiento.lista_canchas = []
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre_cancha, tipo_cancha, precio, horario, estado FROM canchas")
            for row in cursor.fetchall():
                can = Cancha(id_cancha=row[0], nombre_cancha=row[1], precio=row[3], horario=row[4], tipo_cancha=row[2])
                can.estado = row[5]
                self.establecimiento.lista_canchas.append(can)
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
        finally:
            if conn:
                conn.close()

    def crear_cancha_nueva(self):
        print("\n--- REGISTRO DE NUEVA CANCHA DESDE CERO ---")
        conn = None
        try:
            nombre = input("Ingrese el nombre de la cancha (Ej: Cancha Múltiple 1): ")
            tipo = input("Ingrese el tipo de cancha (Ej: Fútbol 5, Baloncesto): ")
            horario = input("Ingrese el horario de disponibilidad (Ej: 08:00 - 22:00): ")

            print("\n-- Configuración de Tarifa Base --")
            valor_h = float(input("Valor por hora ($): "))
            dias = input("Días de aplicación (Ej: Lunes a Domingo): ")
            valor_d = float(input("Recargo por día especial o fin de semana ($): "))

            tarifa_nueva = Tarifa(id_tarifa=0, valor_hora=valor_h, dias_semana=dias, valor_dia=valor_d, valor_ubicacion=0, valor_tipo_jornada=0)
            precio_total = tarifa_nueva.calcular_tarifa()

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tarifas (valor_hora, dias_semana, valor_dia, valor_ubicacion, valor_tipo_jornada) VALUES (?, ?, ?, ?, ?)", (valor_h, dias, valor_d, 0, 0))
            id_tarifa_db = cursor.lastrowid
            cursor.execute("INSERT INTO canchas (id_establecimiento, id_tarifa, nombre_cancha, tipo_cancha, precio, horario, estado) VALUES (?, ?, ?, ?, ?, ?, ?)", (1, id_tarifa_db, nombre, tipo, precio_total, horario, "Disponible"))
            conn.commit()
            self.cargar_canchas_desde_db()
            print(f"\n✓ Cancha '{nombre}' registrada exitosamente con un precio base de ${precio_total:,.2f}.")
        except ValueError:
            print("\n[ERROR] Debes ingresar un valor numérico válido para el precio por hora y el recargo por día.")
            print("La cancha no fue registrada. Inténtalo nuevamente.")
        except EOFError:
            print("\n[ERROR] No se pudo leer la entrada por teclado.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def ver_canchas(self):
        self.cargar_canchas_desde_db()
        print(f"\n--- Establecimiento: {self.establecimiento.nombre_establecimiento} ---")
        print(f"Ubicación: {self.establecimiento.ubicación}")
        if not self.establecimiento.lista_canchas:
            print("No hay canchas registradas todavía.")
            return False
        for can in self.establecimiento.lista_canchas:
            print(f"• ID: {can.id_cancha} | Cancha: {can.nombre_cancha} | Tipo: {can.tipo_cancha} | Precio Base: ${can.precio:,.2f} | Horario: {can.horario} | Estado: {getattr(can,'estado','Disponible')}")
        return True

    def crear_reserva_sistema(self, cliente_actual):
        print("\n--- Creando Nueva Reserva ---")
        if not self.ver_canchas():
            return
        conn = None
        try:
            fecha_apt = input("\nFecha apartada (YYYY-MM-DD): ")
            h_inicio = input("Hora de inicio (Ej: 18:00): ")
            h_final = input("Hora final (Ej: 19:00): ")
            dur = float(input("Duración en horas (Ej: 1.0): "))

            if not self.establecimiento.lista_canchas:
                print("No hay canchas disponibles.")
                return
            precio_hora = self.establecimiento.lista_canchas[0].precio
            id_cancha_res = self.establecimiento.lista_canchas[0].id_cancha
            id_cliente_res = getattr(cliente_actual, 'id_usuario')

            if id_cliente_res is None:
                print("[ERROR] No se pudo identificar el cliente en sesión.")
                return

            nueva_reserva = Reservas(fecha_apt, h_inicio, h_final, dur, "Pendiente", 0.0, 0.0)
            nueva_reserva.calcular(precio_hora)
            print(f"\nEl total de la reserva es: ${nueva_reserva.total_reserva:,.2f}")
            abono_ingresado = float(input("Ingrese the valor del abono a pagar ahora: "))

            print("\n--- SELECCIONE UN MÉTODO DE PAGO ---")
            print("1. Efectivo")
            print("2. Tarjeta")
            print("3. Transferencia")
            opc_pago = int(input("Ingrese el método de pago (1/2/3): "))

            pago_valido = False
            comprobante_ingresado = "N/A"
            id_metodo_db = opc_pago

            if opc_pago == 1:
                monto_rec = float(input("\nIngrese el monto recibido en efectivo: "))
                pago_efectivo = Efectivo(id_metodopago=1, tipo_pago="Efectivo", descripcion="Pago en caja", id_efectivo=1, monto_recibido=monto_rec, cambio=0.0, estado="Pendiente")
                pago_valido = pago_efectivo.validarPago(abono_ingresado)
                comprobante_ingresado = f"EFECTIVO-{datetime.datetime.now().strftime('%H%M%S')}"
            elif opc_pago == 2:
                tipo_tarjeta = input("\nTipo de tarjeta (Visa/Mastercard): ")
                titular = input("Nombre del titular: ")
                vencimiento = input("Fecha de vencimiento (MM/AA): ")
                cvv = input("Código de seguridad: ")
                pago_tarjeta = Tarjeta(id_metodopago=2, tipo_pago="Tarjeta", descripcion="Pago en datáfono", id_tarjeta=1, tipo_tarjeta=tipo_tarjeta, titular=titular, fecha_vencimiento=vencimiento, codigo_seguridad=cvv)
                pago_valido = pago_tarjeta.validarTarjeta()
                comprobante_ingresado = input("Ingrese el número de comprobante (voucher) del datáfono: ")
            elif opc_pago == 3:
                banco = input("\nBanco de origen: ")
                pago_transferencia = Transferencia(id_metodopago=3, tipo_pago="Transferencia", descripcion="Transferencia bancaria", id_transferencia=1, banco_origen=banco, fecha=fecha_apt, valor=abono_ingresado, estado="completada")
                pago_valido = pago_transferencia.validarTransferencia()
                comprobante_ingresado = input("Ingrese el número de comprobante de la transferencia: ")
            else:
                print("Opción de pago inválida.")
                return

            if not pago_valido:
                print("\nEl pago no pudo ser validado. Cancelando el proceso de reserva...")
                return

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reservas (id_cliente, id_cancha, fecha_apartada, hora_inicio, hora_final, duracion, estado, total_reserva, abono) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (id_cliente_res, id_cancha_res, fecha_apt, h_inicio, h_final, dur, "Pendiente", nueva_reserva.total_reserva, abono_ingresado))
            id_reserva_db = cursor.lastrowid
            cursor.execute("INSERT INTO pagos (id_reserva, id_metodo_pago, fecha_pago, valor, comprobante, estado) VALUES (?, ?, ?, ?, ?, ?)", (id_reserva_db, id_metodo_db, fecha_apt, abono_ingresado, comprobante_ingresado, "Registrado"))
            cursor.execute("UPDATE reservas SET estado = 'Confirmada' WHERE id = ?", (id_reserva_db,))
            conn.commit()

            nuevo_pago = Pago(fecha_pago=fecha_apt, valor=abono_ingresado, comprobante=comprobante_ingresado, estado="Registrado")
            print("Reserva reconfirmada con el pago")
            saldo_pendiente = nuevo_pago.calcularTotal(nueva_reserva)
            print(f"\nSaldo pendiente de la reserva: ${saldo_pendiente:,.2f}")
            print(f"✓ Reserva creada con éxito para {cliente_actual.nombre}.")
        except ValueError:
            print("\n[ERROR] Se ingresó a valor numérico incorrecto. La reserva no fue creada.")
        except EOFError:
            print("\n[ERROR] No se pudo leer la entrada por teclado.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def crear_usuario(self):
        conn = None
        try:
            op = int(input("\nIngrese el tipo de usuario que desea crear: 1. Cliente 2. Empleado 3. Administrador: "))
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            documento = input("Ingrese el documento: ")
            telefono = input("Ingrese el telefono: ")
            correo = input("Ingrese el correo: ")
            password = input("Ingrese el password: ")
            fecha_reg = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            if op == 1:
                print("\nBIENVENIDO A LA CREACION DE USUARIO DE CLIENTES")
                cursor.execute("INSERT INTO usuarios (nombre, apellido, documento, telefono, correo, password, tipo_usuario, fecha_registro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nombre, apellido, documento, telefono, correo, password, "cliente", fecha_reg))
                id_usuario = cursor.lastrowid
                cursor.execute("INSERT INTO clientes (id_usuario) VALUES (?)", (id_usuario,))
                conn.commit()
                print("\nCliente creado exitosamente.")
            elif op == 2:
                print("\nBIENVENIDO A LA CREACION DE USUARIO DE EMPLEADOS")
                cargo = input("Ingrese el cargo: ")
                salario = input("Ingrese el salario: ")
                horario = input("Ingrese el horario: ")
                direccion = input("Ingrese la direccion: ")
                cursor.execute("INSERT INTO usuarios (nombre, apellido, documento, telefono, correo, password, tipo_usuario, fecha_registro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nombre, apellido, documento, telefono, correo, password, "empleado", fecha_reg))
                id_usuario = cursor.lastrowid
                cursor.execute("INSERT INTO empleados (id_usuario, cargo, salario, horario, direccion) VALUES (?, ?, ?, ?, ?)", (id_usuario, cargo, salario, horario, direccion))
                conn.commit()
                print("\nEmpleado creado exitosamente.")
            elif op == 3:
                print("\nBIENVENIDO A LA CREACION DE USUARIO DE ADMINISTRADORES")
                cargo = input("Ingrese el cargo: ")
                salario = input("Ingrese el salario: ")
                direccion = input("Ingrese la direccion: ")
                cursor.execute("INSERT INTO usuarios (nombre, apellido, documento, telefono, correo, password, tipo_usuario, fecha_registro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nombre, apellido, documento, telefono, correo, password, "administrador", fecha_reg))
                id_usuario = cursor.lastrowid
                cursor.execute("INSERT INTO administradores (id_usuario, cargo, salario, direccion) VALUES (?, ?, ?, ?)", (id_usuario, cargo, salario, direccion))
                conn.commit()
                print("\nAdministrador creado exitosamente.")
            else:
                print("Opción inválida.")
        except ValueError:
            print("\n[ERROR] Debes ingresar un número para seleccionar el tipo de usuario.")
        except EOFError:
            print("\n[ERROR] No se pudo leer la entrada por teclado.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def ingresar_usuario(self):
        print("\nBIENVENIDO AL INGRESO DE USUARIOS")
        user = input("\nIngrese su correo o nombre, ingresados en el registro: ")
        password = input("Ingrese su contraseña: ")
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, documento, telefono, correo, password, tipo_usuario FROM usuarios WHERE (correo = ? OR nombre = ?) AND password = ?", (user, user, password))
            row = cursor.fetchone()
            if not row:
                print("Usuario o contraseña incorrecta.")
                return
            uid, nombre, apellido, documento, telefono, correo, pwd, tipo_usuario = row
            if tipo_usuario == "cliente":
                usuario_logueado = US.Cliente(nombre, apellido, documento, telefono, correo, pwd)
                usuario_logueado.id_usuario = uid
                print(f"Usuario y contraseña correcta : {usuario_logueado.nombre} ")
                self.redirigir_rol(usuario_logueado, "cliente")
            elif tipo_usuario == "empleado":
                usuario_logueado = US.Empleado(nombre, apellido, documento, telefono, correo, pwd, "", "", "", "")
                usuario_logueado.id_usuario = uid
                print(f"Usuario y contraseña correcta : {usuario_logueado.nombre} ")
                self.redirigir_rol(usuario_logueado, "empleado")
            elif tipo_usuario == "administrador":
                usuario_logueado = US.Administrador(nombre, apellido, documento, telefono, correo, pwd, "", "", "")
                usuario_logueado.id_usuario = uid
                print(f"Usuario y contraseña correcta : {usuario_logueado.nombre} ")
                self.redirigir_rol(usuario_logueado, "administrador")
            else:
                print("Usuario o contraseña incorrecta.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
        finally:
            if conn:
                conn.close()

    def redirigir_rol(self, usuario, rol):
        if rol == "cliente":
            self.menu_cliente(usuario)
        elif rol == "empleado":
            self.menu_empleado(usuario)
        elif rol == "administrador":
            self.menu_administrador(usuario)

    def consultar_mis_reservas(self, cliente):
        print(f"\n--- RESERVAS DE {cliente.nombre.upper()} ---")
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT r.id, r.fecha_apartada, r.hora_inicio, r.hora_final, r.estado, c.nombre_cancha FROM reservas r LEFT JOIN canchas c ON c.id = r.id_cancha WHERE r.id_cliente = ?", (getattr(cliente, 'id_usuario'),))
            rows = cursor.fetchall()
            if not rows:
                print("No tienes reservas registradas actualmente.")
                return
            for row in rows:
                print(f"ID: {row[0]} | Cancha: {row[5]} | Fecha: {row[1]} | Horario: {row[2]} a {row[3]} | Estado: {row[4]}")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
        finally:
            if conn:
                conn.close()

    def mostrar_todas_las_reservas(self):
        print("\n--- TODAS LAS RESERVAS DEL SISTEMA ---")
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT r.id, u.nombre, u.apellido, c.nombre_cancha, r.fecha_apartada, r.hora_inicio, r.hora_final, r.estado FROM reservas r LEFT JOIN usuarios u ON u.id = r.id_cliente LEFT JOIN canchas c ON c.id = r.id_cancha ORDER BY r.id")
            rows = cursor.fetchall()
            if not rows:
                print("No hay reservas en el sistema.")
                return
            for row in rows:
                print(f"Reserva #{row[0]} | Cliente: {row[1]} {row[2]} | Cancha: {row[3]} | Fecha: {row[4]} {row[5]}-{row[6]} | Estado: {row[7]}")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
        finally:
            if conn:
                conn.close()

    def generar_reportes(self):
        print("\n========================================")
        print("           REPORTE GENERAL DEL SISTEMA")
        print("========================================")
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(valor) FROM pagos")
            total = cursor.fetchone()[0]
            if total is None:
                total = 0.0
            print(f"\n[Recaudado] Total de dinero recaudado en pagos: ${total:,.2f}")
            cursor.execute("SELECT COUNT(*) FROM pagos")
            print(f"[Recaudado] Cantidad de pagos registrados: {cursor.fetchone()[0]}")
            print("\n[Reservas por estado]")
            cursor.execute("SELECT estado, COUNT(*) FROM reservas GROUP BY estado")
            rows_r = cursor.fetchall()
            if not rows_r:
                print("No hay reservas registradas en el sistema.")
            else:
                for e, c in rows_r:
                    print(f" - {e}: {c}")
                cursor.execute("SELECT COUNT(*) FROM reservas")
                print(f"Total de reservas: {cursor.fetchone()[0]}")
            print("\n[Usuarios registrados]")
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo_usuario='cliente'")
            print(f" - Clientes: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo_usuario='empleado'")
            print(f" - Empleados: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo_usuario='administrador'")
            print(f" - Administradores: {cursor.fetchone()[0]}")
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            print(f"Total de usuarios: {cursor.fetchone()[0]}")
            print("\n========================================")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
        finally:
            if conn:
                conn.close()

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
            try:
                opc = int(input("Ingrese una opción: "))
                if opc == 1: self.ver_canchas()
                elif opc == 2: self.crear_reserva_sistema(cliente_actual)
                elif opc == 3: self.consultar_mis_reservas(cliente_actual)
                elif opc == 7: print("Cerrando sesión..."); break
                else: print("Opción inválida.")
            except ValueError: print("\n[ERROR] Debes ingresar a número válido.")
            except EOFError: break

    def menu_empleado(self, empleado_actual):
        while True:
            print(f"\n--- MENU EMPLEADO: {empleado_actual.nombre} ---")
            print("1. Registro entrada")
            print("2. Registrar salida")
            print("3. Consultar reservas del sistema")
            print("4. Actualizar disponibilidad")
            print("5. Registrar mantenimiento")
            print("6. Cerrar sesión")
            try:
                opc = int(input("Ingrese una opción: "))
                if opc == 1: empleado_actual.registrar_entrada()
                elif opc == 2: empleado_actual.registrar_salida()
                elif opc == 3: empleado_actual.consultar_reservas(self)
                elif opc == 6: print("Cerrando sesión..."); break
                else: print("Opción inválida.")
            except ValueError: print("\n[ERROR] Debes ingresar a número válido.")
            except EOFError: break

    def menu_administrador(self, administrador_actual):
        while True:
            print(f"\n--- MENU ADMINISTRADOR: {administrador_actual.nombre} ---")
            print("1. Crear usuario en el sistema")
            print("2. Modificar usuario")
            print("3. Eliminar usuario")
            print("4. Generar reportes")
            print("5. Registrar una nueva cancha (Desde cero)")
            print("6. Ver canchas registradas")
            print("7. Cerrar sesión")
            try:
                opc = int(input("Ingrese una opción: "))
                if opc == 1: self.crear_usuario()
                elif opc == 4: administrador_actual.gestionar_reportes(self)
                elif opc == 5: administrador_actual.registrar_cancha(self)
                elif opc == 6: self.ver_canchas()
                elif opc == 7: print("Cerrando sesión..."); break
                else: print("Opción inválida.")
            except ValueError: print("\n[ERROR] Debes ingresar a número válido.")
            except EOFError: break

    def menu(self):
        while True:
            print("\n========================================")
            print("   SISTEMA DE ALQUILER DE CANCHAS       ")
            print("========================================")
            print("1. Crear usuario (Registro rápido)")
            print("2. Ingresar al sistema (Login)")
            print("3. Mostrar clientes registrados")
            print("4. Salir del programa")
            try:
                opc = int(input("Ingrese una opción: "))
                if opc == 1: self.crear_usuario()
                elif opc == 2: self.ingresar_usuario()
                elif opc == 3:
                    conn = None
                    try:
                        conn = sqlite3.connect(DB_NAME)
                        cursor = conn.cursor()
                        cursor.execute("SELECT nombre, apellido, telefono, correo FROM usuarios WHERE tipo_usuario='cliente'")
                        rows = cursor.fetchall()
                        if not rows: print("\nNo hay clientes registrados.")
                        else:
                            for i in rows: print(f"Cliente: {i[0]} {i[1]} - Tel: {i[2]} - Correo: {i[3]}")
                    finally:
                        if conn: conn.close()
                elif opc == 4: print("Saliendo del sistema..."); break
                else: print("Opción inválida.")
            except ValueError: print("\n[ERROR] Debes ingresar a número válido.")
            except EOFError: break


if __name__ == "__main__":
    app = Principal()
    app.menu()
