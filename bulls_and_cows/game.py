# -*- coding: utf-8 -*-

from termcolor import cprint, colored

from engine import make_number, check_number

game = 'yes'
while game == 'yes':
    make_number()
    cprint('The number is puzzled', color='grey', attrs=['bold'])
    count_moves = 0
    while True:
        user_number = input(colored('Enter estimated number: ', color='yellow', attrs=['bold']))
        result = check_number(user_number=user_number)
        if result:
            count_moves += 1
            if result['bulls'] == 4:
                break
            cprint(f"bulls - {result['bulls']}, cows - {result['cows']}", color='blue')
        else:
            cprint('incorrect value, try again...', color='red', attrs=['dark'])
    cprint(f'You are win, the guessed number : {user_number}, moves : {count_moves}', color='cyan', attrs=['bold'])
    game = input(colored('Do you want to play again (yes/no)? > ', color='yellow', attrs=['bold'])).lower()
