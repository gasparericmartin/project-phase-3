class Fighter:

    all = {}

    def __init__(
            self, 
            name, 
            age, 
            weight_class = None, 
            wins = 0, 
            losses = 0,
            id = None):
        self.name = name
        self.age = age
        self.weight_class = weight_class
        self.wins = wins
        self.losses = losses
        self.id = id
    
    def __repr__(self):
        print(
              f'Fighter name: {self.name}' + \
              f'Age: {self.age}' + \
              f'Weight class: {self.weight_class}' + \
              f'Wins: {self.wins}' + \
              f'Losses: {self.losses}' + \
              f'id: {self.id}'
              )
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def age(self):
        return self._age 
    
    @age.setter
    def age(self, age):
        self._age = age
    
    @property
    def weight_class(self):
        return self._weight_class
    
    @weight_class.setter
    def weight_class(self, weight_class):
        self._weight_class = weight_class
    