import pika

class Base(object):
    def __init__(self, user, passwd, host):
        credentials = pika.PlainCredentials(user, passwd)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(
            host=host, credentials=credentials))
        self.ch = self.conn.channel()

    def __del__(self):
        self.ch.close()
        self.conn.close()


class Customer(Base):
    def __init__(self, user, passwd, host, prefetch_count, durable, no_ack, 
            task_queue, store_queue):
        super().__init__(user, passwd, host)

        self.task_queue = task_queue
        self.store_queue = store_queue
        self.prefetch_count = prefetch_count
        self.durable = durable
        self.no_ack = no_ack

    def storeData(self, data):
        self.ch.basic_publish(exchange='', routing_key=self.store_queue, body=data)
        
    def serv_forever(self, func):
        self.ch.basic_qos(prefetch_count=self.prefetch_count)
        if self.task_queue != None:
            self.ch.queue_declare(queue=self.task_queue, durable=self.durable)
        if self.store_queue != None:
            self.ch.queue_declare(queue=self.store_queue, durable=self.durable)

        def callback(ch, method, properties, body):
            func(body, self)
            if self.no_ack == False:
                self.ch.basic_ack(delivery_tag = method.delivery_tag)

        self.ch.basic_consume(callback, queue=self.task_queue, no_ack=self.no_ack)
        self.ch.start_consuming()


class Producter(Base):
    def __init__(self, user, passwd, host, task_queue, durable):
        super().__init__(user, passwd, host)
        self.task_queue = task_queue
        self.durable = durable

    def sendTask(self, body):
        self.ch.basic_publish(exchange='', routing_key=self.task_queue, body=body)

    def produce(self, func, func_args):
        func(self, *func_args)
