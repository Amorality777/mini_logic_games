# -*- coding: utf-8 -*-
from random import randint, choice

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


class Human:
    ate_food = 0

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = None
        self.cat = None
        self.act_box = [self.eat, self.stroke_cat]

    def __str__(self):
        return f'{self.name} fullness: {self.fullness}, happiness: {self.happiness}'

    def go_to_house(self, house):
        self.house = house
        self.house.total_humans += 1

    def take_pet_home(self, cat):
        self.cat = cat
        self.cat.house = self.house
        self.house.total_pets += 1
        cprint(f'{self.name} took the cat {cat.name} home', color='cyan', attrs=['bold'])

    def eat(self):
        portion = 0
        if self.house.food >= 30:
            portion = 30
        elif self.house.food > 0:
            portion = self.house.food
        self.fullness += portion
        self.house.food -= portion
        Human.ate_food += portion
        if portion != 0:
            cprint(f'{self.name} eat', color='green')
        return portion

    def stroke_cat(self):
        if self.cat:
            self.happiness += 5
            self.fullness -= 10
            cprint(f'{self.name} stroke cat', color='yellow')

    def act(self):
        if self.fullness <= 0:
            cprint(f'{self.name} died of hunger', color='red')
            return
        elif self.happiness < 10:
            cprint(f'{self.name} died of depression', color='red')
            return
        elif self.house.dirty > 90:
            self.happiness -= 10

        if self.fullness <= 20:
            self.eat()
            return
        else:
            return True


class Husband(Human):
    earned_money = 0

    def __init__(self, name):
        super().__init__(name=name)
        self.act_box.extend([self.gaming, self.work])
        self.salary = 150

    def act(self):
        result = super().act()
        if result:
            if self.happiness <= 80:
                self.gaming()
            elif self.house.money <= 100:
                self.work()
            else:
                choice(self.act_box)()

    def eat(self):
        result = super().eat()
        if not result:
            cprint(f"{self.name} we don't have food, I'll go to the work", color='red')
            self.work()

    def work(self):
        self.house.money += self.salary
        self.fullness -= 10
        Husband.earned_money += 150
        cprint(f'{self.name} went to work', color='blue')

    def gaming(self):
        if self.happiness <= 100:
            self.happiness += 20
            self.fullness -= 10
            cprint(f'{self.name} play in WoT', color='green')
        else:
            cprint(f"{self.name} I'm so happy, I'd better go to work", color='white')
            self.work()


class Wife(Human):
    buy_coats = 0

    def __init__(self, name):
        super().__init__(name=name)
        self.act_box.extend([self.buy_food, self.buy_cat_feed, self.buy_fur_coat, self.clean_house])

    def act(self):
        result = super().act()
        if result:
            if self.house.food < 20 * self.house.total_humans:
                self.buy_food()
            elif self.house.cat_feed < 10 * self.house.total_pets:
                self.buy_cat_feed()
            elif self.house.dirty >= 80:
                self.clean_house()
            elif self.happiness < 80:
                self.buy_fur_coat()
            elif self.happiness <= 75:
                self.stroke_cat()
            else:
                choice(self.act_box)()

    def eat(self):
        result = super().eat()
        if not result:
            cprint(f"{self.name} we don't have food, I'll go to the store", color='red')
            self.buy_food()

    def sopping(self):
        if self.house.money > 100:
            units_food = 100
        elif self.house.money > 50:
            units_food = 50
        else:
            units_food = self.house.money
        self.house.money -= units_food
        self.fullness -= 10
        return units_food

    def buy_food(self):
        units_food = self.sopping()
        if units_food:
            self.house.food += units_food
            cprint(f'{self.name} bought {units_food} units of food', color='blue')
        else:
            cprint(f"{self.name} I can't buy food, I'll go to clean the house", color='red')
            self.clean_house()

    def buy_cat_feed(self):
        units_food = self.sopping()
        if units_food:
            self.house.cat_feed += units_food
            cprint(f'{self.name} bought {units_food} units of feed for cats', color='blue')
        else:
            cprint(f"{self.name} I can't buy food, I'll go to clean the house", color='red')
            self.clean_house()

    def buy_fur_coat(self):
        if self.house.money >= 350:
            if self.happiness < 120:
                self.house.money -= 350
                self.happiness += 60
                self.fullness -= 10
                Wife.buy_coats += 1
                cprint(f'{self.name} buy coat', color='green')
            else:
                cprint(f"{self.name} I'm so happy, I'd better go to the store", color='white')
                if self.house.food > self.house.cat_feed:
                    self.buy_cat_feed()
                else:
                    self.buy_food()
        else:
            cprint(f"{self.name} can't buy coat, I'll go to stroke cat", color='red')
            self.stroke_cat()

    def clean_house(self):
        dirty = self.house.dirty
        if dirty > 30:
            if dirty >= 100:
                dirty = 100
            self.house.dirty -= dirty
            self.fullness -= 10
            cprint(f'{self.name} clean the house', color='blue')
        else:
            cprint(f'{self.name} the house does not need cleaning', color='green')


