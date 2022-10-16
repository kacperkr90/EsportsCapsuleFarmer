import os


def read_boolean(env_name, default=False):
    return is_true(os.environ.get(env_name, default))


def read_string(env_name, default=''):
    return os.environ.get(env_name, default)


def read_int(env_name, default):
    return to_int_or_default(os.environ.get(env_name), default)


def is_containerized():
    return is_true(os.environ.get('CONTAINERISED', 'false'))


def is_true(s=''):
    return s == 'true'


def to_int_or_default(s, default):
    try:
        return int(s)
    except:
        return default
