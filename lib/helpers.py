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
    list = [weight_class.name for weight_class in classes]

    return list if len(list) > 0 else None


def weight_class_weights():
    classes = Weight_class.get_all()
    list = [weight_class.weight for weight_class in classes]

    return list if len(list) > 0 else None

def display_class_info(weight_class):
    print(f'Weight: {weight_class.weight}lbs\n' +\
          f'Class Name: {weight_class.name}\n')

def display_all_weight_classes():
    weight_classes = Weight_class.get_all()
    if len(weight_classes) > 0:
        [display_class_info(weight_class) for weight_class in weight_classes]
    else:
        print('No weight classes to display')

def weight_class_by_weight(weight):
    try:
        if re.match(r'[0-9]{3}', str(weight)):
            if weight_class := Weight_class.find_by_weight(weight):
                display_class_info(weight_class)
            else:
                print('Weight class not found')
        else:
            raise TypeError('Input must be 3 consecutive numbers')
    except Exception as exc:
        print('There was an error:', exc)

def fighters_in_class(weight):
    weight_class = Weight_class.find_by_weight(weight)
    fighters = weight_class.all_fighters_in_class()
    
    [display_fighter_info(fighter) for fighter in fighters]

def display_fighter_info(fighter):
    if fighter_weight := Weight_class.find_by_id(fighter.weight_class_id):
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
    if len(fighters) > 0:
        [display_fighter_info(fighter) for fighter in fighters]
    else:
        print('No fighters to display')

def fighter_by_name(name):
    try:
        fighter = Fighter.find_by_name(name)
        display_fighter_info(fighter)
    except Exception as exc:
        print('There was an error:', exc)

def fighter_names():
    fighters = Fighter.get_all()
    list = [fighter.name for fighter in fighters]

    return list if len(list) > 0 else None

def fighter_opponents(ftr_name):
    fighter = Fighter.find_by_name(ftr_name)
    opponents = fighter.opponents()
    [print(opponent) for opponent in opponents]

def fighter_fights(ftr_name):
    fighter = Fighter.find_by_name(ftr_name)
    fights = fighter.all_fights()

    [display_fight_info(fight) for fight in fights]

def display_fight_info(fight):
    if fighter_1 := Fighter.find_by_id(fight.ftr_1_id):
        fighter_1_name = fighter_1.name
    else:
        fighter_1_name = 'Fighter deleted'
    
    if fighter_2 := Fighter.find_by_id(fight.ftr_2_id):
        fighter_2_name = fighter_2.name
    else:
        fighter_2_name = 'Fighter deleted'

    if winner := Fighter.find_by_id(fight.winner_id):
        pass

    
    if fighter_1 == winner:
        print(f'Date: {fight.date}\n' +\
                f'Fighter 1: {fighter_1_name} *WINNER* \n' +\
                f'Fighter 2: {fighter_2_name}\n')
    elif fighter_2 == winner: 
        print(f'Date: {fight.date}\n' +\
            f'Fighter 1: {fighter_1_name}\n' +\
            f'Fighter 2: {fighter_2_name} *WINNER*\n')
    
def all_fights():
    [display_fight_info(fight) for fight in Fight.get_all()]

def fights_by_date(date=None, display=True):
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
    return_list = []
    
    for fight in Fight.get_all():
        ftr1 = Fighter.find_by_id(fight.ftr_1_id).name
        ftr2 = Fighter.find_by_id(fight.ftr_2_id).name
        wnr = Fighter.find_by_id(fight.winner_id).name
        
        return_list.append('Date: ' + fight.date +\
                            ' | Fighter 1: ' + ftr1 +\
                            ' | Fighter 2: ' + ftr2)
    
    return return_list

def create_weight_class():
    weight_ = input('Input weight (number only): ')
    name_ = input('Input class name: ')
    weights_list = weight_class_weights() if weight_class_weights() else []
    class_names_list = weight_class_names() if weight_class_names() else []

    try:
        if int(weight_) in weights_list:
            raise Exception('Weight already exists')
        if name_ in class_names_list:
            raise Exception('Name already exists')
        
        Weight_class.create(weight_, name_)
        print('New weight class created')
    except Exception as exc:
        print('Error creating weight class: ', exc)

def update_weight_class(class_name):
    if w_class := Weight_class.find_by_name(class_name):
        print('Current weight class info : ')
        display_class_info(w_class)

        weight_ = input('Input new weight (number only): ')
        name_ = input('Input new name: ')
        
        try: 
            if int(weight_) in weight_class_weights():
                raise Exception('Weight already exists')
            if name_ in weight_class_names():
                raise Exception('Name already exists')

            w_class.weight = weight_
            w_class.name = name_
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

def create_fighter(weight_class_id_=None):
    try:
        name_ = input('Input name: ')
        age_ = input('Input age: ')
        wins_ = input('Input wins: ')
        losses_ = input('Input losses: ')
        
        Fighter.create(name_, age_, weight_class_id_, wins_, losses_)
        print('New fighter created')
    except Exception as exc:
        print('Error creating fighter', exc)

def update_fighter(fighter):
    try:
        fighter.name = input('Input new name: ')
        fighter.weight_class_id = Weight_class.find_by_weight(input('Input new weight (number only): ')).id
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
        same_date_fights = Fight.find_by_date(date_)

        for fight in same_date_fights:
            ftr_list = [ftr_1_.id, ftr_2_.id]
            if fight.ftr_1_id in ftr_list or fight.ftr_2_id in ftr_list:
                raise Exception('Fighters cannot fight twice in a day.')

        if ftr_1_.weight_class_id != ftr_2_.weight_class_id:
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
        same_date_fights = Fight.find_by_date(date_)

        for fight in same_date_fights:
            ftr_list = [ftr_1_.id, ftr_2_.id]
            if fight.ftr_1_id in ftr_list or fight.ftr_2_id in ftr_list:
                raise Exception('Fighters cannot fight twice in a day.')

        if ftr_1_.weight_class_id != ftr_2_.weight_class_id:
            raise Exception('Fighters must be in the same weight class.')
        elif ftr_1_ == ftr_2_:
            raise Exception('Fighters Must be unique')
        elif winner_ not in [ftr_1_, ftr_2_]:
            raise Exception('Winner must be one of the participants.')
        
        fight.date = date_
        fight.ftr_1_id = ftr_1_.id
        fight.ftr_2_id = ftr_2_.id
        fight.winner_id = winner_.id
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











