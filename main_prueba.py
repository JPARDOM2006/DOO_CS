from cancha import Cancha, CanchaBuilder
from establecimiento import Establecimiento, EstablecimientoBuilder
from reservas import Reservas
from tarifa import Tarifa
from horario import Horario, HorarioBuilder
import usuarios as US
from efectivo import Efectivo
from tarjeta import Tarjeta
from tranferencia import Transferencia, TransferenciaBuilder
from mantenimiento import Mantenimiento, MantenimientoBuilder
from pago import Pago
import sqlite3
import datetime
from base_datos import inicializar_base_datos, DB_NAME


class Principal:
    def __init__(self):
        inicializar_base_datos()
        self._crear_establecimiento_defecto()
        self.establecimiento = (EstablecimientoBuilder()
                                .set_nombre("Complejo Deportivo El Golazo")
                                .set_direccion("Av. Principal Calle 100")
                                .set_telefono("")
                                .set_horario("")
                                .build())
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
                can = (CanchaBuilder()
                       .set_id(row[0])
                       .set_nombre(row[1])
                       .set_tipo_superficie(row[2])
                       .set_precio_hora(row[3])
                       .set_horario(row[4])
                       .set_estado(row[5])
                       .build())
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
            tipo = input("Ingrese el tipo de cancha (Ej: Fútbol 5): ")
            horario_disp = input("Ingrese el horario de disponibilidad (Ej: 08:00 AM - 10:00 PM): ")

            print("\n-- Configuración de Horario y Tarifa --")
            dias_semana = input("Días de aplicación (Ej: Lunes a Domingo): ")
            jornada = input("Jornada (Diurna / Nocturna): ")
            h_inicio = input("Hora inicio franja (Ej: 06:00 PM): ")
            h_final = input("Hora final franja (Ej: 10:00 PM): ")
            valor_h = float(input("Valor por hora ($): "))
            valor_d = float(input("Valor recargo por día/fin de semana ($): "))

            # Instanciar Horario con valores de dinero y franjas (Patrón Builder)
            horario_obj = (HorarioBuilder()
                           .set_hora_inicio(h_inicio)
                           .set_hora_fin(h_final)
                           .set_dias_operacion(dias_semana)
                           .set_jornada(jornada)
                           .set_valor_hora(valor_h)
                           .set_recargo_dia(valor_d)
                           .build())
            # Instanciar Tarifa pasando el Horario (dependencia)
            tarifa_nueva = Tarifa(horario_obj)
            precio_total = tarifa_nueva.calcular_tarifa()

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tarifas (valor_hora, dias_semana, valor_dia, valor_ubicacion, valor_tipo_jornada) VALUES (?, ?, ?, ?, ?)",
                (valor_h, dias_semana, valor_d, 0, 0)
            )
            id_tarifa_db = cursor.lastrowid
            cursor.execute(
                "INSERT INTO canchas (id_establecimiento, id_tarifa, nombre_cancha, tipo_cancha, precio, horario, estado) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (1, id_tarifa_db, nombre, tipo, precio_total, horario_disp, "Disponible")
            )
            conn.commit()
            self.cargar_canchas_desde_db()
            print(f"\n✓ Cancha '{nombre}' registrada exitosamente con un precio base de ${precio_total:,.2f}.")
        except ValueError:
            print("\n[ERROR] Debes ingresar un valor numérico válido para el precio por hora y el recargo.")
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
            dia = int(input("Ingrese el día de este mes para la reserva: "))
            # Usamos datetime.date.today() para obtener año y mes actual
            hoy = datetime.date.today()
            anno = hoy.year
            mes = hoy.month
            # Validación de anticipación: la fecha debe ser estrictamente posterior a hoy
            try:
                fecha_nueva_dt = datetime.date(anno, mes, dia)
            except ValueError:
                print("[ERROR] Las reservas deben hacerse con al menos un día de anticipación.")
                return
            if fecha_nueva_dt <= hoy:
                print("[ERROR] Las reservas deben hacerse con al menos un día de anticipación.")
                return
            # Construimos YYYY-MM-DD con ceros a la izquierda si es necesario
            fecha_apt = f"{anno}-{mes:02d}-{dia:02d}"

            h_inicio_str = input("Hora de inicio (Ej: 06:00 PM): ")
            h_final_str = input("Hora final (Ej: 07:00 PM): ")

            try:
                hora_inicio_dt = datetime.datetime.strptime(h_inicio_str.strip(), "%I:%M %p")
                hora_final_dt = datetime.datetime.strptime(h_final_str.strip(), "%I:%M %p")
            except ValueError:
                print("\n[ERROR] Formato de hora inválido. Use el formato HH:MM AM/PM (Ej: 06:00 PM).")
                return

            dur_seg = (hora_final_dt - hora_inicio_dt).total_seconds()
            dur = dur_seg / 3600.0
            if dur <= 0:
                print("\n[ERROR] La hora final debe ser mayor a la hora inicial.")
                return

            if not self.establecimiento.lista_canchas:
                print("No hay canchas disponibles.")
                return
            precio_hora = self.establecimiento.lista_canchas[0].precio
            id_cancha_res = self.establecimiento.lista_canchas[0].id_cancha
            id_cliente_res = getattr(cliente_actual, 'id_usuario')
            if id_cliente_res is None:
                print("[ERROR] No se pudo identificar el cliente en sesión.")
                return

            # Extraemos la hora de apertura y cierre del atributo horario de la cancha
            try:
                # El horario tiene formato "08:00 AM - 10:00 PM"
                horario_cancha = self.establecimiento.lista_canchas[0].horario
                partes = horario_cancha.split(" - ")
                if len(partes) == 2:
                    # Intentamos parsear ambas horas como 24h primero, luego AM/PM
                    try:
                        hora_apertura = datetime.datetime.strptime(partes[0].strip(), "%H:%M")
                        hora_cierre = datetime.datetime.strptime(partes[1].strip(), "%H:%M")
                    except ValueError:
                        # Si falla con 24h, intentamos con formato AM/PM
                        hora_apertura = datetime.datetime.strptime(partes[0].strip(), "%I:%M %p")
                        hora_cierre = datetime.datetime.strptime(partes[1].strip(), "%I:%M %p")
                    
                    # Validación: si la hora de inicio solicitada es menor a la apertura
                    if hora_inicio_dt < hora_apertura:
                        print(f"[ERROR] El horario solicitado está fuera de la jornada de atención de la cancha ({horario_cancha}).")
                        return
                    # Validación: si la hora final solicitada es mayor al cierre
                    if hora_final_dt > hora_cierre:
                        print(f"[ERROR] El horario solicitado está fuera de la jornada de atención de la cancha ({horario_cancha}).")
                        return
                else:
                    # Formato inesperado, continuamos sin validación de horario específico
                    print("[Advertencia] No se pudo parsear el horario de la cancha. Continuando sin validación de jornada.")
            except Exception as e:
                print(f"[ERROR] Problema al validar el horario de la cancha: {e}")
                # Continuamos la reserva para no bloquear el sistema ante errores de parseo

            # Validar disponibilidad con la clase Reservas (SELECT en main, lógica en clase)
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT hora_inicio, hora_final FROM reservas WHERE id_cancha = ? AND fecha_apartada = ? AND estado != 'Cancelada'",
                (id_cancha_res, fecha_apt)
            )
            reservas_existentes = cursor.fetchall()
            conn.close()
            conn = None

            # Validación anti-cruce: comparación explícita de solapamiento de horas
            for existente in reservas_existentes:
                try:
                    ex_inicio = datetime.datetime.strptime(str(existente[0]).strip(), "%I:%M %p")
                    ex_final = datetime.datetime.strptime(str(existente[1]).strip(), "%I:%M %p")
                except ValueError:
                    ex_inicio = datetime.datetime.strptime(str(existente[0]).strip(), "%H:%M")
                    ex_final = datetime.datetime.strptime(str(existente[1]).strip(), "%H:%M")
                if hora_inicio_dt < ex_final and hora_final_dt > ex_inicio:
                    print("[ERROR] La cancha ya se encuentra reservada en ese horario para la fecha seleccionada.")
                    return

            reserva_temp = Reservas(fecha_apt, h_inicio_str.strip(), h_final_str.strip(), dur, "Pendiente", 0.0, 0.0)
            if not reserva_temp.validar_disponibilidad(h_inicio_str.strip(), h_final_str.strip(), reservas_existentes):
                print("\n[ERROR] La cancha no está disponible en el horario seleccionado (hay choque con otra reserva).")
                return

            reserva_temp.calcular(precio_hora)
            print(f"\nEl total de la reserva es: ${reserva_temp.total_reserva:,.2f}")
            try:
                abono_ingresado = float(input("Ingrese el valor del abono a pagar ahora: "))
            except ValueError:
                print("\n[ERROR] Valor ingresado inválido. Cancelando pago...")
                return

            print("\n--- SELECCIONE UN MÉTODO DE PAGO ---")
            print("1. Efectivo")
            print("2. Tarjeta")
            print("3. Transferencia")
            try:
                opc_pago = int(input("Ingrese el método de pago (1/2/3): "))
                pago_valido = False
                comprobante_ingresado = "N/A"
                id_metodo_db = opc_pago

                if opc_pago == 1:
                    pago_efectivo = Efectivo(id_metodopago=1, tipo_pago="Efectivo", descripcion="Pago en caja", id_efectivo=1, monto_recibido=abono_ingresado, cambio=0.0, estado="Pendiente")
                    pago_valido = pago_efectivo.validarPago(abono_ingresado)
                    comprobante_ingresado = f"EFECTIVO-{datetime.datetime.now().strftime('%H%M%S')}"
                elif opc_pago == 2:
                    tipo_tarjeta = "Visa"
                    titular = input("Nombre del titular: ")
                    vencimiento = input("Fecha de vencimiento (MM/AA): ")
                    cvv = input("Código de seguridad: ")
                    pago_tarjeta = Tarjeta(id_metodopago=2, tipo_pago="Tarjeta", descripcion="Pago en datáfono", id_tarjeta=1, tipo_tarjeta=tipo_tarjeta, titular=titular, fecha_vencimiento=vencimiento, codigo_seguridad=cvv)
                    pago_valido = pago_tarjeta.validarTarjeta()
                    comprobante_ingresado = f"VOUCHER-{datetime.datetime.now().strftime('%H%M%S')}"
                    print(f"\n¡Pago con tarjeta procesado con éxito!\nHas pagado un abono de ${abono_ingresado:,.2f}.\nEstaremos pendientes cuando desees cancelar el total de la reserva.")
                elif opc_pago == 3:
                    banco = input("\nBanco de origen: ")
                    pago_transferencia = (TransferenciaBuilder()
                                          .set_id_pago(3)
                                          .set_tipo("Transferencia")
                                          .set_monto(abono_ingresado)
                                          .set_fecha(fecha_apt)
                                          .set_banco_origen(banco)
                                          .build())
                    pago_valido = pago_transferencia.validarTransferencia()
                    comprobante_ingresado = f"TRANSF-{datetime.datetime.now().strftime('%H%M%S')}"
                    print(f"\n¡Transferencia validada con éxito!\nHas registrado un abono de ${abono_ingresado:,.2f}.\nEstado: Abono registrado correctamente.")
                else:
                    print("Opción de pago inválida.")
                    return
            except ValueError:
                print("\n[ERROR] Valor ingresado inválido. Cancelando pago...")
                return

            if not pago_valido:
                print("\nEl pago no pudo ser validado. Cancelando el proceso de reserva...")
                return

            reserva_temp.abono = abono_ingresado

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reservas (id_cliente, id_cancha, fecha_apartada, hora_inicio, hora_final, duracion, estado, total_reserva, abono) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (id_cliente_res, id_cancha_res, fecha_apt, h_inicio_str.strip(), h_final_str.strip(), dur, "Pendiente", reserva_temp.total_reserva, abono_ingresado)
            )
            id_reserva_db = cursor.lastrowid
            cursor.execute(
                "INSERT INTO pagos (id_reserva, id_metodo_pago, fecha_pago, valor, comprobante, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (id_reserva_db, id_metodo_db, fecha_apt, abono_ingresado, comprobante_ingresado, "Registrado")
            )
            cursor.execute("UPDATE reservas SET estado = 'Confirmada' WHERE id = ?", (id_reserva_db,))
            conn.commit()

            nuevo_pago = Pago(fecha_pago=fecha_apt, valor=abono_ingresado, comprobante=comprobante_ingresado, estado="Registrado")
            print("Reserva reconfirmada con el pago")
            saldo_pendiente = reserva_temp.calcular_excedente()
            print(f"\nSaldo pendiente de la reserva: ${saldo_pendiente:,.2f}")
            print(f"✓ Reserva creada con éxito para {cliente_actual.nombre}.")
        except ValueError:
            print("\n[ERROR] Se ingresó un valor numérico incorrecto. La reserva no fue creada.")
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
                nuevo_usuario = US.Cliente(nombre, apellido, documento, telefono, correo, password)
                cursor.execute(
                    "INSERT INTO usuarios (nombre, apellido, documento, telefono, correo, password, tipo_usuario, fecha_registro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (nombre, apellido, documento, telefono, correo, password, "cliente", fecha_reg)
                )
                nuevo_usuario.id_usuario = cursor.lastrowid
                cursor.execute("INSERT INTO clientes (id_usuario) VALUES (?)", (nuevo_usuario.id_usuario,))
                conn.commit()
                print("\nCliente creado exitosamente.")
            elif op == 2:
                print("\nBIENVENIDO A LA CREACION DE USUARIO DE EMPLEADOS")
                cargo = input("Ingrese el cargo: ")
                salario = input("Ingrese el salario: ")
                horario_emp = input("Ingrese el horario: ")
                direccion = input("Ingrese la direccion: ")
                nuevo_usuario = US.Empleado(nombre, apellido, documento, telefono, correo, password, cargo, salario, horario_emp, direccion)
                cursor.execute(
                    "INSERT INTO usuarios (nombre, apellido, documento, telefono, correo, password, tipo_usuario, fecha_registro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (nombre, apellido, documento, telefono, correo, password, "empleado", fecha_reg)
                )
                nuevo_usuario.id_usuario = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO empleados (id_usuario, cargo, salario, horario, direccion) VALUES (?, ?, ?, ?, ?)",
                    (nuevo_usuario.id_usuario, cargo, salario, horario_emp, direccion)
                )
                conn.commit()
                print("\nEmpleado creado exitosamente.")
            elif op == 3:
                print("\nBIENVENIDO A LA CREACION DE USUARIO DE ADMINISTRADORES")
                cargo = input("Ingrese el cargo: ")
                salario = input("Ingrese el salario: ")
                direccion = input("Ingrese la direccion: ")
                nuevo_usuario = US.Administrador(nombre, apellido, documento, telefono, correo, password, cargo, salario, direccion)
                cursor.execute(
                    "INSERT INTO usuarios (nombre, apellido, documento, telefono, correo, password, tipo_usuario, fecha_registro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (nombre, apellido, documento, telefono, correo, password, "administrador", fecha_reg)
                )
                nuevo_usuario.id_usuario = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO administradores (id_usuario, cargo, salario, direccion) VALUES (?, ?, ?, ?)",
                    (nuevo_usuario.id_usuario, cargo, salario, direccion)
                )
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
            cursor.execute(
                "SELECT id, nombre, apellido, documento, telefono, correo, password, tipo_usuario FROM usuarios WHERE (correo = ? OR nombre = ?) AND password = ?",
                (user, user, password)
            )
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
            cursor.execute(
                "SELECT r.id, r.fecha_apartada, r.hora_inicio, r.hora_final, r.estado, c.nombre_cancha, r.total_reserva, r.abono FROM reservas r LEFT JOIN canchas c ON c.id = r.id_cancha WHERE r.id_cliente = ?",
                (getattr(cliente, 'id_usuario'),)
            )
            rows = cursor.fetchall()
            if not rows:
                print("No tienes reservas registradas actualmente.")
                return
            for row in rows:
                res_obj = Reservas(row[1], row[2], row[3], 0, row[4], row[6] or 0, row[7] or 0)
                saldo = res_obj.calcular_excedente()
                print(f"ID: {row[0]} | Cancha: {row[5]} | Fecha: {row[1]} | Horario: {row[2]} a {row[3]} | Estado: {row[4]} | Saldo: ${saldo:,.2f}")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
        finally:
            if conn:
                conn.close()

    def editar_mis_reservas(self, cliente):
        print("\n--- EDITAR MIS RESERVAS ---")
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, fecha_apartada, hora_inicio, hora_final, estado, id_cancha FROM reservas WHERE id_cliente = ? AND estado != 'Cancelada'",
                (cliente.id_usuario,)
            )
            rows = cursor.fetchall()
            if not rows:
                print("No tienes reservas activas para editar.")
                return
            for row in rows:
                print(f"ID: {row[0]} | Cancha: {row[5]} | Fecha: {row[1]} | Horario: {row[2]} a {row[3]} | Estado: {row[4]}")
            id_res = int(input("\nIngrese el ID de la reserva a editar: "))
            seleccionada = None
            for row in rows:
                if row[0] == id_res:
                    seleccionada = row
            if seleccionada is None:
                print("[ERROR] La reserva no existe o no pertenece a tu cuenta.")
                return
            dia = int(input("Ingrese el nuevo día de este mes para la reserva: "))
            hoy = datetime.date.today()
            try:
                fecha_nueva_dt = datetime.date(hoy.year, hoy.month, dia)
            except ValueError:
                print("[ERROR] Las modificaciones de reservas deben hacerse con al menos un día de anticipación.")
                return
            if fecha_nueva_dt <= hoy:
                print("[ERROR] Las modificaciones de reservas deben hacerse con al menos un día de anticipación.")
                return
            fecha_nueva = f"{hoy.year}-{hoy.month:02d}-{dia:02d}"
            nueva_inicio = input("Nueva hora de inicio (Ej: 06:00 PM): ")
            nueva_final = input("Nueva hora final (Ej: 07:00 PM): ")
            hi = datetime.datetime.strptime(nueva_inicio.strip(), "%I:%M %p")
            hf = datetime.datetime.strptime(nueva_final.strip(), "%I:%M %p")
            if hi >= hf:
                print("[ERROR] La hora final debe ser mayor a la hora inicial.")
                return
            hora_apertura = datetime.time(8, 0)
            hora_cierre = datetime.time(22, 0)
            if hi.time() < hora_apertura or hf.time() > hora_cierre:
                print("[ERROR] La reserva debe estar dentro del horario de operación del establecimiento (08:00 - 22:00).")
                return
            dur_nueva = (hf - hi).total_seconds() / 3600.0
            cursor.execute("SELECT precio FROM canchas WHERE id = ?", (seleccionada[5],))
            fila = cursor.fetchone()
            precio_hora = fila[0] if fila and fila[0] else 0.0
            total_nuevo = dur_nueva * precio_hora
            cursor.execute(
                "UPDATE reservas SET fecha_apartada = ?, hora_inicio = ?, hora_final = ?, duracion = ?, total_reserva = ? WHERE id = ? AND id_cliente = ?",
                (fecha_nueva, nueva_inicio.strip(), nueva_final.strip(), dur_nueva, total_nuevo, id_res, cliente.id_usuario)
            )
            conn.commit()
            print(f"\n✓ Reserva #{id_res} actualizada con éxito.")
        except ValueError:
            print("\n[ERROR] Se ingresó un valor numérico incorrecto. La reserva no fue actualizada.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def cancelar_mis_reservas(self, cliente):
        print("\n--- CANCELAR RESERVAS ---")
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, fecha_apartada, hora_inicio, hora_final, estado FROM reservas WHERE id_cliente = ? AND estado != 'Cancelada'",
                (cliente.id_usuario,)
            )
            rows = cursor.fetchall()
            if not rows:
                print("No tienes reservas activas para cancelar.")
                return
            for row in rows:
                print(f"ID: {row[0]} | Fecha: {row[1]} | Horario: {row[2]} a {row[3]} | Estado: {row[4]}")
            id_res = int(input("\nIngrese el ID de la reserva a cancelar: "))
            cursor.execute(
                "UPDATE reservas SET estado = 'Cancelada' WHERE id = ? AND id_cliente = ?",
                (id_res, cliente.id_usuario)
            )
            if cursor.rowcount == 0:
                print("[ERROR] La reserva no existe o no pertenece a tu cuenta.")
                return
            conn.commit()
            print(f"\n✓ Reserva #{id_res} cancelada con éxito. Estado: Cancelada.")
        except ValueError:
            print("\n[ERROR] Debes ingresar a número válido.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def pagar_saldo_pendiente(self, cliente):
        print("\n--- PAGAR SALDO PENDIENTE DE RESERVA ---")
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            # PASO A: Filtrar reservas del cliente logueado con saldo pendiente
            cursor.execute(
                "SELECT id, fecha_apartada, total_reserva, abono FROM reservas WHERE id_cliente = ? AND total_reserva > abono AND estado != 'Cancelada'",
                (cliente.id_usuario,)
            )
            rows = cursor.fetchall()
            if not rows:
                print("No tienes saldo pendiente en ninguna reserva. ¡Estás al día!")
                return
            # PASO B: Listar, calcular y seleccionar la reserva a saldar
            print("\nReservas con saldo pendiente:")
            for row in rows:
                saldo_lista = (row[2] or 0.0) - (row[3] or 0.0)
                print(f"ID: {row[0]} | Fecha: {row[1]} | Total: ${row[2]:,.2f} | Abono: ${row[3]:,.2f} | Saldo pendiente: ${saldo_lista:,.2f}")
            id_res = int(input("\nIngrese el ID de la reserva que desea saldar: "))
            seleccionada = None
            for row in rows:
                if row[0] == id_res:
                    seleccionada = row
            if seleccionada is None:
                print("[ERROR] La reserva no existe o no tiene saldo pendiente.")
                return
            saldo = (seleccionada[2] or 0.0) - (seleccionada[3] or 0.0)
            print(f"\nEl saldo pendiente de la reserva #{id_res} es: ${saldo:,.2f}")
            print("\n--- SELECCIONE UN MÉTODO DE PAGO ---")
            print("1. Efectivo")
            print("2. Tarjeta")
            print("3. Transferencia")
            try:
                opc_pago = int(input("Ingrese el método de pago (1/2/3): "))
                pago_valido = False
                comprobante_ingresado = "N/A"
                id_metodo_db = opc_pago
                # PASO C: Procesar pago con la lógica limpia de comprobantes autogenerados
                if opc_pago == 1:
                    monto_recibido = float(input("Ingrese el monto recibido en efectivo: "))
                    if monto_recibido < 0 or monto_recibido < saldo:
                        print("[ERROR] El monto no puede ser negativo o menor al saldo pendiente.")
                        return
                    cambio = monto_recibido - saldo
                    print(f"\nPago en efectivo recibido. Su cambio es: ${cambio:,.2f}")
                    pago_efectivo = Efectivo(id_metodopago=1, tipo_pago="Efectivo", descripcion="Pago en caja", id_efectivo=1, monto_recibido=monto_recibido, cambio=cambio, estado="Pendiente")
                    pago_valido = pago_efectivo.validarPago(saldo)
                    comprobante_ingresado = f"EFECTIVO-{datetime.datetime.now().strftime('%H%M%S')}"
                elif opc_pago == 2:
                    pago_tarjeta = Tarjeta(id_metodopago=2, tipo_pago="Tarjeta", descripcion="Pago en datáfono", id_tarjeta=1, tipo_tarjeta="Visa", titular=cliente.nombre, fecha_vencimiento="", codigo_seguridad="")
                    pago_valido = pago_tarjeta.validarTarjeta()
                    comprobante_ingresado = f"VOUCHER-{datetime.datetime.now().strftime('%H%M%S')}"
                elif opc_pago == 3:
                    pago_transferencia = (TransferenciaBuilder()
                                          .set_id_pago(3)
                                          .set_tipo("Transferencia")
                                          .set_monto(saldo)
                                          .set_fecha(datetime.date.today().isoformat())
                                          .set_banco_origen("Banco registrado")
                                          .set_comprobante(f"TRANSF-{datetime.datetime.now().strftime('%H%M%S')}")
                                          .build())
                    pago_valido = pago_transferencia.validarTransferencia()
                    comprobante_ingresado = f"TRANSF-{datetime.datetime.now().strftime('%H%M%S')}"
                else:
                    print("Opción de pago inválida.")
                    return
            except ValueError:
                print("\n[ERROR] Valor ingresado inválido. Cancelando pago...")
                return
            if not pago_valido:
                print("\nEl pago no pudo ser validado. Cancelando el proceso...")
                return
            # PASO C: INSERT INTO pagos con exactamente 6 columnas y 6 valores
            fecha_pago = datetime.date.today().isoformat()
            cursor.execute(
                "INSERT INTO pagos (id_reserva, id_metodo_pago, fecha_pago, valor, comprobante, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (id_res, id_metodo_db, fecha_pago, saldo, comprobante_ingresado, "Registrado")
            )
            # PASO D: La reserva queda totalmente pagada y confirmada
            cursor.execute(
                "UPDATE reservas SET abono = total_reserva, estado = 'Confirmada' WHERE id = ? AND id_cliente = ?",
                (id_res, cliente.id_usuario)
            )
            conn.commit()
            print(f"\n✓ Saldo pendiente de la reserva #{id_res} pagado con éxito (${saldo:,.2f}).")
            print("Reserva totalmente pagada y confirmada para la cancha.")
        except ValueError:
            print("\n[ERROR] Se ingresó un valor numérico incorrecto. El pago no fue registrado.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def modificar_perfil(self, cliente_actual):
        print(f"\n--- MODIFICAR MI PERFIL: {cliente_actual.nombre} {cliente_actual.apellido} ---")
        print(f"Documento: {cliente_actual.documento}")
        print(f"Teléfono actual: {cliente_actual.telefono}")
        print(f"Correo actual: {cliente_actual.correo}")
        campo = input("\n¿Qué dato desea modificar? (1. Teléfono / 2. Correo / 3. Cancelar): ").strip()
        if campo == "3":
            print("Perfil sin cambios.")
            return
        if campo != "1" and campo != "2":
            print("Opción inválida.")
            return
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            if campo == "1":
                nuevo_telefono = input("Ingrese el nuevo teléfono: ")
                cursor.execute(
                    "UPDATE usuarios SET telefono = ? WHERE id = ?",
                    (nuevo_telefono, cliente_actual.id_usuario)
                )
                conn.commit()
                cliente_actual.telefono = nuevo_telefono
                print("\n✓ Teléfono actualizado con éxito.")
            else:
                nuevo_correo = input("Ingrese el nuevo correo: ")
                cursor.execute(
                    "UPDATE usuarios SET correo = ? WHERE id = ?",
                    (nuevo_correo, cliente_actual.id_usuario)
                )
                conn.commit()
                cliente_actual.correo = nuevo_correo
                print("\n✓ Correo actualizado con éxito.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def mostrar_todas_las_reservas(self):
        print("\n--- TODAS LAS RESERVAS DEL SISTEMA ---")
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT r.id, u.nombre, u.apellido, c.nombre_cancha, r.fecha_apartada, r.hora_inicio, r.hora_final, r.estado, r.total_reserva, r.abono FROM reservas r LEFT JOIN usuarios u ON u.id = r.id_cliente LEFT JOIN canchas c ON c.id = r.id_cancha ORDER BY r.id"
            )
            rows = cursor.fetchall()
            if not rows:
                print("No hay reservas en el sistema.")
                return
            for row in rows:
                res_obj = Reservas(row[4], row[5], row[6], 0, row[7], row[8] or 0, row[9] or 0)
                saldo = res_obj.calcular_excedente()
                print(f"Reserva #{row[0]} | Cliente: {row[1]} {row[2]} | Cancha: {row[3]} | Fecha: {row[4]} {row[5]}-{row[6]} | Estado: {row[7]} | Saldo: ${saldo:,.2f}")
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
            print("\n[Mantenimientos Programados y Activos]")
            cursor.execute("""
                SELECT c.nombre_cancha, m.id_cancha, m.fecha, m.hora_inicio, m.hora_final, m.estado, m.motivo
                FROM mantenimientos m
                JOIN canchas c ON m.id_cancha = c.id
            """)
            mantenimientos_db = cursor.fetchall()
            for reg in mantenimientos_db:
                print(f"    • Lugar/Cancha: {reg[0]} (ID: {reg[1]})")
                print(f"      Día del Mantenimiento: {reg[2]}")
                print(f"      Hora Inicial: {reg[3]}")
                print(f"      Hora Final: {reg[4]}")
                print(f"      Estado y Motivo: {reg[5]} | {reg[6]}")
            # Canchas marcadas 'En Mantenimiento' en BD sin intervención persistida (registros previos)
            cursor.execute("SELECT id, nombre_cancha, estado FROM canchas WHERE estado = 'En Mantenimiento'")
            canchas_en_mt = cursor.fetchall()
            ids_persistidos = {str(reg[1]) for reg in mantenimientos_db}
            for row in canchas_en_mt:
                if str(row[0]) in ids_persistidos:
                    continue
                print(f"    • Lugar/Cancha: {row[1]} (ID: {row[0]})")
                print("      Día del Mantenimiento: Sin registro en la base de datos (intervención previa)")
                print("      Hora Inicial: Sin registro en la base de datos")
                print("      Hora Final: Sin registro en la base de datos")
                print(f"      Estado y Motivo: {row[2]} | Registro previo en la base de datos (sin motivo almacenado)")
            if not mantenimientos_db and not canchas_en_mt:
                print(" - No hay mantenimientos programados ni canchas activas en mantenimiento.")
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
            print("7. Pagar saldo pendiente de reserva")
            print("8. Cerrar sesión")
            try:
                opc = int(input("Ingrese una opción: "))
                if opc == 1:
                    self.ver_canchas()
                elif opc == 2:
                    self.crear_reserva_sistema(cliente_actual)
                elif opc == 3:
                    self.consultar_mis_reservas(cliente_actual)
                elif opc == 4:
                    cliente_actual.editar_reservas(self)
                elif opc == 5:
                    cliente_actual.cancelar_reservas(self)
                elif opc == 6:
                    self.modificar_perfil(cliente_actual)
                elif opc == 7:
                    self.pagar_saldo_pendiente(cliente_actual)
                elif opc == 8:
                    print("Cerrando sesión...");
                    break
                else:
                    print("Opción inválida.")
            except ValueError:
                print("\n[ERROR] Debes ingresar a número válido.")
            except EOFError:
                break

    def registrar_mantenimiento(self):
        print("\n--- REGISTRO DE MANTENIMIENTO DE CANCHA ---")
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            # 1. Consulta y selección de la cancha a intervenir
            cursor.execute("SELECT id, nombre_cancha, estado FROM canchas")
            rows = cursor.fetchall()
            if not rows:
                print("No hay canchas registradas en el sistema.")
                return
            for row in rows:
                print(f"• ID: {row[0]} | Cancha: {row[1]} | Estado: {row[2]}")
            id_cancha = int(input("\nIngrese el ID de la cancha a intervenir: "))
            seleccionada = None
            for row in rows:
                if row[0] == id_cancha:
                    seleccionada = row
            if seleccionada is None:
                print("[ERROR] La cancha no existe.")
                return
            # 2. Reservas activas de esa cancha (para validación anti-cruces)
            cursor.execute(
                "SELECT id, fecha_apartada, hora_inicio, hora_final, estado FROM reservas WHERE id_cancha = ? AND estado != 'Cancelada'",
                (id_cancha,)
            )
            reservas_cancha = cursor.fetchall()
            print(f"\nReservas activas de la cancha '{seleccionada[1]}':")
            if not reservas_cancha:
                print("  (Ninguna reserva activa registrada para esta cancha.)")
            else:
                for r in reservas_cancha:
                    print(f"  • ID: {r[0]} | Fecha: {r[1]} | Horario: {r[2]} a {r[3]} | Estado: {r[4]}")
            # 3. Captura de datos del mantenimiento
            hoy = datetime.datetime.now()
            dia_mt = int(input("Ingrese el número del día para el mantenimiento (ej: 12, 15, 20): "))
            hora_inicio = input("Hora de inicio del mantenimiento (Ej: 06:00 PM): ").strip()
            hora_final = input("Hora final del mantenimiento (Ej: 07:00 PM): ").strip()
            motivo = input("Describa el motivo o descripción del mantenimiento (ej: Reparación de césped): ").strip()
            # 4a. Validación de fecha anticipada: día estrictamente posterior al de hoy
            try:
                fecha_mt = datetime.date(hoy.year, hoy.month, dia_mt)
            except ValueError:
                print("[ERROR] El día debe ser posterior al día de hoy.")
                return
            if dia_mt <= datetime.datetime.now().day:
                print("[ERROR] El día debe ser posterior al día de hoy.")
                return
            fecha = f"{hoy.year}-{hoy.month:02d}-{dia_mt:02d}"
            # 4b. Validación de franja horaria coherente
            try:
                ini_mt = datetime.datetime.strptime(hora_inicio, "%I:%M %p")
                fin_mt = datetime.datetime.strptime(hora_final, "%I:%M %p")
            except ValueError:
                try:
                    ini_mt = datetime.datetime.strptime(hora_inicio, "%H:%M")
                    fin_mt = datetime.datetime.strptime(hora_final, "%H:%M")
                except ValueError:
                    print("[ERROR] Formato de hora inválido. Use HH:MM AM/PM (Ej: 06:00 PM).")
                    return
            if fin_mt <= ini_mt:
                print("[ERROR] La hora final del mantenimiento debe ser mayor a la hora de inicio.")
                return
            # 4c. Vinculación estricta: reservas activas de ESA cancha en ESA fecha
            cursor.execute(
                "SELECT hora_inicio, hora_final FROM reservas WHERE id_cancha = ? AND fecha_apartada = ? AND estado != 'Cancelada'",
                (id_cancha, fecha)
            )
            reservas_fecha = cursor.fetchall()
            for r in reservas_fecha:
                try:
                    r_ini = datetime.datetime.strptime(str(r[0]).strip(), "%I:%M %p")
                    r_fin = datetime.datetime.strptime(str(r[1]).strip(), "%I:%M %p")
                except ValueError:
                    r_ini = datetime.datetime.strptime(str(r[0]).strip(), "%H:%M")
                    r_fin = datetime.datetime.strptime(str(r[1]).strip(), "%H:%M")
                if ini_mt < r_fin and fin_mt > r_ini:
                    print(f"[ERROR] El mantenimiento se cruza con una reserva activa que va de {str(r[0]).strip()} a {str(r[1]).strip()} en la fecha {fecha}. Registro cancelado.")
                    return
            # 5. Instancia del objeto usando el Patrón Builder
            try:
                mantenimiento_nuevo = (
                    MantenimientoBuilder()
                    .set_id_cancha(id_cancha)
                    .set_fecha(fecha)
                    .set_hora_inicio(hora_inicio)
                    .set_hora_final(hora_final)
                    .set_motivo(motivo)
                    .set_estado("Programado")
                    .build()
                )
            except ValueError as be:
                print(f"[ERROR] {be}")
                return
            # 6. Persistencia del objeto Mantenimiento en la tabla mantenimientos
            cursor.execute(
                """
                INSERT INTO mantenimientos (id_cancha, fecha, hora_inicio, hora_final, motivo, estado)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    mantenimiento_nuevo.id_cancha,
                    mantenimiento_nuevo.fecha,
                    mantenimiento_nuevo.hora_inicio,
                    mantenimiento_nuevo.hora_final,
                    mantenimiento_nuevo.motivo,
                    mantenimiento_nuevo.estado,
                )
            )
            cursor.execute(
                "UPDATE canchas SET estado = 'En Mantenimiento' WHERE id = ?",
                (mantenimiento_nuevo.id_cancha,)
            )
            conn.commit()
            # 7. Confirmación extrayendo los datos directamente del objeto
            print(f"\n[ÉXITO] La cancha ID {mantenimiento_nuevo.id_cancha} se ha registrado en mantenimiento correctamente.")
            print(f"Intervención programada: {mantenimiento_nuevo.fecha} de {mantenimiento_nuevo.hora_inicio} a {mantenimiento_nuevo.hora_final}")
            print(f"Motivo registrado: {mantenimiento_nuevo.motivo}")
            print(f"Estado de la intervención: {mantenimiento_nuevo.estado}")
        except ValueError:
            print("\n[ERROR] Debes ingresar a número válido.")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def menu_empleado(self, empleado_actual):
        while True:
            print(f"\n--- MENU EMPLEADO: {empleado_actual.nombre} ---")
            print("1. Registro entrada")
            print("2. Registrar salida")
            print("3. Consultar reservas del sistema")
            print("4. Registrar mantenimiento")
            print("5. Cerrar sesión")
            try:
                opc = int(input("Ingrese una opción: "))
                if opc == 1:
                    empleado_actual.registrar_entrada()
                elif opc == 2:
                    empleado_actual.registrar_salida()
                elif opc == 3:
                    empleado_actual.consultar_reservas(self)
                elif opc == 4:
                    self.registrar_mantenimiento()
                elif opc == 5:
                    print("Cerrando sesión...");
                    break
                else:
                    print("Opción inválida.")
            except ValueError:
                print("\n[ERROR] Debes ingresar a número válido.")
            except EOFError:
                break

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
                if opc == 1:
                    self.crear_usuario()
                elif opc == 4:
                    administrador_actual.gestionar_reportes(self)
                elif opc == 5:
                    administrador_actual.registrar_cancha(self)
                elif opc == 6:
                    self.ver_canchas()
                elif opc == 7:
                    print("Cerrando sesión...");
                    break
                else:
                    print("Opción inválida.")
            except ValueError:
                print("\n[ERROR] Debes ingresar a número válido.")
            except EOFError:
                break

    def menu(self):
        while True:
            print("\n========================================")
            print("   SISTEMA DE ALQUILER DE CANCHAS       ")
            print("========================================")
            print("1. Crear usuario (Registro rápido)")
            print("2. Ingresar al sistema (Login)")
            print("3. Salir del programa")
            try:
                opc = int(input("Ingrese una opción: "))
                if opc == 1:
                    self.crear_usuario()
                elif opc == 2:
                    self.ingresar_usuario()
                elif opc == 3:
                    print("Saliendo del sistema...");
                    break
                else:
                    print("Opción inválida.")
            except ValueError:
                print("\n[ERROR] Debes ingresar a número válido.")
            except EOFError:
                break


if __name__ == "__main__":
    app = Principal()
    app.menu()