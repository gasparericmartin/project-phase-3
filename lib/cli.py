#!/usr/bin/env python3

import inquirer
import re
import datetime
from helpers import *

def date_validator(answers, date):
    month = date[0:2]
    day = date[3:5]
    year = date[6:]

    current_day = datetime.datetime.now()

    try:
        datetime.datetime(int(year), int(month), int(day))

        if not re.fullmatch(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', date):
            raise inquirer.errors.ValidationError('Improper date format')
        
        elif int(year) not in range(1993, datetime.datetime.now().year + 1):
            raise Exception('Only past fights between 1993 and the present may be logged.')
        elif int(year) == current_day.year:
            if int(month) > current_day.month:
                raise Exception('No future dates allowed.')
            elif int(month) == current_day.month and int(day) > current_day.day:
                raise Exception('No future dates allowed')
            else:
                return True
        else:
            return True
    
    except Exception as exc:
        print(' Date Error: ', exc)

def name_validator(answers, name):
    if not re.fullmatch(r'[A-z]+[ -][A-z]*[ -]*[A-z]+', name):
        raise inquirer.errors.ValidationError('', reason='Name must be ' +\
                                                'two or three words separated by' +\
                                                'hyphens or spaces.')
    return True
    
main_menu = [
    inquirer.List('choice',
                  message='Make a selection',
                  choices=['Weight Classes', 'Fighters', 'Fights', 'Exit program'])

]

weight_classes = [
    inquirer.List('choice',
                    message='Make a selection',
                    choices=['Display All Classes', 'Search by Weight', 
                            'Fighters by Weight Class',
                            'Add Weight Class', 'Update Weight Class',
                            'Delete Weight Class', 'Back'])
]

fighters = [
    inquirer.List('choice',
                    message='Make a selection',
                    choices=['View All Fighters', 'Search by Name',
                            'View Fights or Opponents',
                            'Add Fighter', 'Update Fighter',
                            'Delete Fighter', 'Back'])
]

fighter_menu = [
    inquirer.List('choice',
                    message='Make a selection',
                    choices=['View Fights', 'View Opponents', 'Back'])
]

fights = [
    inquirer.List('choice',
                    message='Make a selection',
                    choices=['View All Fights', 'Search by Date',
                            'Add Fight', 'Update Fight', 'Delete Fight',
                            'Back'])
]

weight_inquiry = [
    inquirer.Text('weight', message='Input weight (number only): ',
                  validate=lambda _, x: re.match(r'[0-9]{3}', x))
]

name_inquiry = [
    inquirer.Text('name', message='Input name: ', validate=name_validator)
]

date_inquiry = [
    inquirer.Text('date', message='Input date in 01/01/2001 format: ',
                  validate=date_validator)
]

def choices(func):
    return [
        inquirer.List('choice',
        message='Make a selection',
        choices=func())
    ]


def main():
    while True:
        user_choice = inquirer.prompt(main_menu)['choice']
        
        if user_choice == 'Weight Classes':
            weight_classes_loop()

        elif user_choice == 'Fighters':
            fighters_loop()
        
        elif user_choice == 'Fights':
            fights_loop()

        elif user_choice == 'Exit program':
            exit_program()

def weight_classes_loop():
    while True:
        user_choice = inquirer.prompt(weight_classes)['choice']
                
        if user_choice == 'Display All Classes':
            display_all_weight_classes()
                
        elif user_choice == 'Search by Weight':
            weight = inquirer.prompt(weight_inquiry)['weight']
            weight_class_by_weight(weight)
                
        elif user_choice == 'Fighters by Weight Class':
            weight_class_choices = choices(weight_class_names) if weight_class_names() else None
        
            if weight_class_choices:
                choice = inquirer.prompt(weight_class_choices)['choice']
                weight_class = Weight_class.find_by_name(choice)

                # fighters_in_class(weight_class)
                [display_fighter_info(fighter) for fighter in weight_class.all_fighters_in_class()]
            else:
                print('No weight classes to access')

        elif user_choice == 'Add Weight Class':
            create_weight_class()
                
        elif user_choice == 'Update Weight Class':
            weight_class_choices = choices(weight_class_names) if weight_class_names() else None

            if weight_class_choices:
                choice = inquirer.prompt(weight_class_choices)['choice']
                update_weight_class(choice)
            else: 
                print('No weight classes to update')
                
        elif user_choice == 'Delete Weight Class':
            weight_class_choices = choices(weight_class_names) if weight_class_names() else None

            if weight_class_choices:        
                choice = inquirer.prompt(weight_class_choices)['choice']
                delete_weight_class(choice)
            else:
                print('No weight classes to delete')
                
        elif user_choice == 'Back':
            main()

def fighters_loop():
    while True:
        user_choice = inquirer.prompt(fighters)['choice']
                
        if user_choice == 'View All Fighters':
            all_fighters()
                
        elif user_choice == 'Search by Name':
            name = inquirer.prompt(name_inquiry)['name']
            fighter_by_name(name)
                
        elif user_choice == 'View Fights or Opponents':
            fighter_choices = choices(fighter_names) if fighter_names() else None
            
            if fighter_choices:
                choice = inquirer.prompt(fighter_choices)['choice']
                menu_choice = inquirer.prompt(fighter_menu)['choice']

                print(menu_choice)

                if menu_choice == 'View Opponents':
                    fighter_opponents(choice)
                elif menu_choice == 'View Fights':
                    fighter_fights(choice)
            else:
                print('No fighters in database')
                
        elif user_choice == 'Add Fighter':
            class_choices_in_lbs = choices(weight_class_weights) if weight_class_weights() else None

            if class_choices_in_lbs:
                print('Choose your fighter\'s weight class')
                raw_choice = inquirer.prompt(class_choices_in_lbs)['choice']
                w_class = Weight_class.find_by_weight(raw_choice)

                create_fighter(w_class)
            else:
                create_fighter()
                
        elif user_choice == 'Update Fighter':
            fighter_choices = choices(fighter_names) if fighter_names() else None

            if fighter_choices:
                choice = inquirer.prompt(fighter_choices)['choice']
                fighter = Fighter.find_by_name(choice)
                        
                print('Current fighter info: ')
                display_fighter_info(fighter)
                update_fighter(fighter)
            else:
                print('No fighters to update')
                
        elif user_choice == 'Delete Fighter':
            fighter_choices = choices(fighter_names) if fighter_names() else None
            
            if fighter_choices:
                choice = inquirer.prompt(fighter_choices)['choice']
                fighter = Fighter.find_by_name(choice)

                delete_fighter(fighter)
            else:
                print('No fighters to delete')
                
        elif user_choice == 'Back':
            main()

def fights_loop():
    while True:
        user_choice = inquirer.prompt(fights)['choice']

        if user_choice == 'View All Fights':
            all_fights()
        
        elif user_choice == 'Search by Date':
            fights_by_date()
        
        elif user_choice == 'Add Fight':
            fighter_choices = choices(fighter_names)
            
            print('Enter fighter 1: ')
            f1 = inquirer.prompt(fighter_choices)['choice']
            print('Enter fighter 2: ')
            f2 = inquirer.prompt(fighter_choices)['choice']
            print('Enter winner: ')
            wnr = inquirer.prompt(fighter_choices)['choice']
            date_ = inquirer.prompt(date_inquiry)['date']

            
            create_fight(date_, f1, f2, wnr)
        
        elif user_choice == 'Update Fight':
            fight_choices = choices(all_fight_info)
            fighter_choices = choices(fighter_names)
            
            raw_choice = inquirer.prompt(fight_choices)['choice']
            choice = re.findall(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', raw_choice)[0]
            fight_s = fights_by_date(choice, False)

            print('Enter new fighter 1: ')
            f1 = inquirer.prompt(name_inquiry)['name']
            print('Enter new fighter 2: ')
            f2 = inquirer.prompt(name_inquiry)['name']
            print('Enter new winner: ')
            wnr = inquirer.prompt(name_inquiry)['name']
            print('Enter new date: ')
            date_ = inquirer.prompt(date_inquiry)['date']
            
            if len(fight_s) == 1:
                update_fight(fight_s[0], f1, f2, wnr, date_)
            else:
                search_name = re.search(r'[A-z]+[ -][A-z]*[ -]*[A-z]+', raw_choice).group()
                for fight in fight_s:
                    compare_name = Fighter.find_by_id(fight.ftr_1).name
                    if search_name == compare_name:
                        update_fight(fight, f1, f2, wnr, date_)
            
        elif user_choice == 'Delete Fight':
            fight_choices = choices(all_fight_info)

            raw_choice = inquirer.prompt(fight_choices)['choice']
            choice = re.findall(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', raw_choice)[0]
            fight_s = fights_by_date(choice, False)
            
            if len(fight_s) == 1:
                delete_fight(fight_s[0])
            else:
                search_name = re.search(r'[A-z]+[ -][A-z]*[ -]*[A-z]+', raw_choice).group()
                for fight in fight_s:
                    compare_name = Fighter.find_by_id(fight.ftr_1).name
                    if search_name == compare_name:
                        delete_fight(fight)
                
        elif user_choice == 'Back':
            main()

    


if __name__ == '__main__':
    Weight_class.create_table()
    Fighter.create_table()
    Fight.create_table()
    
    main()
