# findrobots.py

import gzip
import io
import glob
from concurrent import futures

'''
    def work():
        return result

    # no-parallel implementation
    results = map(work,data)

    # parallel implementation
    with ProcessPoolExecutor() as pool:
        results = pool.map(work,data)

    # submit single tasks using the pool.submit()
    with ProcessPoolExecutor() as pool:
        future_result = pool.submit(work,arg)
        r = future_result.result()
'''

def find_robots(filename):
    '''
    Find all of the hosts that access robots.txt in a single log file
    '''
    robots = set()
    with gzip.open(filename) as f:
        for line in io.TextIOWrapper(f,encoding='ascii'):
            fields = line.split()
            if fields[6] == '/robots.txt':
                robots.add(fields[0])
    return robots

def find_all_robots(logdir):
    '''
    Find all hosts across and entire sequence of files
    '''
    files = glob.glob(logdir+"/*.log.gz")
    all_robots = set()
    with futures.ProcessPoolExecutor() as pool:
        for robots in pool.map(find_robots, files):
            all_robots.update(robots)
    return all_robots

if __name__ == '__main__':
    import time
    start = time.time()
    robots = find_all_robots("logs")
    end = time.time()
    for ipaddr in robots:
        print(ipaddr)
    print('Took {:f} seconds'.format(end-start))
