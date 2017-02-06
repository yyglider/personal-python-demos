"""A generally useful event scheduler class.

Each instance of this class manages its own queue. No multi-threading is implied;

Each instance is parametrized with two functions,
one that is supposed to return the current time,
one that is supposed to implement a delay.


You can implement real-time scheduling by substituting time and sleep from built-in module time,
or you can implement simulated time by writing your own functions.

Events are specified by tuples (time, priority, action, argument, kwargs).
As in UNIX, lower priority numbers mean higher priority; in this
way the queue can be maintained as a priority queue.

Execution of the event means calling the action function, passing it the argument
sequence in "argument" (remember that in Python, multiple function
arguments are be packed in a sequence) and keyword parameters in "kwargs".

"""
# XXX The timefunc and delayfunc should have been defined as methods
# XXX so you can define new kinds of schedulers using subclassing
# XXX instead of having to define a module or class just to hold
# XXX the global state of your particular time and delay functions.

import time
import heapq
from collections import namedtuple
try:
    import threading
except ImportError:
    import dummy_threading as threading
from time import monotonic as _time

__all__ = ["scheduler"]

class Event(namedtuple('Event', 'time, priority, action, argument, kwargs')):
    def __eq__(s, o): return (s.time, s.priority) == (o.time, o.priority)
    def __lt__(s, o): return (s.time, s.priority) <  (o.time, o.priority)
    def __le__(s, o): return (s.time, s.priority) <= (o.time, o.priority)
    def __gt__(s, o): return (s.time, s.priority) >  (o.time, o.priority)
    def __ge__(s, o): return (s.time, s.priority) >= (o.time, o.priority)

_sentinel = object()

class scheduler:

    def __init__(self, timefunc=_time, delayfunc=time.sleep):
        """Initialize a new instance, passing the time and delay functions"""
        self._queue = []
        self._lock = threading.RLock()
        self.timefunc = timefunc
        self.delayfunc = delayfunc

    def enterabs(self, time, priority, action, argument=(), kwargs=_sentinel):
        """Enter a new event in the queue at an absolute time.
        Returns an ID for the event which can be used to remove it, if necessary.
        """
        if kwargs is _sentinel:
            kwargs = {}
        event = Event(time, priority, action, argument, kwargs)
        with self._lock:
            print('lock and add to heap',event)
            # heapq 是一个最小堆，堆顶元素 _queue[0] 永远是最小的. 和 Java 中的优先队列类似
            heapq.heappush(self._queue, event)
        return event # The ID

    def enter(self, delay, priority, action, argument=(), kwargs=_sentinel):
        """A variant that specifies the time as a relative time.
        This is actually the more commonly used interface.
        """
        time = self.timefunc() + delay
        return self.enterabs(time, priority, action, argument, kwargs)

    def cancel(self, event):
        """Remove an event from the queue.

        This must be presented the ID as returned by enter().
        If the event is not in the queue, this raises ValueError.

        """
        with self._lock:
            self._queue.remove(event)
            heapq.heapify(self._queue)

    def empty(self):
        """Check whether the queue is empty."""
        with self._lock:
            return not self._queue

    def run(self, blocking=True):
        """Execute events until the queue is empty.
        If blocking is False executes the scheduled events due to
        expire soonest (if any) and then return the deadline of the
        next scheduled call in the scheduler.

        When there is a positive delay until the first event, the
        delay function is called and the event is left in the queue;
        otherwise, the event is removed from the queue and executed
        (its action function is called, passing it the argument).  If
        the delay function returns prematurely, it is simply
        restarted.

        It is legal for both the delay function and the action
        function to modify the queue or to raise an exception;
        exceptions are not caught but the scheduler's state remains
        well-defined so run() may be called again.

        A questionable hack is added to allow other threads to run:
        just after an event is executed, a delay of 0 is executed, to
        avoid monopolizing the CPU when other threads are also
        runnable.

        """
        # localize variable access to minimize overhead
        # and to improve thread safety
        print('begin running!')
        lock = self._lock
        q = self._queue
        delayfunc = self.delayfunc
        timefunc = self.timefunc
        pop = heapq.heappop
        print('pop out event:',pop)
        while True:
            with lock:
                if not q:
                    break
                print(q[0])
                time, priority, action, argument, kwargs = q[0]
                now = timefunc()
                if time > now:
                    print('time > now')
                    delay = True
                else:
                    print('time < now')
                    delay = False
                    pop(q)
            if delay:
                if not blocking:
                    return time - now
                delayfunc(time - now)
            else:
                action(*argument, **kwargs)
                delayfunc(0)   # Let other threads run

    @property
    def queue(self):
        """An ordered list of upcoming events.

        Events are named tuples with fields for:
            time, priority, action, arguments, kwargs

        """
        # Use heapq to sort the queue rather than using 'sorted(self._queue)'.
        # With heapq, two events scheduled at the same time will show in
        # the actual order they would be retrieved.
        with self._lock:
            events = self._queue[:]
        return list(map(heapq.heappop, [events]*len(events)))

if __name__ == '__main__':
    scheduler = scheduler(time.time, time.sleep)


    def print_event(name, start):
        now = time.time()
        elapsed = int(now - start)
        print('EVENT: {} elapsed={} name={}'.format(
            time.ctime(now), elapsed, name))


    start = time.time()
    print('START:', time.ctime(start))
    #  enter(self, delay, priority, action, argument=(), kwargs=_sentinel):
    scheduler.enter(2, 1, print_event, ('first', start))
    scheduler.enter(3, 1, print_event, ('second', start))
    print(scheduler.queue)

    scheduler.run()