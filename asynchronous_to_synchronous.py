import threading
import time


# Assume AsyncExecutor is a given class and we cannot modify it
class AsyncExecutor:
    def execute(self, task, callback):
        # Simulate asynchronous work with sleep
        threading.Thread(target=self._run, args=(task, callback)).start()

    def _run(self, task, callback):
        task()
        callback()


# Our new class SynchronousExecutor extends AsyncExecutor
class SynchronousExecutor(AsyncExecutor):
    def execute(self, task, callback):
        condition = threading.Condition()

        def wrapper_callback():
            with condition:
                callback()
                condition.notify()  # Notify the waiting thread that the task is done

        with condition:
            super().execute(task, wrapper_callback)
            condition.wait()  # Wait until the asynchronous execution is done


def example_task():
    print("Task started.")
    time.sleep(2)  # Simulating a time-consuming task
    print("Task completed.")


def example_callback():
    print("Callback invoked after task completion.")


executor = SynchronousExecutor()
executor.execute(example_task, example_callback)
print("Main thread continues after the task is completed.")

# Idea is based on ki task ko thread me le ja ke sleep kro and tab tak main thread ko wait krne do
