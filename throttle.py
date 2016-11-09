import datetime
from datetime import datetime as dt
from functools import wraps

class throttle(object):

    def __init__(self, seconds = 0, minutes= 0 , hours = 0):
        self.throttle_period = datetime.timedelta(
            seconds = seconds,
            minutes = minutes,
            hours = hours
        )
        self.time_of_last_call = dt.min
    
    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            now = dt.now()
            time_since_last_call = now - self.time_of_last_call

            if time_since_last_call > self.throttle_period:
                self.time_of_last_call = now
                return fn(*args, **kwargs)
        
        return wrapper