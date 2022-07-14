import queue
import sys
import threading


def producer(shared_queue: queue.Queue):
    """
    Producer of the jobs.
    :param shared_queue: The Queue
    :return:
    """
    # adding to the queue
    shared_queue.put('some value or task')
    # check Exception shared_queue.Full or just full()

    # when all done, add None to the queue
    shared_queue.put(None)


def consumer(shared_queue: queue.Queue):
    """
    A consumer of jobs.
    :param shared_queue: The Queue
    :return:
    """
    # get a work from the queue
    work_item = shared_queue.get()
    # check Exception shared.queue.Empty or empty()

    if work_item is None:
        sys.exit(1)

    shared_queue.task_done()  # but avoid put None in the producer.


if __name__ == '__main__':
    """Creating a thread safe queue, which avoids race conditions."""
    # creating a queue
    shared_queue = queue.Queue()  # maxsize=10 size of queue, block=True to use the thread safe, timeout=1

    # creating a consumer
    consumer = threading.Thread(target=consumer, args=(shared_queue,))
    # consumer.start()

    # creating a producer
    producer = threading.Thread(target=producer, args=(shared_queue,))
    # producer.start()

    # producer.join()
    # consumer.join()
