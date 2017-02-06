import sched
import time

'''
 Each event is run in the same thread, so if an event takes longer to run than the delay between events,
 there will be overlap. The overlap is resolved by postponing the later event.
 No events are lost, but some events may be called later than they were scheduled.

'''



scheduler = sched.scheduler(time.time, time.sleep)


def long_event(name):
    print('BEGIN EVENT :', time.ctime(time.time()), name)
    time.sleep(2)
    print('FINISH EVENT:', time.ctime(time.time()), name)

print('START:', time.ctime(time.time()))
scheduler.enter(2, 1, long_event, ('first',))
scheduler.enter(3, 1, long_event, ('second',))

scheduler.run()