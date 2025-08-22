from math import sqrt
from random import sample

class Agent:
    def __init__(self,start_position, env):
        self.position = start_position
        self.env = env
        self.target = None
        self.env.grid[start_position[0]][start_position[1]] = "A"  # Marca a posição inicial do agente na grade
        self.action_log = [start_position]
        self.last_known_food_pos = None

        #Parâmetros do modelo
        #Learning rate(Alfa): Indica quão grande será a alteração na força de associação para um determinado aprendizado
        #Esse valor esta associado ao Estimulo Condicionado que induz uma reação do agente ("Notorioedade" do estimulo)
        self.alpha = {
            "Sino": 0.001,
            "Comida": 0.001,
            "Luz": 0.001
        }
        #Reinforcement rate (Beta): Indica a força de associação entre o Estimulo Condicionado e o Estimulo Incondicionado
        self.betha = 1
        #Saliencia de estimulo para penalidade
        self.alfa_prime = 0.15 #Penalidade é bem maior que a recompensa
        self.mu = 0.9 #Inibição latente
        self.reward = 1
        self.prediction_threshold = 0.5 #Threshold para o condicionamento
        self.active_trace_period = 5 #Período de ativação do traço (5s)

        self.w = {
            "Sino" : {
                "Comida": 0.0,
                "Sino": 0.0,
                "Luz": 0.0
            },
            "Comida": {
                "Sino": 0.0,
                "Comida": 0.0,
                "Luz": 0.0
                },
            "Luz": {
                "Sino": 0.0,
                "Comida": 0.0,
                "Luz": 0.0   
            }
          }
        
        #Contem tuplas do tipo (Tipo de traço: String, inicio: Float)
        self.active_traces = []

    def calculate_distance(self, possible_next_position ,target_position):
        return sqrt((possible_next_position[0] - target_position[0]) ** 2 + (possible_next_position[1] - target_position[1]) ** 2)
    
    def set_target(self):
        if self.env.food_pos is not None:
            self.target = self.env.food_pos

    #Function that moves the agent towards the target position
    #The used algorithm is a simple greedy approach (Heuristica Gulosa)
    def move_to_target(self):
        movs = [-1,0,1]

        #Primeiro, verificamos se há alvo, caso não haja, o agente se move aleatoriamente no grid
        if self.target is None:
            #Implement random move
            dx,dy = sample(movs,2)
            self.env.grid[self.position[0]][self.position[1]] = "C"
            self.position = (self.position[0] + dx, self.position[1] + dy)
            self.action_log.append(self.position)
            self.env.grid[self.position[0]][self.position[1]] = "A"
            return

        best_next_position = None
        min_distance = float('inf')

        #Iteramos sobre as posições adjacentes possíveis
        for dx in movs:
            for dy in movs:
                #Calculamos a nova posição do agente
                next_position = (self.position[0] + dx, self.position[1] + dy)
                
                #Verificamos se a nova posição é válida. Caso a posição seja válida, calculamos a distância
                #Euclidiana entre a nova posição e o alvo.
                if self.env.is_valid_position(next_position):
                    distance = self.calculate_distance(next_position, self.env.food_pos)
                    
                    #Se a distância for menor que a distância mínima encontrada até agora, atualizamos a melhor posição
                    if distance < min_distance:
                        min_distance = distance
                        best_next_position = next_position
        
        if best_next_position:
            self.env.grid[self.position[0]][self.position[1]] = "C"
            self.position = best_next_position
            self.action_log.append(self.position)
            self.env.grid[self.position[0]][self.position[1]] = "A"
            
            #Caso a nova posição seja a posição do alimento, precisamos removê-lo do ambiente
            if self.position == self.target():
                self.interact()

            print(f"Agente se moveu para {self.position}")

    #Interage com o alimento, removendo-o do mapa e removendo a percepção da presença de alimento
    def interact(self):
        self.env.food_pos = None
        self.target = None

    def perceive_event(self, event_type, position):

        if self.is_reward_expected(event_type):
            if self.last_known_food_pos:
                self.target = self.last_known_food_pos 
    
    def is_reward_expected(self, stimulus, visited=None):
        """
        Verifica recursivamente se um estímulo leva a uma expectativa de recompensa.
        """
        if visited is None:
            visited = set()

        if stimulus in visited:
            return False # Evita loops

        visited.add(stimulus)

        # Verifica predição direta
        if self.w[stimulus].get("Comida", 0) > self.prediction_threshold:
            return True

        # Verifica predição indireta
        for next_stimulus, weight in self.w[stimulus].items():
            if weight > self.prediction_threshold:
                if self.is_reward_expected(next_stimulus, visited):
                    return True

        return False 

    def learn(self,finished_traces,reward_present):
        for e1,t1 in self.active_traces:
            reward_is_present_or_expected = reward_present or self.is_reward_expected(e1)

            if reward_is_present_or_expected:
                for e2,t2 in self.active_traces:
                    if e1 != e2 and t1 < t2:
                        reward_value = self.reward if e2 == "Comida" else self.w[e2].get("Comida", 0)
                        self.w[e1][e2] += self.alphas[e1] * self.betha * (reward_value - self.w[e1][e2])

        for e1, t1 in finished_traces:
            prediction = self.is_reward_expected(e1)

            if prediction and not reward_present:
                if self.w[e1]["Comida"] > -1: #Valor inibitorio minimo
                    self.w[e1]["Comida"] -= self.alfa_prime 

            if not prediction and not reward_present:
                self.alpha[e1] *= self.mu


    def update_trace(self, current_time):
        traces = [(et, ct) for et, ct in self.active_traces if current_time - ct < self.active_trace_period]
        finishing_traces = list(set(self.active_traces) - set(traces)) 
        self.active_traces = traces
        return finishing_traces
    

