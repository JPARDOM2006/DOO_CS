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

    def calcular(self, tarifa_hora):
        self.total_reserva = self.duracion * tarifa_hora
        print(f"Total de la reserva: {self.total_reserva}")     

    def fecha(self):
        print(f"Fecha apartada: {self.fecha_apartada}")

    def horario(self):
        print(f"Horario: {self.hora_inicio} - {self.hora_final}")

    def consultar_estado(self):
        print(f"Estado de la reserva: {self.estado}")

    def reserva_confirmada(self):
        if self.abono >= self.total_reserva * 0.5:
            self.estado = "Confirmada"
            print("Reserva confirmada")
        else:
            print("La reserva no se puede confirmar, falta el abono")

    def calcular_abono(self, porcentaje=0.5):
        self.abono = self.total_reserva * porcentaje
        print(f"Abono requerido: {self.abono}")  



        def crear_cliente(self):
            nombre=input(("Ingrese el nombre "))

            nuevo_cliente= US()
            self.lista_cliente.append(nuevo_cliente)

       