from queue import Queue
from threading import Thread
import time

_sentinel = object()


# A thread that produces data
def producer(out_q):
    n = 10
    while n > 0:
        # Produce some data
        out_q.put(n)
        time.sleep(2)
        n -= 1

    # Put the sentinel on the queue to indicate completion
    out_q.put(_sentinel)


# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()

        # Check for termination
        if data is _sentinel:
            in_q.put(_sentinel)
            break

        # Process the data
        print('Got:', data)
    print('Consumer shutting down')


# 如果生产者线程需要立即知道消费线程是否处理数据了，此时应该将发送数据包装成一个Event对象

from threading import Event

def producer_event(out_q):
    n = 10
    while n > 0:
        # produce some data
        data = n
        # make an (data,event) pair and hand it to the consumer
        evt = Event()
        out_q.put((data, evt))
        time.sleep(2)
        # wait for the consumer to process
        evt.wait()
        n -= 1
        print("consumed!")


def consumer_event(in_q):
    while True:
        # Get some data
        data, evt = in_q.get()

        # Check for termination
        if data is _sentinel:
            in_q.put(_sentinel)
            break
        # Process the data
        print('Got:', data)
        evt.set()
    print('Consumer shutting down')


if __name__ == '__main__':
    q = Queue()  # already have all of the required locking
    t1 = Thread(target=consumer_event, args=(q,))
    t2 = Thread(target=producer_event, args=(q,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
