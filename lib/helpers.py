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
    fighters = Fighter.get_all()
    [display_fighter_info(fighter) for fighter in fighters]

def fighter_by_name(name):
    try:
        fighter = Fighter.find_by_name(name)
        display_fighter_info(fighter)
    except Exception as exc:
        print('There was an error: ', exc)

def fighter_opponents(fighter):
    pass

def display_fight_info(fight):
    fighter_1 = Fighter.find_by_id(fight.ftr_1).name
    fighter_2 = Fighter.find_by_id(fight.ftr_2).name
    winner = Fighter.find_by_id(fight.winner).name if fight.winner else None
    
    if fighter_1 == winner:
        print(f'Date: {fight.date}\n' +\
                f'Fighter 1: {fighter_1} *WINNER* \n' +\
                f'Fighter 2: {fighter_2}\n')
    elif fighter_2 == winner: 
        print(f'Date: {fight.date}\n' +\
            f'Fighter 1: {fighter_1}\n' +\
            f'Fighter 2: {fighter_2} *WINNER*\n')
    else:
        print(f'Date: {fight.date}\n' +\
            f'Fighter 1: {fighter_1}\n' +\
            f'Fighter 2: {fighter_2}\n' +\
            f'Winner: Everybody loses\n')
    
    

def all_fights():
    fights = Fight.get_all()
    [display_fight_info(fight) for fight in fights]

def fights_by_date(date):
    pass

def fights_by_fighter(fighter):
    #use fighter name or instance?
    pass




