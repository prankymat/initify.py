def init_args(exclude=[]):
    def decorator(func):
        import inspect, functools
        argspec = inspect.getargspec(func)
        argnames = argspec.args[1:]

        d = argspec.defaults
        if not argnames or not d:
            d = {x : None for x in argnames}

        defaults = dict(zip(argnames[-len(d):], d))
        @functools.wraps(func)
        def __init__(self, *args, **kwargs):
            args_it = iter(args)
            for key in argnames:
                if key in kwargs:
                    value = kwargs[key]
                else:
                    try:
                        value = next(args_it)
                    except StopIteration:
                        value = defaults[key]
                setattr(self, key, value)
            func(self, *args, **kwargs)
            super(type(self), self).__init__(self)

            for var in exclude:
                delattr(self, var)
        return __init__
    return decorator
