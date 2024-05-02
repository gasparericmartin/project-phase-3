# lib/cli.py

import inquirer
from helpers import *

main_menu = [
    inquirer.List('choice',
                  message='Make a selection',
                  choices=['weight classes', 'fighters', 'fights'])

]

weight_classes = [
    inquirer.List('choice',
                    message='Make a selection',
                    choices=['display all classes', 'Search by weight', 'back',
                            'add weight class' ])
]

fighters = [
    inquirer.List('choice',
                    message='Make a selection',
                    choices=['Search by name', 'view all fighters', 'back'])
]

def main():
    while True:
        user_choice = inquirer.prompt(main_menu)['choice']
        print(user_choice)
        if user_choice == 'weight classes':
            user_choice = inquirer.prompt(weight_classes)['choice']
            if user_choice == 'back':
                print('return to main menu')
            elif user_choice == 'display all classes':
                print('displayed')
        elif user_choice == 'fighters':
            user_choice = inquirer.prompt(fighters)['choice']
            if user_choice == 'Search by name':
                print('Searched by name')
            elif user_choice == 'back':
                print('back to main menu')
        else:
            exit()
    


if __name__ == '__main__':
    main()
