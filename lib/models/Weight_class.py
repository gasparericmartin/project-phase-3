from models.__init__ import CURSOR, CONN

class Weight_class:

    all = {}
    
    def __init__(self, weight, name, id = None):
        self.weight = weight
        self.name = name
        self.id = id
    
    def __repr__(self):
        print(f'Class weight limit: {self.weight}lbs' + \
              f'Class name: {self.name}' + \
                 f'Class id: {self.id}')

    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, weight):
        self._weight = weight
    
    @property
    def name(self):
        return self._name 
    
    @name.setter
    def name(self, name):
        self._name = name