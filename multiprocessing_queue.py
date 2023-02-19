import multiprocessing


def producer(shared_queue: multiprocessing.Queue):
    """
    Create and put work in the shared queue.
    :param shared_queue: Queue object
    :return:
    """
    # generate work
    shared_queue.put('put some work here')

    # when finished put(None)
    # you can try using timeout.


def consumer(shared_queue: multiprocessing.Queue):
    """
    Consume the work from a shared queue.
    :param shared_queue: Queue object
    :return:
    """
    # consuming a work
    shared_queue.get()
    # check here if not None


if __name__ == '__main__':
    """Create a process safe queue."""
    shared_queue = multiprocessing.Queue()
    consumer_object = multiprocessing.Process(target=consumer, args=(shared_queue,))

    # consumer_object.start()

    producer_object = multiprocessing.Process(target=producer, args=(shared_queue,))

    # producer_object.start()

    # wait for the processes to finish
    # consumer_object.join()
    # producer_object.join()
