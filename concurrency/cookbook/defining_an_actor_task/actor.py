from queue import Queue
from threading import Thread, Event

# Sentinel used for shutdown
class ActorExit(Exception):
    pass

class Actor:
    def __init__(self):
        self._mailbox = Queue()

    # 'sending' task is sth that can be sacled up into systems involving multiple process
    def send(self, msg):
        '''
        Send a message to the actor
        '''
        print('put msg to Queue: ',msg)
        self._mailbox.put(msg)

    def recv(self):
        '''
        Receive an incoming message
        '''
        msg = self._mailbox.get()
        print('get msg from Queue: ', msg)
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        '''
        Close the actor, thus shutting it down
        '''
        print('close, pug exit signal to Queue ... ')
        self.send(ActorExit)

    def start(self):
        '''
        Start concurrent execution
        '''
        print('start ...')
        self._terminated = Event()
        print('init event ... ')
        t = Thread(target=self._bootstrap)
        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()
            print('set event ... ')

    def join(self):
        self._terminated.wait()

    def run(self):
        '''
        Run method to be implemented by the user
        '''
        while True:
            msg = self.recv()

# Sample ActorTask
class PrintActor(Actor):
    def run(self):
        while True:
            msg = self.recv()
            print("Got:", msg)





if __name__ == '__main__':
    # Sample use
    p = PrintActor()
    p.start()
    p.send("Hello")
    p.send("World")
    p.close()
    p.join()

    # Sample use 2
    # defined by generators
    # def PrintActorGen():
    #     while True:
    #         try:
    #             msg = yield
    #             print("Got:", msg)
    #         except GeneratorExit:
    #             print("actor terminating")
    # p = PrintActorGen()
    #
    # next(p)
    # p.send('hello')
    # p.send('world')
    # p.close()