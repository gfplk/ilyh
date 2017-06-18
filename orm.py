from threading import Thread
from pymysql import Connection

__POOL = []  # 数据库连接池


def create_pool(size, **kwargs):
    '''
    创建一个连接池
    '''   
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
