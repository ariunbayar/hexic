from random import randint
import re


def generate_password():
    return randint(1000, 9999)


def is_deposit(phone_number, msg):
    if phone_number == '+976596':
        pattern = r'^\(Tand ([0-9]{8}) dugaaraas ([0-9]{3,}) negj ilgeelee\)'
        regex = re.compile(pattern, re.IGNORECASE)
        match = regex.match(msg)

        if match:
            return int(match.group(1)), int(match.group(2))

    return None, None
