import threading
import time
import random

# Shared variables
waiting_room_capacity = 5
waiting_customers = 0

# Synchronization primitives
waiting_room = threading.Semaphore(
    waiting_room_capacity
)  # Semaphore for waiting chairs

customer_ready = threading.Condition()  # Condition variable for customer signaling
barber_sleeping = threading.Event()  # Event for barber's sleep status


def barber():
    global waiting_customers

    while True:
        with customer_ready:
            while waiting_customers == 0:
                print("Barber is sleeping...")
                barber_sleeping.set()  # Notify customers the barber is sleeping
                customer_ready.wait()  # Wait for a customer to arrive
                barber_sleeping.clear()  # Customer has woken the barber

            # A customer is ready
            waiting_customers -= 1
            print("Barber is cutting hair.")
            # Simulate hair cutting
            time.sleep(1)
            print("Barber finished cutting hair.")
            # Notify waiting customers that a chair has become free
            waiting_room.release()
            customer_ready.notify()  # Wake up another customer if needed


def customer(customer_id):
    global waiting_customers

    print(f"Customer {customer_id} is entering the shop.")
    if not waiting_room.acquire(blocking=False):
        print(f"Customer {customer_id} leaves as there are no free chairs.")
        return

    with customer_ready:
        waiting_customers += 1
        print(f"Customer {customer_id} is waiting.")
        # Signal the barber if they are sleeping
        if barber_sleeping.is_set():
            barber_sleeping.clear()
            customer_ready.notify()  # Wake up the barber if asleep

    # Wait until the barber finishes the haircut
    with waiting_room:
        print(f"Customer {customer_id} is getting a haircut.")
        # Simulate waiting for a haircut
        time.sleep(1)
        print(f"Customer {customer_id} is leaving after the haircut.")


if __name__ == "__main__":
    barber_thread = threading.Thread(target=barber)
    barber_thread.start()

    customer_threads = []
    for i in range(1, 11):
        t = threading.Thread(target=customer, args=(i,))
        customer_threads.append(t)
        t.start()
        time.sleep(random.uniform(0.5, 1.5))

    for t in customer_threads:
        t.join()

    barber_thread.join()
