from random import choice

from termcolor import cprint


class House:

    def __init__(self):
        self.money = 100
        self.food = 50
        self.dirty = 0
        self.cat_feed = 30
        self.total_pets = 0
        self.total_humans = 0

    def __str__(self):
        return f'In house money: {self.money}, food: {self.food},' \
               f'feed for cats: {self.cat_feed}, dirty: {self.dirty}.'

    def act(self):
        self.dirty += 5


class HouseWithGhosts(House):

    def __init__(self):
        super().__init__()
        self.special_act_box = [self.lost_money, self.lost_food]
        self.accidents = 0

    def special_act(self):
        self.accidents += 1
        choice(self.special_act_box)()

    def lost_money(self):
        self.money //= 2
        cprint(f'somewhere half the money was gone', color='red', attrs=['bold', 'underline', 'reverse'])

    def lost_food(self):
        self.food //= 2
        cprint(f'somewhere half the food was gone', color='red', attrs=['bold', 'underline', 'reverse'])
