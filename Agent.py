from math import sqrt

class Agent:
    def __init__(self,start_position, env):
        self.position = start_position
        self.env = env
        self.target = None
        self.action_log = [start_position]
        self.last_know_food_pos = None

        #Parâmetros do modelo
        #Learning rate(Alfa): Indica quão grande será a alteração na força de associação para um determinado aprendizado
        #Esse valor esta associado ao Estimulo Condicionado que induz uma reação do agente ("Notorioedade" do estimulo)
        self.alpha = 0.001
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
                "Sino": 0.0
            },
            "Comida": {
                "Sino": 0.0,
                "Comida": 0.0
                }
          }
        
        #Contem tuplas do tipo (Tipo de traço: String, inicio: Float)
        self.active_traces = []

    def calculate_distance(self, target_position):
        return sqrt((self.position[0] - target_position[0]) ** 2 + (self.position[1] - target_position[1]) ** 2)
    
    def set_target(self):
        if self.env.food_pos is not None:
            self.target = self.env.food_pos

    #Function that moves the agent towards the target position
    #The used algorithm is a simple greedy approach (Heuristica Gulosa)
    def move_to_target(self):
        
        #Primeiro, verificamos se há alvo ou se o agente já está na posição do alvo.
        #Em ambos os casos, não há movimento a ser feito.
        if self.target is None or self.position == self.target:
            return #Implement random move
        
        best_next_position = None
        min_distance = float('inf')

        #Iteramos sobre as posições adjacentes possíveis
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                #Calculamos a nova posição do agente
                next_position = (self.position[0] + dx, self.position[1] + dy)
                
                #Verificamos se a nova posição é válida. Caso a posição seja válida, calculamos a distância
                #Euclidiana entre a nova posição e o alvo.
                if self.env.is_valid_position(next_position):
                    distance = self.calculate_distance(next_position)
                    
                    #Se a distância for menor que a distância mínima encontrada até agora, atualizamos a melhor posição
                    if distance < min_distance:
                        min_distance = distance
                        best_next_position = next_position

        if best_next_position:
            self.position = best_next_position
            self.action_log.append(self.position)
            print(f"Agente se moveu para {self.position}")

    def perceive_event(self, event_type, position):

        associative_strength = self.w[event_type].get("Comida", 0.0) 
        if associative_strength > self.prediction_threshold:
            if self.last_known_food_pos:
                self.target = self.last_known_food_pos 
        

    def learn(self,finished_traces,reward_present):
        for e1,t1 in self.active_traces:
            for e2,t2 in self.active_traces:
                if e1 != e2 and self.env.food_pos is not None:

                    if t1 < t2:
                        self.w[e1][e2] += self.alpha * self.betha * (self.reward - self.w[e1][e2])

        for e1, t1 in finished_traces:
            prediction = self.w[e1].get("Comida", 0) > self.prediction_threshold

            if prediction and not reward_present:
                self.w[e1]["Comida"] -= self.alfa_prime 

            if not prediction and not reward_present:
                self.alpha *= self.mu


    def update_trace(self, current_time):
        traces = [(et, ct) for et, ct in self.active_traces if current_time - ct < self.active_trace_period]
        finishing_traces = list(set(self.active_traces) - set(traces)) 
        self.active_traces = traces
        return finishing_traces