class Child(Human):

    def __init__(self, name):
        super().__init__(name=name)
        self.act_box.clear()
        self.act_box.extend([self.eat, self.sleep])

    def __str__(self):
        return super().__str__()

    def act(self):
        if self.fullness <= 0:
            cprint(f'{self.name} died of hunger', color='red')
            return

        if self.fullness <= 20:
            self.eat()
        else:
            choice(self.act_box)()

    def eat(self):
        if self.fullness <= 100:
            if self.house.food >= 10:
                self.fullness += 10
                self.house.food -= 10
                cprint(f'{self.name} eat', color='yellow')
            else:
                cprint(f"{self.name} we don't have food", color='red')
                self.sleep()
        else:
            cprint(f'{self.name} not hungry')
            self.sleep()

    def sleep(self):
        self.fullness -= 10
        cprint(f'{self.name} sleep', color='yellow')


class Cat:

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.house = None

    def __str__(self):
        return f'{self.name} fullness {self.fullness}'

    def eat_feed(self):
        if self.house.cat_feed >= 10 * self.house.total_pets:
            cprint(f'{self.name} eat', color='yellow', attrs=['bold'])
            self.fullness += 20
            self.house.cat_feed -= 10
        elif self.house.cat_feed >= 10:
            self.fullness += 10
            self.house.cat_feed -= 5
        else:
            cprint(f"{self.name} no food, I'm angry at the owner will go spoil the furniture!",
                   color='red', attrs=['bold'])
            self.tear_wallpaper()

    def sleep(self):
        self.fullness -= 10
        cprint(f'{self.name} sleep', color='grey', attrs=['bold'])

    def tear_wallpaper(self):
        cprint(f'{self.name} tear wallpaper', color='blue', attrs=['bold'])
        self.fullness -= 10
        self.house.dirty += 5

    def act(self):
        if self.fullness <= 0:
            cprint(f'{self.name} died...', color='red', attrs=['bold'])
            return
        dice = randint(1, 6)
        if self.fullness <= 30:
            self.eat_feed()
        elif dice == 1:
            self.sleep()
        elif dice == 2:
            self.eat_feed()
        else:
            self.tear_wallpaper()


home = HouseWithGhosts()
serge = Husband(name='Serge')
masha = Wife(name='Maria')
baby = Child(name='Jerry')
my_cats = [
    Cat(name='Mur'),
    Cat(name='Garfield'),
    Cat(name='Catty'),
    Cat(name='Sleepy'),
    Cat(name='Honey'),
]
for person in (serge, masha, baby):
    person.go_to_house(house=home)

for my_cat in my_cats:
    serge.take_pet_home(cat=my_cat)

accidents = 5
for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    home.act()
    serge.act()
    masha.act()
    baby.act()
    for my_cat in my_cats:
        my_cat.act()
    if day % 365 // accidents == 0:
        home.special_act()
    cprint(serge, color='white', attrs=['bold'])
    cprint(masha, color='white', attrs=['bold'])
    cprint(baby, color='white', attrs=['bold'])
    for my_cat in my_cats:
        cprint(my_cat, color='white', attrs=['bold'])
    cprint(home, color='white', attrs=['bold'])
cprint(
    f'Total units:\n\tfood eaten: {Human.ate_food}'
    f'\n\tbought coats: {Wife.buy_coats}\n\tearned money: {Husband.earned_money}',
    color='yellow', attrs=['bold'])
cprint(f'Simulation results: '
       f'\n\taccidents: {home.accidents},'
       f'\n\tsalary: {serge.salary},'
       f'\n\tthe maximum number of cats: {home.total_pets}', color='green')