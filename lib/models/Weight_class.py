from models.__init__ import CURSOR, CONN

class Weight_class:

    all = {}
    
    def __init__(self, weight, name, id = None):
        self.weight = weight
        self.name = name
        self.id = id
    
    def __repr__(self): 
            print(f'Class weight limit: {self.weight}lbs, ' + \
                f'Class name: {self.name}, ' + \
                    f'Class id: {str(self.id)}')

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
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS weight_classes (
            id INTEGER PRIMARY KEY,
            weight INTEGER,
            name TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS weight_classes
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql = """
            INSERT INTO weight_classes (weight, name)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.weight, self.name))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    
    def update(self):
        sql = """
            UPDATE weight_classes
            SET weight = ?, name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.weight_class, self.name, self.id))
        CONN.commit()
    
    def delete(self):
        sql = """
            DELETE FROM weight_classes 
            WHERE id = ? 
        """
        CURSOR.execute(sql, (self.id))
        CONN.commit()
    
