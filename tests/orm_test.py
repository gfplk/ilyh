from threading import Thread
from ilyh.orm import create_pool, close_pool, __POOL, select, execute
import logging
import pprint
import sys
import collections
import time
#logging.basicConfig(level=logging.DEBUG)

DB_JOB_KWARGS = {
    'user': 'gfplk',
    'password': '51job_fuck',
    'database': 'db_job',
    'charset': 'utf8',
    'host': 'ilyh.club'
}

DB_TEST_KWARGS = {
    'user': 'gfplk',
    'password': '51job_fuck',
    'database': 'db_test',
    'charset': 'utf8',
    'host': 'ilyh.club'
}


def pool():
    global KWARGS
    create_pool(10, **DB_JOB_KWARGS)
    for i in __POOL:
        print(i)
    close_pool()


def sel():
    global KWARGS
    create_pool(1, **DB_JOB_KWARGS)
    sql = 'select * from tb_job'
    size = 2
    args = None

    def func():
        pprint.pprint(select(sql, args, size))

    tasks = [Thread(target=func) for i in range(1000)]
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()

def exe():
    global KWARGS
    create_pool(10, **DB_TEST_KWARGS)
    sql = 'insert into tb_test(a, b, c, d) values(%s, %s, %s, %s)'
    test = {
        'a': 'a',
        'b': 'b',
        'c': 'c',
        'd': 'd',
    }
    args = (test['a'], test['b'], test['c'], test['d'])
    def func():
        pprint.pprint(execute(sql, args))
    tasks = [Thread(target=func) for i in range(1000)]
    now = time.time()
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
    now = time.time() - now
    print('spent %r seconds.' % now)

    for i in __POOL:
        print(i['is_used'])


if __name__ == '__main__':
    try:
        #pool()
        #sel()
        exe()
    except KeyboardInterrupt as e:
        close_pool()
