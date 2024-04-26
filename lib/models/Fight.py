from models.__init__ import CURSOR, CONN

class Fight:

    all = {}

    def __init__(
            self, 
            date, 
            ftr_1 = None, 
            ftr_2 = None, 
            winner = None, 
            id = None):
        self.date = date
        self.ftr_1 = ftr_1
        self.ftr_2 = ftr_2
        self.winner = winner
        self.id = id
    
    def __repr__(self):
        print(
            f'Fight date: {self.date}, ' + \
            f'Fighter 1: {self.ftr_1}, ' + \
            f'Fighter 2: {self.ftr_2}, ' + \
            f'Winner: {self.winner}, ' + \
            f'id: {self.id}'
        )
    
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, date):
        self._date = date