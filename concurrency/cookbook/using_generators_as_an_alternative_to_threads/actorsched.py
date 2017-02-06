from collections import deque

# 协程执行的是无限循环，而且一开始就会停在首个yield表达式那里，等待有值传给它，协程会把收到的值当成yield表达式的值,
# 然后继续执行它所需的操作，等处理完之后，继续循环。
# 这样，我们就可以反复调用协程的send()和throw()方法向其push值了

class ActorScheduler:
    def __init__(self):
        self._actors = { }          # Mapping of names to actors
        self._msg_queue = deque()   # Message queue
    
    def new_actor(self, name, actor):
        '''
        Admit a newly started actor to the scheduler and give it a name
        '''
        self._msg_queue.append((actor,None))
        self._actors[name] = actor

    def send(self, name, msg):
        '''
        Send a message to a named actor
        '''
        actor = self._actors.get(name)
        if actor:
            # 将actor信息加入队列
            self._msg_queue.append((actor,msg))

    def run(self):
        '''
        Run as long as there are pending messages.
        '''
        while self._msg_queue:
            actor, msg = self._msg_queue.popleft()
            print('popleft msg queue:',actor,msg)
            try:
                 actor.send(msg)
            except StopIteration:
                 pass

# Example use
if __name__ == '__main__':
    def printer():
        while True:
            msg = yield
            print('Got:', msg)

    def counter(sched):
        while True:
            # Receive the current count
            n = yield    
            if n == 0:
                break
            # Send to the printer task
            sched.send('printer', n)
            # Send the next count to the counter task (recursive)
            sched.send('counter', n-1)

    sched = ActorScheduler()
    # Create the initial actors , new_actor(name,actor) and then append to queue
    sched.new_actor('printer', printer())
    sched.new_actor('counter', counter(sched))
    print(sched._actors)
    print(sched._msg_queue)

    # Send an initial message to the counter to initiate
    sched.send('counter', 100)
    print(sched._msg_queue)

    sched.run()
