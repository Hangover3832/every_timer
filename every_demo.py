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

    @Every.While(10, param="Timed while loop decorator usage") # repeat for 10s
    def execute_demo(param:str):
        nonlocal counter

        VerySimple()

        if MyFunction1(param1=counter): # Add param1 dynamically
            print(f"Function1 returned: {MyFunction1.result}, function2 time remaining: {my_function2_timer.time_remaining:.2f}s")
            counter += 1
            print(f"{MyFunction1.kwargs=}")

        if my_function2_timer(b=2): # Override b dynamically
            print(f"Function2 returned: {my_function2_timer.result}, function1 time remaining: {MyFunction1.time_remaining:.2f}s")
            print(f"{my_function2_timer.kwargs=}")

        sleep(0.01)
        return param

    print(f"Loop exited with: '{execute_demo.result}'")

    # or:
    # Every(10).do(execute_demo).do_while(param="Not decorated")

    # or:
    # timed_while = Every(10).do(execute_demo).among(param="Not decorated")
    # timed_while.do_while()
    # ...
    # result = timed_while.do_while().result


if __name__ == "__main__":
    Demo() # This will run the demo code
