import threading


class ReadWriteLock:
    def __init__(self):
        self.readers = 0
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()

    def acquire_read_lock(self):
        # Acquire the read lock by incrementing the reader count
        with self.read_lock:
            self.readers += 1
            if self.readers == 1:
                # If this is the first reader, lock the write_lock
                self.write_lock.acquire()

    def release_read_lock(self):
        # Release the read lock by decrementing the reader count
        with self.read_lock:
            self.readers -= 1
            if self.readers == 0:
                # If there are no more readers, release the write_lock
                self.write_lock.release()

    def acquire_write_lock(self):
        # Acquire the write lock directly
        self.write_lock.acquire()

    def release_write_lock(self):
        # Release the write lock
        self.write_lock.release()


rw_lock = ReadWriteLock()


def reader():
    print(f"{threading.current_thread().name} attempting to read")
    rw_lock.acquire_read_lock()
    print(f"{threading.current_thread().name} reading")
    # Simulate reading operation
    threading.Event().wait(1)
    rw_lock.release_read_lock()
    print(f"{threading.current_thread().name} finished reading")


def writer():
    print(f"{threading.current_thread().name} attempting to write")
    rw_lock.acquire_write_lock()
    print(f"{threading.current_thread().name} writing")
    # Simulate writing operation
    threading.Event().wait(2)
    rw_lock.release_write_lock()
    print(f"{threading.current_thread().name} finished writing")


# Creating threads
readers = [threading.Thread(target=reader, name=f"Reader-{i}") for i in range(3)]
writer_thread = threading.Thread(target=writer, name="Writer")

# Start threads
for r in readers:
    r.start()
writer_thread.start()

# Join threads
for r in readers:
    r.join()
writer_thread.join()
