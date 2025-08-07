import time
from Environment import Environment
from Agent import Agent
from EventController import EventController

#Eventos de Condicionamento Simples (Figura 4, primeira linha, do artigo)
events = [
    (10, "Sino", (0,0)),
    (11, "Comida", (18,18)),
    (40, "Sino", (0,0)),
    (41, "Comida", (18,18)),
    (70, "Sino", (0,0)),
    (71, "Comida", (18,18)),
    (100, "Sino", (18,18))
]
current_time = 0
duration = 120 #Duração total da simulação

#Instancia os elementos da simulação
env = Environment()
agente = Agent((5,5), env)
controller = EventController(events)

#Loop principal da simulação
print("Iniciando simulação...")
while current_time < duration:

    print(f"----Tempo: {current_time:.1f}s ----")
    event = controller.verifica_eventos(current_time)

    if event:
        event_type, pos = event
        print(f"NOVO EVENTO: {event_type} na posicao {pos}")

        #Se um evento ocorreu, ele deve ser "percebido" pelo agente.
        agente.active_traces.append((event_type, current_time))
        agente.perceive_event(event_type, pos)

        if event_type == "Sino":
            agente.perceive_event(event_type, pos)
        elif event_type == "Comida":
            env.place_food(pos)
            agente.last_known_food_pos = pos
            agente.set_target()
    
    reward_present = env.food_pos is not None 
    finished_traces = agente.update_trace(current_time)
    agente.learn(finished_traces, reward_present)
    agente.move_to_target()

    #O passo finaliza com o avanço do tempo da simulação
    time.sleep(0.1)
    current_time += 0.3

print(f"\n--- FIM DA SIMULAÇÃO (t={current_time:.1f}s) ---")
final_weight = agente.w['Sino'].get('Comida', 0)
print(f"Força final da associação 'Sino' -> 'Comida': {final_weight:.4f}")