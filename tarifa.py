class Tarifa:
    def __init__(self, id_tarifa, descripcion, precio_por_hora, es_horario_pico=False):
        
        self.id_tarifa = id_tarifa
        self.descripcion = descripcion        
        self.precio_por_hora = precio_por_hora  
        self.es_horario_pico = es_horario_pico 