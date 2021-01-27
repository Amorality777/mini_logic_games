from random import sample


def make_number():
    global number
    number = sample('0123456789', 4)
    if number[0] == '0':
        number.reverse()
    number = ''.join(number)


def valid_num(user_number: str):
    if len(user_number) != 4:
        flag = False
    elif not user_number.isdigit():
        flag = False
    elif len(set(user_number)) != 4:
        flag = False
    else:
        flag = True
    return flag


def check_number(user_number: str):
    if valid_num(user_number=user_number):
        result = {'bulls': 0, 'cows': 0}
        for order, digit in enumerate(user_number):
            if number[order] == digit:
                result['bulls'] += 1
            elif digit in number:
                result['cows'] += 1
        return result


number = '0'
