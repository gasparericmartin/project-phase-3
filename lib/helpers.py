# lib/helpers.py
from models.__init__ import CONN, CURSOR
from models.Fight import Fight
from models.Fighter import Fighter
from models.Weight_class import Weight_class

def fighters_in_class(weight):
    weight_class = Weight_class.find_by_weight(weight)
    fighters = Fighter.find_by_weight_class(weight_class.id)
    
    [display_fighter_info(fighter) for fighter in fighters]

def display_fighter_info(fighter):
    #Use Weight_class find_by_id to get weight class number
    print(f'Name: {fighter.name}\n' +\
            f'Age: {fighter.age}\n' +\
            f'Weight class: {fighter.weight_class}\n' +\
            f'Wins: {fighter.wins}\n' +\
            f'Losses: {fighter.losses}\n')

def all_fighters():
    pass

def fighter_by_name(name):
    pass

def fighter_opponents(fighter):
    pass

def all_fights():
    pass

def fights_by_date(date):
    pass

def fights_by_fighter(fighter):
    #use fithter name or instance?
    pass




