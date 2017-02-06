#!/usr/bin/env python3

# IO密集型并发
# 用队列及线程实现并发

import argparse
import multiprocessing
import os
import queue
import tempfile
import threading
import webbrowser
import Feed
import Qtrac


def main():
    limit, concurrency = handle_commandline()
    Qtrac.report("starting...")
    filename = os.path.join(os.path.dirname(__file__), "whatsnew.dat")
    jobs = queue.Queue()  # joinable queue
    results = queue.Queue()
    create_threads(limit, jobs, results, concurrency)   # 创建线程
    todo = add_jobs(filename, jobs)
    process(todo, jobs, results, concurrency)


def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--limit", type=int, default=0,
                        help="the maximum items per feed [default: unlimited]")
    parser.add_argument("-c", "--concurrency", type=int,
                        default=multiprocessing.cpu_count() * 4,
                        help="specify the concurrency (for debugging and "
                             "timing) [default: %(default)d]")
    args = parser.parse_args()
    return args.limit, args.concurrency


# 想在队列上调用join方法就必须保证queue.Queue.get和queue.Queue.task_done一一对应
# queue.Queue是一个线程安全的队列，而且是一个支持join()方法的队列。
# 多进程下，与之对应的是multiprocessing.JoinableQueue(),而不是multiprocessing.Queue
def worker(limit, jobs, results):

    # 守护线程，因此此处可以是无限循环
    while True:
        try:
            feed = jobs.get()  # 一直阻塞，直到获取
            ok, result = Feed.read(feed, limit)
            if not ok:
                Qtrac.report(result, True)
            elif result is not None:
                Qtrac.report("read {}".format(result[0][4:-6]))
                results.put(result)
        finally:
            jobs.task_done()


def create_threads(limit, jobs, results, concurrency):
    for _ in range(concurrency):
        thread = threading.Thread(target=worker, args=(limit, jobs,
                                                       results))
        thread.daemon = True
        thread.start()


# 如果要添加的任务很多，或者是“添加任务”这项操作本身很耗时，那么最好使用单独线程来做
def add_jobs(filename, jobs):
    for todo, feed in enumerate(Feed.iter(filename), start=1):
        jobs.put(feed)
    return todo

def process(todo, jobs, results, concurrency):
    canceled = False
    try:
        jobs.join()  # Wait for all the work to be done
    except KeyboardInterrupt:  # May not work on Windows
        Qtrac.report("canceling...")
        canceled = True
    if canceled:
        done = results.qsize()
    else:
        done, filename = output(results)
    Qtrac.report("read {}/{} feeds using {} threads{}".format(done, todo,
                                                              concurrency, " [canceled]" if canceled else ""))
    print()
    if not canceled:
        webbrowser.open(filename)



def output(results):
    done = 0
    filename = os.path.join(tempfile.gettempdir(), "whatsnew.html")
    with open(filename, "wt", encoding="utf-8") as file:
        file.write("<!doctype html>\n")
        file.write("<html><head><title>What's New</title></head>\n")
        file.write("<body><h1>What's New</h1>\n")
        while not results.empty():  # Safe because all jobs have finished
            result = results.get_nowait()
            done += 1
            for item in result:
                file.write(item)
        file.write("</body></html>\n")
    return done, filename


if __name__ == "__main__":
    main()
