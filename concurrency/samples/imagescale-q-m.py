#!/usr/bin/env python3

# 用队列及多进程实现并发
# 适合io密集型

import argparse
import collections
import math
import multiprocessing
import os
import sys
import Qtrac
import Image

# python imagescale-m.py -S D:/worksapce/python/python-practice/sample/picture  D:/worksapce/python/python-practice/sample/new_picture

# 保存待执行的任务（待缩小的图像）
Result = collections.namedtuple("Result", "copied scaled name")
# 收集任务的执行结果
Summary = collections.namedtuple("Summary", "todo copied scaled canceled")


def main():
    sys.path.append("D:/worksapce/python/python-practice/concurrency")
    # 缩小后图像尺寸，是否采用平滑缩放，缩小前/后图片所在的目录，cpu核心数
    size, smooth, source, target, concurrency = handle_commandline()
    Qtrac.report("starting...")
    summary = scale(size, smooth, source, target, concurrency)
    summarize(summary, concurrency)


def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--concurrency", type=int,
            default=multiprocessing.cpu_count(),
            help="specify the concurrency (for debugging and "
                "timing) [default: %(default)d]")
    parser.add_argument("-s", "--size", default=400, type=int,
            help="make a scaled image that fits the given dimension "
                "[default: %(default)d]")
    parser.add_argument("-S", "--smooth", action="store_true",
            help="use smooth scaling (slow but good for text)")
    parser.add_argument("source",
            help="the directory containing the original .xpm images")
    parser.add_argument("target",
            help="the directory for the scaled .xpm images")
    args = parser.parse_args()
    source = os.path.abspath(args.source)
    target = os.path.abspath(args.target)
    if source == target:
        args.error("source and target must be different")
    if not os.path.exists(args.target):
        os.makedirs(target)
    return args.size, args.smooth, source, target, args.concurrency

# 基于队列的多进程技术，是一个相当通用的“并发任务执行”函数
# 它把待执行的任务分派给各个进程，并收集执行结果。
def scale(size, smooth, source, target, concurrency):
    canceled = False
    jobs = multiprocessing.JoinableQueue()  # 创建支持join方法的队列
    results = multiprocessing.Queue()   # 创建no joinable
    create_processes(size, smooth, jobs, results, concurrency)  # 创建缩小操作所需的进程，创建完成后出于阻塞状态
    todo = add_jobs(source, target, jobs)   # 添加到工作队列
    try:
        jobs.join() # 调用join方法，等待工作队列变空
    except KeyboardInterrupt: # May not work on Windows
        Qtrac.report("canceling...")
        canceled = True
    copied = scaled = 0
    while not results.empty(): # Safe because all jobs have finished
        result = results.get_nowait()
        copied += result.copied
        scaled += result.scaled
    return Summary(todo, copied, scaled, canceled)

# 创建多个进程，每个进程都传入了同一个worker()函数和任务的细节，细节信息中包含2个共享队列，用于存放任务和结果
# 无需加锁，队列会自行处理好同步问题
def create_processes(size, smooth, jobs, results, concurrency):
    for _ in range(concurrency):
        process = multiprocessing.Process(target=worker, args=(size,
                smooth, jobs, results))
        process.daemon = True   # 设置该进程为守护进程，主进程终止后，守护进程也会照常终止
        # 每创建完一个进程，调用start方法，促使其开始执行worker函数，这些进程比如会阻塞，因为任务队列里还没有任务
        # 虽然它们阻塞了，但是主进程和这些进程是各自独立的，所以主进程不会阻塞。主进程会很快把这些进程创建完毕，
        # 并从create_processes中返回。然后调用本函数的那段代码会把待处理的任务添加到队列中，刚才阻塞的进程就可以领取
        # 任务，继续执行
        process.start()

# 将任务封装这函数里，然后函数经target参数传给multiprocessing.Process对象
def worker(size, smooth, jobs, results):
    # 没轮循环都尝试从共享的工作队列里领取一项任务，此处使用无限循环不会有问题，因为执行worker的进程都是守护进程，
    # 主进程终止时，它们也会随之终止
    while True:
        try:
            # 如果队列中没有任务，get方法将会一直阻塞
            sourceImage, targetImage = jobs.get()
            try:
                result = scale_one(size, smooth, sourceImage, targetImage)
                Qtrac.report("{} {}".format("copied" if result.copied else
                        "scaled", os.path.basename(result.name)))
                results.put(result)
            except Image.Error as err:
                Qtrac.report(str(err), True)
        finally:
            jobs.task_done()


def add_jobs(source, target, jobs):
    for todo, name in enumerate(os.listdir(source), start=1):
        sourceImage = os.path.join(source, name)
        targetImage = os.path.join(target, name)
        jobs.put((sourceImage, targetImage))
    return todo


def scale_one(size, smooth, sourceImage, targetImage):

    oldImage = Image.from_file(sourceImage)
    if oldImage.width <= size and oldImage.height <= size:
        oldImage.save(targetImage)
        return Result(1, 0, targetImage)
    else:
        if smooth:
            scale = min(size / oldImage.width, size / oldImage.height)
            newImage = oldImage.scale(scale)
        else:
            stride = int(math.ceil(max(oldImage.width / size,
                                       oldImage.height / size)))
            newImage = oldImage.subsample(stride)
        newImage.save(targetImage)
        return Result(0, 1, targetImage)


def summarize(summary, concurrency):
    message = "copied {} scaled {} ".format(summary.copied, summary.scaled)
    difference = summary.todo - (summary.copied + summary.scaled)
    if difference:
        message += "skipped {} ".format(difference)
    message += "using {} processes".format(concurrency)
    if summary.canceled:
        message += " [canceled]"
    Qtrac.report(message)
    print()


if __name__ == "__main__":
    main()
