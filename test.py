import unittest, logging
logging.basicConfig(level=logging.DEBUG)
from message_queue import *


class MessageQueueTest(unittest.TestCase):
    def test_base(self):
        base = Base('admin', '123456', 'db1.ichunt.com')
        print(base.conn)

    def test_1_send(self):
        def func(producter):
            func_args = ('Love Wang Xue', 'Love someone forever')
            print(func_args)
            for i in func_args:
                producter.sendTask(i)

        producter = Producter('admin', '123456', 'db1.ichunt.com', 
                'love', True)
        producter.produce(func)

    def test_2_customer(self):
        def func(body, customer):
            print('Received', body)
            customer.storeData(body)

        customer = Customer('admin', '123456', 'db1.ichunt.com', 5, True, False, 
                'love', 'love someone forever')
        customer.servForever(func)


if __name__ == '__main__':
    unittest.main()
