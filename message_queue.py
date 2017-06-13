import pika
from threading import Thread

class Base(object):
    def __init__(self, user, passwd, host):
        credentials = pika.PlainCredentials(user, passwd)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(
            host=host, credentials=credentials))
        self.ch = self.conn.channel()

    def __del__(self):
        self.ch.close()
        self.conn.close()


class _Task(Thread):
    def __init__(self, target, args, no_ack, ch, method, properties):
        super().__init__(target=target, args=args)
        self.no_ack = no_ack
        self.ch = ch
        self.method = method
        self.properties = properties

    def run(self):
        super().run()
        if self.no_ack == False:
            self.ch.basic_ack(delivery_tag = self.method.delivery_tag)


class Customer(Base):
    def __init__(self, user, passwd, host, prefetch_count, durable, no_ack, 
            task_queue, store_queue):
        super().__init__(user, passwd, host)

        self.task_queue = task_queue
        self.store_queue = store_queue
        self.prefetch_count = prefetch_count
        self.durable = durable
        self.no_ack = no_ack

    def sendTask(self, body):
        self.ch.basic_publish(exchange='', routing_key=self.task_queue, body=body)

    def storeData(self, data):
        self.ch.basic_publish(exchange='', routing_key=self.store_queue, body=data)
        
    def servForever(self, func):
        if self.task_queue != None:
            self.ch.queue_declare(queue=self.task_queue, durable=self.durable)
        if self.store_queue != None:
            self.ch.queue_declare(queue=self.store_queue, durable=self.durable)

        def callback(ch, method, properties, body):
            task = _Task(func, (self, body), self.no_ack, ch, method, properties)
            task.start()

        self.ch.basic_qos(prefetch_count=self.prefetch_count)
        self.ch.basic_consume(callback, queue=self.task_queue, no_ack=self.no_ack)
        self.ch.start_consuming()


class Producter(Base):
    def __init__(self, user, passwd, host, task_queue, durable):
        super().__init__(user, passwd, host)
        self.task_queue = task_queue
        self.durable = durable

    def sendTask(self, body):
        self.ch.basic_publish(exchange='', routing_key=self.task_queue, body=body)

    def produce(self, func):
        if self.task_queue != None:
            self.ch.queue_declare(queue=self.task_queue, durable=self.durable)
        func(self)
