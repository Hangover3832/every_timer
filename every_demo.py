from every import Every
from time import sleep, perf_counter, monotonic
from random import random

def Demo():

    # simplest usage:
    @Every.every(5.0, keep_interval=False)
    def VerySimple() -> None:
        sleep(2)
        print(f"A very simple but expensive function has been executed.")
        # since this function takes 2 seconds to execute and keep_interval is False,
        # the effective interval is about 7 seconds

    VerySimple.interval = 4.9 # override interval at runtime
    print(VerySimple) # testing __repr__()

    # decorator usage:
    @Every.every(2.71, param2=10, param3=20, timer_function=monotonic, execute_immediately=True) # static param1 and param2, execute on first call
    def MyFunction1(param1, param2, param3) -> int: # param1 is required dynamically when calling the function
        print(f"Function1 executed with {param1=}, {param2=} and {param3=}")
        MyFunction1.interval = 3 * random() # Change interval at runtime
        return param1 + 1
    print(MyFunction1)

    # direct usage:
    def MyFunction2(a, b):
        print(f"MyFunction2 executed with {a=} and {b=}")
        return a * b
    my_function2_timer = Every(3.14).do(MyFunction2).among(a=5, b=6).using(perf_counter) # static parameter a and b & use different timer function
    print(my_function2_timer)

    VerySimple.reset().execute() # reset the timer and execute immediately
    
    counter = 0

    @Every.While(30) # repeat for 30s
    def timed_while():
        nonlocal counter

        VerySimple()

        executed, res = MyFunction1(param1=counter) # Add param1 dynamically
        if executed:
            print(f"Function1 returned: {res}, function2 time remaining: {my_function2_timer.time_remaining:.2f}s")
            counter += 1

        executed, res = my_function2_timer(b=2) # Override b dynamically
        if executed:
            print(f"Function2 returned: {res}, function1 time remaining: {MyFunction1.time_remaining:.2f}s")

        sleep(0.01)


if __name__ == "__main__":
    Demo() # This will run the demo code
