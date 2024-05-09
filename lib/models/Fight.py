from models.__init__ import CURSOR, CONN
import re
import datetime

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
        return f'Fight date: {self.date}, ' + \
            f'Fighter 1: {self.ftr_1}, ' + \
            f'Fighter 2: {self.ftr_2}, ' + \
            f'Winner: {self.winner}, ' + \
            f'id: {self.id}'
        
    
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, date):
        month = date[0:2]
        day = date[3:5]
        year = date[6:]

        current_day = datetime.datetime.now()
       
        if not re.fullmatch(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', date):
            raise TypeError('Date must be formatted like 01/01/2001.')
        elif int(year) not in range(1993, datetime.datetime.now().year + 1):
            raise Exception('Only past fights between 1993 and the present may be logged.')
        elif int(year) == current_day.year:
            if int(month) > current_day.month:
                raise Exception('No future dates allowed.')
            elif int(month) == current_day.month and int(day) > current_day.day:
                raise Exception('No future dates allowed')

        self._date = date
        
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS fights(
            id INTEGER PRIMARY KEY,
            date TEXT,
            ftr_1 INTEGER,
            ftr_2 INTEGER,
            winner INTEGER,
            FOREIGN KEY (ftr_1) REFERENCES fighters(id),
            FOREIGN KEY (ftr_2) REFERENCES fighters(id),
            FOREIGN KEY (winner) REFERENCES fighters(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS fights
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql = """
            INSERT INTO fights (date, ftr_1, ftr_2, winner)
            VALUES (?,?,?,?)
        """
        CURSOR.execute(sql,(self.date, self.ftr_1, self.ftr_2, self.winner))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    
    def update(self):
        sql = """
            UPDATE fights
            SET date = ?, ftr_1 = ?, ftr_2 = ?, winner = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.date, self.ftr_1, self.ftr_2, self.winner, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM fights
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None
    
    @classmethod
    def create(cls, date, ftr_1=None, ftr_2=None, winner=None):
        fight = cls(date, ftr_1, ftr_2, winner)
        fight.save()
        return fight
    
    @classmethod
    def instance_from_db(cls, row):
        fight = cls.all.get(row[0])
        if fight:
            fight.date = row[1]
            fight.ftr_1 = row[2]
            fight.ftr_2 = row[3]
            fight.winner = row[4]
        else:
            fighter = cls(row[1], row[2], row[3], row[4])
            fighter.id = row[0]
            cls.all[fighter.id] = fighter
        
        return fight
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM fights
        """

        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM fights
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_date(cls, date):
        sql = """
            SELECT *
            FROM fights
            WHERE date = ?
        """
        rows = CURSOR.execute(sql, (date,)).fetchall()
        return [cls.instance_from_db(row) for row in rows if rows]
    
    

