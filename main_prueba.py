from cancha import Cancha
from establecimiento import Establecimiento
from horario import Horario
from reservas import Reservas
from tarifa import Tarifa
import usuarios as US


class SistemaAlquilerPrincipal:

  def __init__(self):
    self.establecimiento = Establecimiento(
        id_establecimiento=1,
        nombre_establecimiento="Complejo Deportivo El Golazo",
        ubicación="Av. Principal Calle 100",
    )
    self.lista_clientes = []
    self.lista_reservas = []

  def menu(self):
    while True:
      print("\n========================================")
      print("   SISTEMA DE ALQUILER DE CANCHAS       ")
      print("========================================")
      print("1. Registrar nuevo cliente")
      print("2. Ver lista de clientes")
      print("3. Registrar cancha y tarifa de prueba")
      print("4. Ver canchas del establecimiento")
      print("5. Crear una reserva")
      print("6. Salir")

      opc = input("\nIngrese una opción: ")

      if opc == "1":
        print("\n--- Registro de Cliente ---")
        id_usuario = len(self.lista_clientes) + 1
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        documento = input("Documento: ")
        telefono = input("Teléfono: ")
        correo = input("Correo: ")
        fecha_registro = input("Fecha de registro (YYYY-MM-DD): ")
        user = input("Usuario: ")
        password = input("Contraseña: ")

        nuevo_cliente = US.Usuarios(id_usuario, nombre, apellido, documento, telefono, correo, fecha_registro, user, password )
        self.lista_clientes.append(nuevo_cliente)
        print("✓ Cliente registrado con éxito.")

      elif opc == "2":
        print("\n--- Lista de Clientes Registrados ---")
        if not self.lista_clientes:
          print("No hay clientes registrados.")
        for c in self.lista_clientes:
          print(
              f"ID: {c.id_usuario} | Nombre: {c.nombre} {c.apellido} | Doc:"
              f" {c.documento}"
          )

      elif opc == "3":
        print("\n--- Configurando Cancha y Tarifa de Prueba ---")
       
        tarifa_base = Tarifa(
            id_tarifa=1,
            valor_hora=50000,
            dias_semana="Fines de semana",
            valor_dia=10000,
            valor_ubicacion=5000,
            valor_tipo_jornada=15000,
        )

      
        cancha_nueva = Cancha(
            id_cancha=101,
            nombre_cancha="Cancha Sintética 1",
            precio=tarifa_base.calcular_tarifa(),
            horario="08:00 - 22:00",
            tipo_cancha="Fútbol 5",
        )

        self.establecimiento.agregar_cancha(cancha_nueva)
        print("✓ Cancha y tarifa añadidas correctamente al establecimiento.")

      elif opc == "4":
        print(f"\n--- Establecimiento: {self.establecimiento.nombre_establecimiento} ---")
        print(f"Ubicación: {self.establecimiento.ubicación}")
        if not self.establecimiento.lista_canchas:
          print("No hay canchas registradas todavía (Prueba la opción 3).")
        for can in self.establecimiento.lista_canchas:
          print(
              f"• Cancha: {can.nombre_cancha} | Tipo: {can.tipo_cancha} |"
              f" Precio Base: ${can.precio:,.2f}"
          )

      elif opc == "5":
        print("\n--- Creando Nueva Reserva ---")
        if not self.establecimiento.lista_canchas:
          print(
              "¡Error! Primero debes registrar al menos una cancha (Opción 3)."
          )
          continue

        id_res = len(self.lista_reservas) + 1
        fecha_apt = input("Fecha apartada (YYYY-MM-DD): ")
        h_inicio = input("Hora de inicio (Ej: 18:00): ")
        h_final = input("Hora final (Ej: 19:00): ")
        dur = float(input("Duración en horas (Ej: 1.0): "))

        precio_hora = self.establecimiento.lista_canchas[0].precio

        nueva_reserva = Reservas(
            id_reserva=id_resRes := id_res,
            fecha_apartada=fecha_apt,
            hora_inicio=h_inicio,
            hora_final=h_final,
            duracion=dur,
            estado="Pendiente",
            total_reserva=0.0,
            abono=0.0,
        )

     
        nueva_reserva.calcular(precio_hora)
        
       
        abono_ingresado = float(input("Ingrese el valor del abono pagado: "))
        nueva_reserva.abono = abono_ingresado
        nueva_reserva.reserva_confirmada()

        self.lista_reservas.append(nueva_reserva)
        print("✓ Reserva procesada en el sistema.")

      elif opc == "6":
        print("¡Gracias por usar el sistema! Saliendo...")
        break
      else:
        print("Opción inválida, intenta de nuevo.")


if __name__ == "__main__":
  app = SistemaAlquilerPrincipal()
  app.menu()