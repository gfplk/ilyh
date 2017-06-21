#coding=utf-8
import time,threading
lock=threading.Lock()
def fun(str):
    print(time.strftime('%H:%M:%S'))
    time.sleep(5)

for i in range(10):
    t = threading.Thread(target=fun, args=('hi',)).start()
