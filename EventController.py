#Essa classe tem a função de gerenciar os eventos que acontecem ao longo do tempo durante a execução do programa
#O valor "eventos" que são pré definidos e devem ser passados ao construtor
#Cenário são tuplas do tipo (tempo, evento, position)

class EventController:
    def __init__(self,events):
        self.events = sorted(events, key= lambda x: x[0])
        self.event_index = 0 #Armazena o indice do próximo evento a ser realizado

    #Verifica se, para um dado current_time, um evento deve acontecer (ou já deveria ter acontecido)
    #Se sim, retoran o evento
    def verifica_eventos(self, current_time):
        if self.event_index >= len(self.events):
            return None
        
        time, event, pos = self.events[self.event_index]
        if current_time >= time:
            self.event_index += 1
            return (event, pos)
        
        return None
        
