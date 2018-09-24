from threading import Thread, Barrier

BARRIER = Barrier(5)

class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(sensor_index, how_many, counter):
    BARRIER.wait()
    for _ in range(how_many):
        counter.increment(1)


def run_threads(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


how_many = 10**5
counter = Counter()
run_threads(worker, how_many, counter)
print('Counter should be %d, found %d' % (5 * how_many, counter.count))


from threading import Lock

class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count  = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


BARRIER = Barrier(5)
counter = LockingCounter()
run_threads(worker, how_many, counter)
print('Counter should be %d, found %d' % (5 * how_many, counter.count))