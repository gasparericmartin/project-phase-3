# lib/helpers.py
from models.__init__ import CONN, CURSOR
from models.Fight import Fight
from models.Fighter import Fighter
from models.Weight_class import Weight_class
import re

def exit_program():
    print('Exiting program')
    exit()

def weight_class_names():
    classes = Weight_class.get_all()
    return [weight_class.name for weight_class in classes]

def weight_class_weights():
    classes = Weight_class.get_all()
    return [weight_class.weight for weight_class in classes]

def display_class_info(weight_class):
    print(f'Weight: {weight_class.weight}lbs\n' +\
          f'Class Name: {weight_class.name}\n')

def display_all_weight_classes():
    weight_classes = Weight_class.get_all()

    [display_class_info(weight_class) for weight_class in weight_classes]

def weight_class_by_weight(weight):
    if re.match(r'[0-9]{3}', str(weight)):
        if weight_class := Weight_class.find_by_weight(weight):
            display_class_info(weight_class)
        else:
            print('Weight class not found')
    else:
        raise TypeError('Input must be 3 consecutive numbers')

def fighters_in_class(weight):
    weight_class = Weight_class.find_by_weight(weight)
    fighters = Fighter.find_by_weight_class(weight_class.id)
    
    [display_fighter_info(fighter) for fighter in fighters]

def display_fighter_info(fighter):
    if fighter_weight := Weight_class.find_by_id(fighter.weight_class):
        print(f'Name: {fighter.name}\n' +\
                f'Age: {fighter.age}\n' +\
                f'Weight class: {fighter_weight.weight}\n' +\
                f'Wins: {fighter.wins}\n' +\
                f'Losses: {fighter.losses}\n')
    else:
        print(f'Name: {fighter.name}\n' +\
                f'Age: {fighter.age}\n' +\
                f'Weight class: None\n' +\
                f'Wins: {fighter.wins}\n' +\
                f'Losses: {fighter.losses}\n')

def all_fighters():
    fighters = Fighter.get_all()
    [display_fighter_info(fighter) for fighter in fighters]

def fighter_by_name(name):
    if fighter := Fighter.find_by_name(name):
        try:
            display_fighter_info(fighter)
        except Exception as exc:
            print('There was an error: ', exc)
    else:
        print('Fighter not found')

def fighter_names():
    fighters = Fighter.get_all()
    return [fighter.name for fighter in fighters]

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
    #Very strange behavior, first call to Fight.get_all() returning none
    #Will not function without first call
    Fight.get_all()
    [display_fight_info(fight) for fight in Fight.get_all()]

def fights_by_date(date, display=True):
    pattern = re.compile('[0-9]{2}\/[0-9]{2}\/[0-9]{4}')
    if not date:
        date = str(input('Enter date in 01/01/2001 format: '))
    
    while not pattern.match(date):
        print('Invalid input')
        date = str(input('Enter date in 01/01/2001 format: '))
    
    if fights := Fight.find_by_date(date):
        if display:
            [display_fight_info(fight) for fight in fights]
        else:
            return fights
    else:
         print('No fights from that date found')
    
def fights_by_fighter(fighter):
    fights = fighter.all_fights()
    [display_fight_info(fight) for fight in fights]

def all_fight_info():
    Fight.get_all()
    return_list = []
    
    for fight in Fight.get_all():
        ftr1 = Fighter.find_by_id(fight.ftr_1).name
        ftr2 = Fighter.find_by_id(fight.ftr_2).name
        wnr = Fighter.find_by_id(fight.winner).name
        
        return_list.append('Date: ' + fight.date +\
                            ' | Fighter 1: ' + ftr1 +\
                            ' | Fighter 2: ' + ftr2)
    
    return return_list

def create_weight_class():
    weight_ = input('Input weight (number only): ')
    name_ = input('Input class name: ')

    try:
        Weight_class.create(weight_, name_)
        print('New weight class created')
    except Exception as exc:
        print('Error creating weight class: ', exc)

