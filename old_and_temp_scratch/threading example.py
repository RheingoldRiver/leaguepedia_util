import threading
import time

def cat(param):
    for i in range(5):
        print(str(i) + "cat" + param)
        time.sleep(1)

def kitten():
    time.sleep(.5)
    for i in range(5):
        print(str(i) + "kitten")
        time.sleep(1)

t1 = threading.Thread(target=cat,kwargs={"param":x})
t2 = threading.Thread(target=kitten)

t1.start(kwargs={"x":"dogs"})
t2.start()
print('cats are the best 1')
t1.join(timeout=3)
t1.is_alive()
print('cats are the best')
