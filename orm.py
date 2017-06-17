from threading import Thread
from pymysql import Connection

__POOL = []


def create_pool(size, **kwargs):
    global __POOL
    for i in range(size):
        __POOL.append(Connection(kwargs))


def select():
    pass


def execute():
    pass


class Model(dict):
    pass


class Field(object):
    pass
