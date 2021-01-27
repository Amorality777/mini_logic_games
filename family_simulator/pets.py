from random import randint

from termcolor import cprint


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
