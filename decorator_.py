from functools import wraps


def counter(func):
    @wraps(func)
    def _inner(*arg, **kwargs):
        result = func(*arg, **kwargs)
        _inner.n_count += 1
        return result

    _inner.n_count = 0

    return _inner
