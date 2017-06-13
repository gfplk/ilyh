from message_queue import *
import time


class MessageQueueTest:
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
        def func(customer, body):
            print('Received', body)
            customer.storeData(body)
            time.sleep(10)
            

        customer = Customer('admin', '123456', 'ilyh.club', 5, True, False, 
                'love', 'love someone forever')
        customer.servForever(func)


if __name__ == '__main__':
    mqt = MessageQueueTest()
    mqt.test_1_send()
    mqt.test_2_customer()
