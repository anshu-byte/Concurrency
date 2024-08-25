import threading


class UberRides:
    def __init__(self):
        self.democrats_waiting = 0
        self.republicans_waiting = 0
        self.lock = threading.Lock()
        self.democrats_semaphore = threading.Semaphore(0)
        self.republicans_semaphore = threading.Semaphore(0)

    def seatDemocrat(self):
        with self.lock:
            self.democrats_waiting += 1
            print(
                f"Democrat waiting. Democrats: {self.democrats_waiting}, Republicans: {self.republicans_waiting}"
            )
            if self.democrats_waiting == 4:
                self.democrats_semaphore.release(4)
                self.democrats_waiting -= 4
                self.drive("DDDD")
            elif self.democrats_waiting >= 2 and self.republicans_waiting >= 2:
                self.democrats_semaphore.release(2)
                self.republicans_semaphore.release(2)
                self.democrats_waiting -= 2
                self.republicans_waiting -= 2
                self.drive("DDRR")

        # Wait until the semaphore is released
        self.democrats_semaphore.acquire()

    def seatRepublican(self):
        with self.lock:
            self.republicans_waiting += 1
            print(
                f"Republican waiting. Democrats: {self.democrats_waiting}, Republicans: {self.republicans_waiting}"
            )
            if self.republicans_waiting == 4:
                self.republicans_semaphore.release(4)
                self.republicans_waiting -= 4
                self.drive("RRRR")
            elif self.republicans_waiting >= 2 and self.democrats_waiting >= 2:
                self.democrats_semaphore.release(2)
                self.republicans_semaphore.release(2)
                self.democrats_waiting -= 2
                self.republicans_waiting -= 2
                self.drive("DDRR")

        # Wait until the semaphore is released
        self.republicans_semaphore.acquire()

    def drive(self, group):
        print(f"Group seated: {group}. Ride started!")


def rider(ride, party):
    if party == "D":
        ride.seatDemocrat()
    else:
        ride.seatRepublican()


if __name__ == "__main__":
    ride = UberRides()
    threads = []
    rider_groups = ["R", "R", "R", "D", "R", "D", "D", "D"]

    for i, party in enumerate(rider_groups):
        thread = threading.Thread(target=rider, args=(ride, party), name=f"Rider-{i+1}")
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
