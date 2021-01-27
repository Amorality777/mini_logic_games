from random import sample


class EngineGame:
    def __init__(self):
        self.number = '0'

    def make_number(self):
        number = sample('0123456789', 4)
        if number[0] == '0':
            number.reverse()
        self.number = ''.join(number)

    def valid_num(self, user_number: str):
        if len(user_number) != 4:
            flag = False
        elif not user_number.isdigit():
            flag = False
        elif len(set(user_number)) != 4:
            flag = False
        else:
            flag = True
        return flag

    def check_number(self, user_number: str):
        if self.valid_num(user_number=user_number):
            result = {'bulls': 0, 'cows': 0}
            for order, digit in enumerate(user_number):
                if self.number[order] == digit:
                    result['bulls'] += 1
                elif digit in self.number:
                    result['cows'] += 1
            return result
