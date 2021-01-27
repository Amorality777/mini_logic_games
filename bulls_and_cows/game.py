# -*- coding: utf-8 -*-

from termcolor import cprint, colored

from engine import EngineGame


class BullsAndCows:
    def __init__(self):
        self.game = 'yes'
        self.engine = EngineGame()
        self.count_moves = 0
        self.user_number = None

    def play(self):
        while self.game == 'yes':
            self.number_generation()
            self.logic_game()
            self.game_over()

    def logic_game(self):
        while True:
            self.user_number = input(colored('Enter estimated number: ', color='yellow', attrs=['bold']))
            result = self.engine.check_number(user_number=self.user_number)
            if result:
                self.count_moves += 1
                if result['bulls'] == 4:
                    break
                cprint(f"bulls - {result['bulls']}, cows - {result['cows']}", color='blue')
            else:
                cprint('incorrect value, try again...', color='red', attrs=['dark'])

    def number_generation(self):
        self.engine.make_number()
        cprint('The number is puzzled', color='grey', attrs=['bold'])

    def game_over(self):
        cprint(f'You are win, the guessed number : {self.user_number}, moves : {self.count_moves}', color='cyan',
               attrs=['bold'])
        self.game = input(colored('Do you want to play again (yes/no)? > ', color='yellow', attrs=['bold'])).lower()



