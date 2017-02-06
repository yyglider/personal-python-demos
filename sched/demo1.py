import sched
import time

'''
The sched module implements a generic event scheduler for running tasks at specific times.
The scheduler class uses a time function to learn the current time,
and a delay function to wait for a specific period of time.
The actual units of time are not important,
 which makes the interface flexible enough to be used for many purposes.
'''

scheduler = sched.scheduler(time.time, time.sleep)


def print_event(name, start):
    now = time.time()
    elapsed = int(now - start)
    print('EVENT: {} elapsed={} name={}'.format(
        time.ctime(now), elapsed, name))

start = time.time()
print('START:', time.ctime(start))
scheduler.enter(2, 1, print_event, ('first', start))
scheduler.enter(3, 1, print_event, ('second', start))

scheduler.run()