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
        self.lista_clinte = []
        self.lista_cancha = []



class principal:

    def __init__(self):
        self.lista_canchas=[]
        self.lista_clientes=[]
        self.lista_reservas=[]


    def menu(self):

        while True:
            print("1. para crear cliente")
            opc= input("ingrese una opción")

            if opc=="1":
                nombre= input("ingrese el nombre")
                apellido= input("ingrese el apellido")
                documento= input("ingrese el documento")
                telefono= input("ingrese el telefono")
                correo= input("ingrese el correo")
                fecha_registro= input("ingrese el fecha_registro")
                user= input("ingrese el user")
                password= input("ingrese el password")


                nuevo_cliente= US.Usuarios(nombre,apellido,documento,telefono,correo,fecha_registro,user,password)
                self.lista_clientes.append(nuevo_cliente)

            elif opc=="2":
                for i in self.lista_clientes:
                    print(i.nombre)

if __name__ =="__main__":
    a=principal()
    a.menu()