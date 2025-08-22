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
    


simple_conditioning_events = [
    (10, "Sino", (0,0)), (11, "Comida", (18,18)),
    (40, "Sino", (0,0)), (41, "Comida", (18,18)),
    (70, "Sino", (0,0)), (71, "Comida", (18,18)),
    (100, "Sino", (0,0))
]

# 2. Extinção
extinction_events = [
    (10, "Sino", (0,0)), (11, "Comida", (18,18)),
    (40, "Sino", (0,0)), (41, "Comida", (18,18)),
    (70, "Sino", (0,0)), (71, "Comida", (18,18)),
    (100, "Sino", (0,0)),
    (130, "Sino", (0,0)),
    (160, "Sino", (0,0))
]

# 3. Inibição Latente
latent_inhibition_events = [
    (10, "Sino", (0,0)), (30, "Sino", (0,0)), (50, "Sino", (0,0)),
    (80, "Sino", (0,0)), (81, "Comida", (18,18)),
    (110, "Sino", (0,0)), (111, "Comida", (18,18)),
    (140, "Sino", (0,0)), (141, "Comida", (18,18)),
    (170, "Sino", (0,0))
]

# 4. Bloqueio
blocking_events = [
    (10, "Sino", (0,0)), (11, "Comida", (18,18)),
    (30, "Sino", (0,0)), (31, "Comida", (18,18)),
    (50, "Sino", (0,0)), (51, "Comida", (18,18)),
    (80, "Sino", (0,0)), (81, "Luz", (0,0)), (82, "Comida", (18,18)),
    (110, "Sino", (0,0)), (111, "Luz", (0,0)), (112, "Comida", (18,18)),
    (140, "Sino", (0,0)), (141, "Luz", (0,0)), (142, "Comida", (18,18)),
    (170, "Luz", (0,0))
]

# 5. Condicionamento Secundário
secondary_conditioning_events = [
    (10, "Sino", (0,0)), (11, "Comida", (18,18)),
    (30, "Sino", (0,0)), (31, "Comida", (18,18)),
    (50, "Sino", (0,0)), (51, "Comida", (18,18)),
    (70, "Sino", (0,0)), (71, "Comida", (18,18)),
    (90, "Sino", (0,0)), (91, "Comida", (18,18)),
    (110, "Luz", (0,0)), (111, "Sino", (0,0)), (112, "Comida", (18,18)),
    (130, "Luz", (0,0)), (131, "Sino", (0,0)), (132, "Comida", (18,18)),
    (150, "Luz", (0,0)), (151, "Sino", (0,0)), (152, "Comida", (18,18)),
    (180, "Luz", (0,0))
]
        
