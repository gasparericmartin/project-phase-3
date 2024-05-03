# lib/cli.py

import inquirer
import re
from helpers import *

main_menu = [
    inquirer.List('choice',
                  message='Make a selection',
                  choices=['Weight Classes', 'Fighters', 'Fights', 'Exit program'])

]

weight_classes = [
    inquirer.List('choice',
                    message='Make a selection',
                    choices=['Display All Classes', 'Search by Weight',
                            'Add Weight Class', 'Update Weight Class',
                            'Delete Weight Class', 'Back'])
]

fighters = [
    inquirer.List('choice',
                    message='Make a selection',
                    choices=['View All Fighters', 'Search by Name',
                            'Add Fighter', 'Update Fighter',
                            'Delete Fighter', 'Back'])
]

fighter_menu = [
    inquirer.List('choice',
                    message='Make a selection',
                    choices=['View Fights', 'View Opponents'])
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
    inquirer.Text('name', message='Input name: ')
]


def main():
    while True:
        user_choice = inquirer.prompt(main_menu)['choice']
        print(user_choice)
        if user_choice == 'Weight Classes':
            user_choice = inquirer.prompt(weight_classes)['choice']
            
            if user_choice == 'Display All Classes':
                display_all_weight_classes()
            elif user_choice == 'Search by Weight':
                weight = inquirer.prompt(weight_inquiry)['weight']
                weight_class_by_weight(weight)
            elif user_choice == 'Add Weight Class':
                create_weight_class()
            elif user_choice == 'Update Weight Class':
                #Fixed exit issue very ungracefully
                weight_class_choices = [
                    inquirer.List('choice',
                    message='Make a selection',
                    choices=weight_class_names())
                ]
                
                choice = inquirer.prompt(weight_class_choices)['choice']
                update_weight_class(choice)
            elif user_choice == 'Delete Weight Class':
                #Fixed exit issue very ungracefully
                weight_class_choices = [
                    inquirer.List('choice',
                    message='Make a selection',
                    choices=weight_class_names())
                ]
                
                choice = inquirer.prompt(weight_class_choices)['choice']
                delete_weight_class(choice)
            elif user_choice == 'Back':
                pass 

        
        elif user_choice == 'Fighters':
            user_choice = inquirer.prompt(fighters)['choice']
            
            if user_choice == 'View All Fighters':
                all_fighters()
            elif user_choice == 'Search by Name':
                name = inquirer.prompt(name_inquiry)['name']
                fighter_by_name(name)
            elif user_choice == 'Add Fighter':
                #remember to make weight validator
                create_fighter()
            elif user_choice == 'Update Fighter':
                fighter_choices = [
                    inquirer.List('choice',
                    message='Make a selection',
                    choices=fighter_names())
                ]

                choice = inquirer.prompt(fighter_choices)['choice']
                fighter = Fighter.find_by_name(choice)
                
                print('Current fighter info: ')
                display_fighter_info(fighter)
                update_fighter(fighter)
            elif user_choice == 'Delete Fighter':
                fighter_choices = [
                    inquirer.List('choice',
                    message='Make a selection',
                    choices=fighter_names())
                ]

                choice = inquirer.prompt(fighter_choices)['choice']
                fighter = Fighter.find_by_name(choice)

                delete_fighter(fighter)
            elif user_choice == 'Back':
                pass
        
        elif user_choice == 'Fights':
            user_choice = inquirer.prompt(fights)['choice']

            if user_choice == 'View All Fights':
                all_fights()
            elif user_choice == 'Search by Date':
                fights_by_date()
            elif user_choice == 'Add Fight':
                fighter_choices = [
                    inquirer.List('choice',
                    message='Make a selection',
                    choices=fighter_names())
                ]
                
                print('Enter fighter 1: ')
                f1 = inquirer.prompt(fighter_choices)['choice']
                print('Enter fighter 2: ')
                f2 = inquirer.prompt(fighter_choices)['choice']
                print('Enter winner: ')
                wnr = inquirer.prompt(fighter_choices)['choice']
                
                create_fight(f1, f2, wnr)
            elif user_choice == 'Update Fight':
                pass
            elif user_choice == 'Delete Fight':
                pass
            elif user_choice == 'Back':
                pass


        
        elif user_choice == 'Exit program':
            exit_program()
    


if __name__ == '__main__':
    main()