def update_weight_class(class_name):
    if w_class := Weight_class.find_by_name(class_name):
        print('Current weight class info : ')
        display_class_info(w_class)
        try: 
            w_class.weight = input('Input new weight (number only): ')
            w_class.name = input('Input new name: ')
            w_class.update()
            print('Weight class successfully updated')
        except Exception as exc:
            print('Error updating class: ', exc)
    else:
        print('Weight class not found')

def delete_weight_class(class_name):
    if w_class := Weight_class.find_by_name(class_name):
        try:
            w_class.delete()
            print('Weight class deleted')
        except Exception as exc:
            print('Error deleting weight class', exc)
    else:
        print('Weight class not found')

def create_fighter(weight_):
    try:
        name_ = input('Input name: ')
        age_ = input('Input age: ')
        wins_ = input('Input wins: ')
        losses_ = input('Input losses: ')
        
        Fighter.create(name_, age_, weight_, wins_, losses_)
        print('New fighter created')
    except Exception as exc:
        print('Error creating fighter', exc)

def update_fighter(fighter):
    try:
        fighter.name = input('Input new name: ')
        fighter.weight = Weight_class.find_by_weight(input('Input new weight (number only): ')).id
        fighter.age = input('Input new age: ')
        fighter.wins = input('Input new wins: ')
        fighter.losses = input('Input new losses: ')
        
        fighter.update()
        print('Fighter successfully updated')
    except Exception as exc:
        print('Error updating fighter: ', exc)

def delete_fighter(fighter):
    try:
        fighter.delete()
        print('Fighter deleted')
    except Exception as exc:
        print('Error deleting fighter: ', exc)

def create_fight(date_, f1, f2, wnr):
    try:
        ftr_1_ = Fighter.find_by_name(f1)
        ftr_2_ = Fighter.find_by_name(f2)
        winner_ = Fighter.find_by_name(wnr)

        Fight.find_by_date(date_)
        same_date_fights = Fight.find_by_date(date_)

        for fight in same_date_fights:
            ftr_list = [ftr_1_.id, ftr_2_.id]
            if fight.ftr_1 in ftr_list or fight.ftr_2 in ftr_list:
                raise Exception('Fighters cannot fight twice in a day.')

        if ftr_1_.weight_class != ftr_2_.weight_class:
            raise Exception('Fighters must be in the same weight class.')
        elif ftr_1_ == ftr_2_:
            raise Exception('Fighters Must be unique')
        elif winner_ not in [ftr_1_, ftr_2_]:
            raise Exception('Winner must be one of the participants.')
        
        Fight.create(date_, ftr_1_.id, ftr_2_.id, winner_.id)
        print('Fight created')
    except Exception as exc:
        print('Error creating fight:', exc)

def update_fight(fight, f1_, f2_, wnr_, date_):
    try:
        ftr_1_ = Fighter.find_by_name(f1_)
        ftr_2_ = Fighter.find_by_name(f2_)
        winner_ = Fighter.find_by_name(wnr_)

        Fight.find_by_date(date_)
        same_date_fights = Fight.find_by_date(date_)

        for fight in same_date_fights:
            ftr_list = [ftr_1_.id, ftr_2_.id]
            if fight.ftr_1 in ftr_list or fight.ftr_2 in ftr_list:
                raise Exception('Fighters cannot fight twice in a day.')

        if ftr_1_.weight_class != ftr_2_.weight_class:
            raise Exception('Fighters must be in the same weight class.')
        elif ftr_1_ == ftr_2_:
            raise Exception('Fighters Must be unique')
        elif winner_ not in [ftr_1_, ftr_2_]:
            raise Exception('Winner must be one of the participants.')
        
        fight.date = date_
        fight.ftr_1 = ftr_1_.id
        fight.ftr_2 = ftr_2_.id
        fight.winner = winner_.id
        fight.update()
        print('Fight updated')
    except Exception as exc:
        print('Error updating fight:', exc)

def delete_fight(fight):
    try:
        fight.delete()
        print('Fight deleted')
    except Exception as exc:
        print('Error deleting fight: ', exc)











