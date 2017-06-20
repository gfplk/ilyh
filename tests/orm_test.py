from threading import Thread
from ilyh.orm import create_pool, close_pool, __POOL, select, execute
import logging
import pprint
import sys
logging.basicConfig(level=logging.DEBUG)

KWARGS = {
    'user': 'gfplk',
    'password': '51job_fuck',
    'database': 'db_job',
    'charset': 'utf8',
    'host': 'ilyh.club'
}


def pool():
    global KWARGS
    create_pool(10, **KWARGS)
    for i in __POOL:
        print(i)
    close_pool()


def sel():
    global KWARGS
    create_pool(1, **KWARGS)
    sql = 'select * from tb_job'
    size = 2
    args = None

    def func():
        pprint.pprint(select(sql, args, size))

    tasks = [Thread(target=func) for i in range(10)]
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()


if __name__ == '__main__':
    try:
        # pool()
        sel()
    except KeyboardInterrupt as e:
        close_pool()
