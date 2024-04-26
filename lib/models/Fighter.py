class Fighter:
    

    def __init__(
            self, 
            name, 
            age, 
            weight_class = None, 
            wins = 0, 
            losses = 0):
        self.name = name
        self.age = age
        self.weight_class = weight_class
        self.wins = wins
        self.losses = losses
    
    def __repr__(self):
        print(
              f'Fighter name: {self.name}' + \
              f'Age: {self.age}' + \
              f'Weight class: {self.weight_class}' + \
              f'Wins: {self.wins}' + \
              f'Losses: {self.losses}'
              )
        