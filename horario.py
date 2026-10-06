class Horario:
    def __init__(self, id_horario, hora_inicio, hora_fin):
        
        self.id_horario = id_horario
        self.hora_inicio = hora_inicio  
        self.hora_fin = hora_fin        
        self.es_bloqueado = False

    