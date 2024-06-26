from models.__init__ import CURSOR, CONN
from models.Fighter import Fighter
import re

class Weight_class:

    all = {}
    
    def __init__(self, weight, name, id = None):
        self.id = id
        self.weight = weight
        self.name = name
        
    
    def __repr__(self): 
        return f'Class weight limit: {str(self.weight)}lbs, ' + \
        f'Class name: {str(self.name)}, ' + \
        f'Class id: {str(self.id)}'

    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, weight):
        if not re.fullmatch(r'[0-9]?[0-9]{2}', str(weight)):
            raise TypeError('Weights must be 2 or 3 digit integers')

        self._weight = weight

    @property
    def name(self):
        return self._name 
    
    @name.setter
    def name(self, name):
        if not re.fullmatch(r'[A-z]*[ ]?[A-z]+weight', name):
            raise TypeError('Weight class name must be a string ending in \'weight\'')
            
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
        CURSOR.execute(sql, (self.weight, self.name, self.id))
        CONN.commit()
    
    def delete(self):
        sql = """
            DELETE FROM weight_classes 
            WHERE id = ? 
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None
    
    @classmethod
    def create(cls, weight, name):
        weight_class = cls(weight, name)
        weight_class.save()
        return weight_class
    
    @classmethod
    def instance_from_db(cls, row):

        weight_class = cls.all.get(row[0])
        if weight_class:
            weight_class.weight = row[1]
            weight_class.name = row[2]
        else:
            weight_class = cls(row[1], row[2])
            weight_class.id = row[0]
            cls.all[weight_class.id] = weight_class
        return weight_class
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM weight_classes
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
        SELECT *
        FROM weight_classes
        WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_weight(cls, weight):
        sql = """
            SELECT * 
            FROM weight_classes
            WHERE weight is ?
        """

        row = CURSOR.execute(sql, (weight,)).fetchone()
        if row:
            return cls.instance_from_db(row)
        else:
            raise Exception('Weight class not found')
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM weight_classes
            WHERE name = ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def all_fighters_in_class(self):
        sql = """
            SELECT *
            FROM fighters
            WHERE weight_class_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Fighter.instance_from_db(row) for row in rows]