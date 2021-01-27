# -*- coding: utf-8 -*-

import csv
import json
import re
import time
from datetime import datetime
from decimal import Decimal, getcontext

from termcolor import cprint

from game_text import text_dict


class RPGMap:
    getcontext().prec = 20
    remaining_time = '123456.0987654321'
    time_for_game = Decimal(remaining_time)
    field_names = ['current_location', 'current_experience', 'current_date']
    map_file = "rpg.json"
    result_file = 'dungeon.csv'

    def __init__(self):
        self.map_game = self._init_map()
        self.available_loc = []
        self.hero = Hero()
        self.text = self.hero.text

    def _init_map(self):
        with open(self.map_file, "r") as rpg:
            map_game = json.load(rpg)
        return map_game['Location_0_tm0']

    def restart_game(self):
        self.map_game = self._init_map()
        self.available_loc = []
        self.hero.restart_hero()
        self.run()

    def run(self):
        with open(self.result_file, "a", newline='') as out_file:
            while not self.hero.game_over():
                self.hero.look_stats()
                self._init_hero_acts()
                self.hero.act_choice()
                self.move()
                self.write_result(out_file)
        if self.hero.game_ending == 'Win':
            print(self.text['good end'])
        else:
            print(f"{self.hero.game_ending}\n{self.text['bad end']}")
            self.restart_game()

    def move(self):
        if 'Location' in self.hero.act:
            step = self.available_loc.index(self.hero.act)
            self.map_game = self.map_game[step][self.hero.act]

    def _init_hero_acts(self):
        self.available_loc = []
        self.hero.acts_for_choice = []
        for loc in self.map_game:
            if isinstance(loc, dict):
                for loc_name in loc:
                    self.available_loc.append(loc_name)
                    self.hero.acts_for_choice.append(loc_name)
            else:
                self.available_loc.append(loc)
                self.hero.acts_for_choice.append(loc)

    def write_result(self, out_file):
        now = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        row = {'current_location': self.hero.location, 'current_experience': self.hero.exp, 'current_date': now}
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=self.field_names)
        writer.writerow(row)


class Hero:
    loc_patt = re.compile(r'Location.*(\d+)_tm([\d.]+)')
    hatch_patt = re.compile(r'Hatch_tm([\d.]+)')
    mob_patt = re.compile(r'(Mob|Boss).*exp(\d+)_tm([\d.]+)')

    def __init__(self):
        self.lang = 'en'
        self.language()
        self.text = text_dict[self.lang]
        self.name = input(self.text['name'])
        self.exp = 0
        self.act = ''
        self.started_at = time.time()
        self.acts_for_choice = []
        self.choice = None
        self.time_left = RPGMap.time_for_game
        self.location = 'Location_0_tm0'
        self.game_ending = None
        self.count_acts = 0

    def language(self):
        lang = input(f'Choose language: {[x for x in text_dict]}: ')
        if lang == 'ru':
            self.lang = lang
        print(f'{text_dict[self.lang]["lang"]}{self.lang}')

    def restart_hero(self):
        self.exp = 0
        self.act = ''
        self.acts_for_choice = []
        self.time_left = RPGMap.time_for_game
        self.location = 'Location_0_tm0'
        self.game_ending = None
        self.choice = None

    def act_choice(self):
        if self.acts_for_choice:
            self.print_start_step()
            self.choice = input(f'{self.name}{self.text["choice"]}')
        else:
            self.choice = ''
            self.act = self.game_ending = 'Empty location'
        if self.choice.isdigit() and (0 <= int(self.choice) <= self.count_acts):
            self.act = self.acts_for_choice[int(self.choice)]
            if 'Location' in self.act:
                self.move()
            elif 'Mob' in self.act or 'Boss' in self.act:
                self.fight()
            elif 'Hatch' in self.act:
                self.try_hatch()
        elif 'exit' in self.choice.lower() or 'выход' in self.choice.lower():
            exit(self.text['exit'])
        elif self.act != 'Empty location':
            cprint(self.text['invalid value'], color='red')
            self.act_choice()

    def look_stats(self):
        color = 'blue'
        cprint(f'{self.text["location"]} {self.location}', color=color)
        cprint(f'{self.text["stats"][0]} {self.exp} {self.text["stats"][1]} '
               f'{self.time_left} {self.text["stats"][2]}',
               color=color)
        delta = time.time() - self.started_at
        delta = time.gmtime(delta)
        cprint(f'{self.text["time"]}{delta.tm_min}:{delta.tm_sec}', color=color)

    def try_hatch(self):
        time_spent = self.hatch_patt.search(self.act)[1]
        self.time_left -= Decimal(time_spent)
        if self.time_left > Decimal(0) and self.exp >= 280:
            self.game_ending = 'Win'
        else:
            self.game_ending = 'Not enough time or exp'

    def print_start_step(self):
        color = 'blue'
        cprint(self.text["inside"], color=color)
        if self.acts_for_choice:
            for num, act in enumerate(self.acts_for_choice):
                if 'Location' in act:
                    cprint(f'{num}--> {self.text["location_list"]}{act}', color='green')
                elif 'Mob' in act or 'Boss' in act:
                    cprint(f'{num}--> {self.text["monster"]}{act}', color='red')
                else:
                    cprint(f'{num}--> {self.text["see_exit"]}{act}', color='green')
        self.count_acts = len(self.acts_for_choice) - 1
        text = f'{self.text["choice_act"][0]}{self.count_acts}{self.text["choice_act"][1]}'
        cprint(text, color=color)

    def fight(self):
        fight_info = self.mob_patt.search(self.act)
        exp, time_spent = fight_info[2], fight_info[3]
        self.time_left -= Decimal(time_spent)
        self.exp += int(exp)
        self.acts_for_choice.remove(self.act)
        cprint(f'{self.name} {self.text["fight"]}', color='red')
        self.look_stats()
        self.act_choice()

    def move(self):
        self.location = self.act
        time_spent = self.loc_patt.search(self.act)[2]
        self.time_left -= Decimal(time_spent)
        cprint(f'{self.name} {self.text["move"]} {self.act}', color='green')

    def game_over(self):
        if self.time_left <= Decimal(0):
            self.game_ending = 'Time out'

        if self.game_ending:
            return True


if __name__ == '__main__':
    my_game = RPGMap()
    my_game.run()
