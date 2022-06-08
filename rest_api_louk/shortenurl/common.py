import time
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug

def validate_url(url):
    pass

class local_timer:
    """
    Class designed to provide sampling capabilities-
    of the time the function is performed
    """
    BASE_MILESECONDS = 1000
    def __init__(self):
        self.first = self.eval_time()
        self.second = None
    def reset(self):
        self.first = self.eval_time()
    def get_current_time(self):
        self.second = self.eval_time()
        time_taken = self.second - self.first
        return f'{time_taken} milliseconds'
    
    def eval_time(self):
        return int(round(time.time() * self.BASE_MILESECONDS))


def valid_url(to_validate):
    validator = URLValidator()
    try:
        validator(to_validate)
        return True
    except ValidationError:
        return False


def valid_slug(to_validate):
    try:
        validate_slug(to_validate)
        return True
    except ValidationError:
        return False


#List of possible strings
SERVER_ON = 'Server status: on'
UNDEFINED_FORMULA = 'Illegal expression'
#List of possible system error
GENERAL_ERROR = 1000, 'General error'
TYPE_URL_ERROR = 1001, 'Type url error'
TYPE_SLUG_ERROR = 1002, 'Type slug error'
NO_OPERATOR_CLASS_FOUND = 1010, 'Dev team no.1010'