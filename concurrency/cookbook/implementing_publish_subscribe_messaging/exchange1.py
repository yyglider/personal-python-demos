from collections import defaultdict


# an exchange is nothing more than an object that keeps a set of active subscribers
class Exchange:
    def __init__(self):
        self._subscribers = set()

    def attach(self, task):
        self._subscribers.add(task)

    def detach(self, task):
        self._subscribers.remove(task)

    # 调用所有订阅者的send方法
    def send(self, msg):
        for subscriber in self._subscribers:
            subscriber.send(msg) # 订阅者需要实现send方法


# Dictionary of all created exchanges
_exchanges = defaultdict(Exchange)


# Return the Exchange instance associated with a given name
def get_exchange(name):
    return _exchanges[name]


if __name__ == '__main__':
    # Example task (just for testing)
    class Task:
        def __init__(self, name):
            self.name = name

        def send(self, msg):
            print('{} got: {!r}'.format(self.name, msg))


    task_a = Task('A')
    task_b = Task('B')

    exc = get_exchange('spam')
    exc.attach(task_a)
    exc.attach(task_b)
    exc.send('msg1')
    exc.send('msg2')

    exc.detach(task_a)
    exc.detach(task_b)
    exc.send('msg3')
