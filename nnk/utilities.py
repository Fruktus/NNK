import threading


def threaded(name=None, daemon=False):
    def threaded_wrapper(fn):
        def wrapper(*args, **kwargs):
            t = threading.Thread(target=fn, args=args, kwargs=kwargs, name=name, daemon=daemon)
            t.start()
            # return t  # TODO maybe instead of removing the decorator make it return a reference to thread
        return wrapper
    return threaded_wrapper
