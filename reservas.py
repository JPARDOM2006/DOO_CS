import usuarios as US
import mysql.connector as my
con = my.connect(host = "localhost", user = "root", password = ""
, database = "canchas")

#con.is_connect():
 #   print("Exitoso")

class Reservas:
    def __init__(self,fecha_apartada, hora_inicio, hora_final, duracion, estado, total_reserva, abono):
        self.fecha_apartada = fecha_apartada
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.duracion = duracion
        self. estado = estado
        self.total_reserva = total_reserva
        self.abono = abono
        self.lista_clinte = []

        def crear_cliente(self):
            nombre=input(("Ingrese el nombre "))

            nuevo_cliente= US()
            self.lista_cliente.append(nuevo_cliente)
        