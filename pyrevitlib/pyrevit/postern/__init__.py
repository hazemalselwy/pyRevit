import threading
from functools import wraps


class Postern():
    def __init__(self):
        pass

    def route(target_url):
        def wrap(f):
            @wraps(f)
            def wrapped_f(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapped_f
        return wrap
