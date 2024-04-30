from models.__init__ import CURSOR, CONN
from models.Fight import Fight

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
        self.id = id
        self.name = name
        self.age = age
        self.weight_class = weight_class
        self.wins = wins
        self.losses = losses
        
    
    def __repr__(self):
        return f'Fighter name: {self.name}, ' + \
               f'Age: {self.age}, ' + \
               f'Weight class: {self.weight_class}, ' + \
               f'Wins: {self.wins}, ' + \
               f'Losses: {self.losses}, ' + \
               f'id: {self.id}'
              
    
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
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS fighters (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            weight_class INTEGER,
            wins INTEGER,
            losses INTEGER,
            FOREIGN KEY (weight_class) REFERENCES weight_classes(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS fighters
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql = """
            INSERT INTO fighters (name, age, weight_class, wins, losses)
            VALUES (?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.age, self.weight_class, self.wins, self.losses))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    
    def update(self):
        sql = """
            UPDATE fighters
            SET name = ?, age = ?, wins = ?, losses = ?, weight_class = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.age, self.wins,
                            self.losses, self.weight_class))
        CONN.commit()
    
    def delete(self):
        sql = """
            DELETE FROM fighters
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def create(cls, name, age, weight_class, wins, losses):
        fighter = cls(name, age, weight_class, wins, losses)
        fighter.save()
        return fighter

    @classmethod
    def instance_from_db(cls, row):
        fighter = cls.all.get(row[0])
        if fighter:
            fighter.name = row[1]
            fighter.age = row[2]
            fighter.weight_class = row[3]
            fighter.wins = row[4]
            fighter.losses = row[5]

        else:
            fighter = cls(row[1], row[2], row[3], row[4], row[5])
            fighter.id = row[0]
            cls.all[fighter.id] = fighter
        return fighter
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM fighters
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM fighters
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM fighters
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_weight_class(cls, weight_class_id):
        sql = """
            SELECT *
            FROM fighters
            WHERE weight_class = ?
        """
        rows = CURSOR.execute(sql, (weight_class_id,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    def all_fights(self):
        sql = """
            SELECT *
            FROM fights
            WHERE ftr_1 = ? OR ftr_2 = ?
        """

        rows = CURSOR.execute(sql, (self.id, self.id)).fetchall()
        return [Fight.instance_from_db(row) for row in rows]
    
    def all_wins(self):
        sql = """
            SELECT *
            FROM fights
            WHERE winner = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Fight.instance_from_db(row) for row in rows]



        
     
    