#!/usr/bin/env python3

# 用Future及多进程实现并发
# 适合cpu密集型
# python imagescale-m.py -S D:/worksapce/python/python-practice/sample/picture  D:/worksapce/python/python-practice/sample/new_picture


import sys
if sys.version_info < (3, 2):
    print("requires Python 3.2+ for concurrent.futures")
    sys.exit(1)
import argparse
import collections
import concurrent.futures
import math
import multiprocessing
import os
import Qtrac
import Image


Result = collections.namedtuple("Result", "copied scaled name")
Summary = collections.namedtuple("Summary", "todo copied scaled canceled")


def main():
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


def scale(size, smooth, source, target, concurrency):
    futures = set()
    with concurrent.futures.ProcessPoolExecutor(max_workers=concurrency) as executor:
        for sourceImage, targetImage in get_jobs(source, target):
            future = executor.submit(scale_one, size, smooth, sourceImage,targetImage)
            futures.add(future)
        summary = wait_for(futures) # 会阻塞，直到所有future都执行完毕
        if summary.canceled:
            executor.shutdown()
        return summary
# if we caught the KeyboardInterrupt in this function we'd lose the
# accumulated todo, copied, scaled counts.

# 生成器函数
def get_jobs(source, target):
    for name in os.listdir(source):
        yield os.path.join(source, name), os.path.join(target, name)


def wait_for(futures):
    canceled = False
    copied = scaled = 0
    try:
        # 会阻塞，知道所有future都执行完毕，此时该函数会把这个future返回给调用者
        for future in concurrent.futures.as_completed(futures):
            err = future.exception()
            if err is None:
                result = future.result()
                copied += result.copied
                scaled += result.scaled
                Qtrac.report("{} {}".format("copied" if result.copied else
                        "scaled", os.path.basename(result.name)))
            elif isinstance(err, Image.Error):
                Qtrac.report(str(err), True)
            else:
                raise err # Unanticipated
    except KeyboardInterrupt:
        Qtrac.report("canceling...")
        canceled = True
        for future in futures:
            future.cancel()
    return Summary(len(futures), copied, scaled, canceled)


def scale_one(size, smooth, sourceImage, targetImage):
    # Image.from_file会报错，因为Image是模块名
    oldImage = Image.Image.from_file(sourceImage)
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
