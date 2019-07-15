import threading


def threaded(name=None, daemon=False):
    def threaded_wrapper(fn):
        def wrapper(*args, **kwargs):
            threading.Thread(target=fn, args=args, kwargs=kwargs, name=name, daemon=daemon).start()
        return wrapper
    return threaded_wrapper
