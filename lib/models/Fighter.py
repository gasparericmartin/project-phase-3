from models.__init__ import CURSOR, CONN
from models.Fight import Fight
import re

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
        if re.fullmatch(r'[A-z]+[ -][A-z]*[ -]*[A-z]+', name):
            self._name = name
        else:
            raise TypeError('Name must be a string with 2 or 3 names ' +\
                            'separated by hyphens or spaces.')
    
    @property
    def age(self):
        return self._age 
    
    @age.setter
    def age(self, age):
        if re.fullmatch(r'[0-9]{2}', str(age)):
            self._age = age
        else:
            raise TypeError('Age must be a 2 digit integer.')
    
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
            SET name = ?, age = ?, weight_class = ?, wins = ?, losses = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.age, self.weight_class,
                             self.wins, self.losses, self.id))
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
    def create(cls, name, age, weight_class=None, wins=0, losses=0):
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
        if row:
            return cls.instance_from_db(row)
        else:
            raise Exception('Fighter not found')
    
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
    
    def opponents(self):
        sql = """
            SELECT *
            FROM fights
            WHERE ftr_1 = ? OR ftr_2 = ?
        """
        rows = CURSOR.execute(sql, (self.id, self.id)).fetchall()
        fight_list = [Fight.instance_from_db(row) for row in rows]
        fight_set = {}

        for fight in fight_list:
            if self.id == fight.ftr_1:
                fight_set.add(fight.ftr_2)
            elif self.id == fight.ftr_2:
                fight_set.add(fight.ftr_1)
        
        return fight_set





        
     
    