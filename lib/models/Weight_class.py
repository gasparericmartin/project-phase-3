class Weight_class:
    
    
    def __init__(self, weight, name, id = None):
        self.weight = weight
        self.name = name
        self.id = id
    
    def __repr__(self):
        print(f'Class weight limit: {self.weight}' + \
              f'Class name: {self.name}' + \
                 f'Class id: {self.id}')
        