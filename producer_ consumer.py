import threading

# Shared resource
shared_resource = []

# Condition variable
condition = threading.Condition()


# Consumer thread
def consumer():
    with condition:
        while not shared_resource:
            print("Consumer is waiting...")
            condition.wait()
        item = shared_resource.pop(0)
        print("Consumer consumed item:", item)


# Producer thread
def producer():
    with condition:
        item = "New item"
        shared_resource.append(item)
        print("Producer produced item:", item)
        condition.notify()


# Create and start the threads
consumer_threads = []
producer_threads = []
n = 3
for i in range(n):
    consumer_thread = threading.Thread(target=consumer)
    producer_thread = threading.Thread(target=producer)
    producer_thread.start()
    consumer_thread.start()
    producer_threads.append(producer_thread)
    consumer_threads.append(consumer_thread)

for i in range(n):
    producer_threads[i].join()
    consumer_threads[i].join()
