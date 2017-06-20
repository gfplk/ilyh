from threading import Thread, Lock, current_thread
import pymysql
from pymysql import Connection
import logging
import time

__POOL = []


class DBConnection(dict):
    is_used = None
    connection = None


def create_pool(size, **kwargs):
    logging.debug('create_pool(%r, %r' % (size, kwargs))
    global __POOL
    kwargs['cursorclass'] = pymysql.cursors.DictCursor
    for i in range(size):
        __POOL.append(DBConnection(
            is_used=False, connection=Connection(**kwargs)))


def close_pool():
    logging.debug('%r - close_pool()' % current_thread())
    global __POOL
    try:
        for p in __POOL:
            p['connection'].close()
    except:
        raise


__LOCK = Lock()


def get_connection():
    global __POOL, __LOCK
    with __LOCK:
        while 1:
            for conn in __POOL:
                if conn['is_used'] == False:
                    conn['is_used'] = True
                    return conn
            logging.debug('%r - waiting for other thread release the connection.' % current_thread())
            time.sleep(2)


def select(sql, args, size=None):
    log = '%r - select(%r, %r, %r)' % (current_thread(), sql, args, size)
    logging.debug(log)
    global __POOL, __LOCK
    conn = get_connection()
    logging.debug(log + '%r' % conn)
    try:
        with conn['connection'].cursor() as cursor:
            sql = sql.replace('?', '%s')
            if size and isinstance(size, int) and size >= 1:
                sql = ' '.join([sql, 'limit %d' % size])
            cursor.execute(sql, args or ())
            rs = cursor.fetchall()
            return [x for x in rs]
    except:
        raise
    finally:
        with __LOCK:
            conn['is_used'] = False


def execute(sql, args):
    global __POOL, __LOCK
    conn = get_connection()
    try:
        with conn['connection'].cursor() as cursor:
            cursor.execute(sql.replace('?', '%s'), args or ())
            affected = cursor.rowcount
            return affected
    except:
        conn.rollback()
        raise
    finally:
        with __LOCK:
            conn['is_used'] = False


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100'):
        super().__init__(name, ddl, primary_key, default)