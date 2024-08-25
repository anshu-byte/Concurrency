import threading
import queue


def worker(arg1, arg2, arg3):
    thread_name = threading.current_thread().name
    print(thread_name)
    pass


arg1, arg2, arg3 = 1, 2, 3
thread1 = threading.Thread(target=worker, args=(arg1, arg2, arg3))
thread2 = threading.Thread(target=worker, args=(arg1, arg2, arg3), name="thread-2")

# Thread methods
thread1.start()
thread2.start()
thread1.join()
thread2.join()


event = threading.Event()
# Event methods

# Set the event
event.set()  # Sets the event to true
event.clear()  # Sets the event to false
event.wait()  # Waits for the event to be set
event.is_set()  # Checks if the event is set


condition = threading.Condition()

# Condition methods
condition.wait()  # Waits for the condition to be met
condition.notify()  # Wakes up a waiting thread
condition.notify_all()  # Wakes up all waiting threads

rlock = threading.RLock()

# RLock methods
rlock.acquire()  # Acquires the lock
rlock.release()  # Releases the lock

lock = threading.Lock()

# Lock methods
lock.acquire()  # Acquires the lock
lock.release()  # Releases the lock

barrier = threading.Barrier(2)

# Barrier methods
barrier.wait()  # Waits for all threads to reach the barrier

semaphore = threading.Semaphore(4)

# Semaphore methods
semaphore.acquire()
semaphore.release()


bounded_semaphore = threading.BoundedSemaphore(4)

# BoundedSemaphore methods
bounded_semaphore.acquire()
bounded_semaphore.release()


q = queue.Queue()

# Queue methods
q.put("item")  # Adds an item to the queue
q.get()  # Removes an item from the queue


# with -> context manager
with condition:
    pass

with rlock:
    pass

with lock:
    pass

with semaphore:
    pass

with bounded_semaphore:
    pass

with q:
    pass
