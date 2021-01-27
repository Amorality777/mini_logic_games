from termcolor import cprint

from family_simulator.houses import HouseWithGhosts
from family_simulator.humans import Husband, Wife, Child, Human
from family_simulator.pets import Cat


class FamilySimulator:
    cats_names = ('Garfield', 'Mur', 'Catty', 'Sleepy', 'Honey', 'Sammy')

    def __init__(self, husband: str = 'Serge', wife: str = 'Maria', child: str = 'Jerry'):
        self.number_days_simulation = 365
        self.home = HouseWithGhosts()
        self.husband = Husband(name=husband)
        self.wife = Wife(name=wife)
        self.baby = Child(name=child)
        self.cat = Cat
        self.count_cats = 5
        self.my_cats = []
        self.accidents = 5

    def play(self):
        self.move_into_house()
        self.take_home_pet()
        self.simulate()

    def move_into_house(self):
        for person in (self.husband, self.wife, self.baby):
            person.go_to_house(house=self.home)

    def take_home_pet(self):
        self.count_cats = self.count_cats if len(self.cats_names) >= self.count_cats else len(self.cats_names)
        for i in range(self.count_cats):
            self.my_cats.append(self.cat(name=self.cats_names[i]))
        for my_cat in self.my_cats:
            self.husband.take_pet_home(cat=my_cat)

    def simulate(self):
        for day in range(self.number_days_simulation):
            cprint('================== День {} =================='.format(day), color='red')
            self.acts(day)
            self.print_day_stats()
        self.print_total_stats()

    def print_total_stats(self):
        cprint(
            f'Total units:\n\tfood eaten: {Human.ate_food}'
            f'\n\tbought coats: {Wife.buy_coats}\n\tearned money: {Husband.earned_money}',
            color='yellow', attrs=['bold'])
        cprint(f'Simulation results: '
               f'\n\taccidents: {self.home.accidents},'
               f'\n\tsalary: {self.husband.salary},'
               f'\n\tthe maximum number of cats: {self.home.total_pets}', color='green')

    def print_day_stats(self):
        cprint(self.husband, color='white', attrs=['bold'])
        cprint(self.wife, color='white', attrs=['bold'])
        cprint(self.baby, color='white', attrs=['bold'])
        for cat in self.my_cats:
            cprint(cat, color='white', attrs=['bold'])
        cprint(self.home, color='white', attrs=['bold'])

    def acts(self, day):
        self.home.act()
        self.husband.act()
        self.wife.act()
        self.baby.act()
        for cat in self.my_cats:
            cat.act()
        if day % 365 // self.accidents == 0:
            self.home.special_act()
