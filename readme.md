# Every

A lightweight Python utility class for executing functions at regular intervals with precise timing control.

## Overview

The `Every` class provides a simple and efficient way to execute functions periodically without the complexity of threading or event loops. It's particularly useful for scenarios where you need to perform actions at regular intervals, such as:

- Sensor reading
- Status updates
- Periodic data logging
- Timed events in games or simulations

## Features

- Simple and intuitive API
- Precise timing control using monotonic time
- Flexible parameter passing
- No external dependencies
- Customizable time function
- Thread-safe execution
- Easy timed while loop execution
- Optional decorator usage

## Installation

Simply copy the `every.py` file into your project directory.

## Usage

### Basic Example

```python
from every import Every

def print_hello():
    print("Hello")

# Create an Every instance that runs every 1 second
every_sec = Every(1.0).do(print_hello)

# In your main loop:
executed, result = every_sec()  # Will execute if 1 second has passed
```

### With Parameters

```python
def greet(name):
    print(f"Hello, {name}!")

# Create with default parameters
greeter = Every(2.0).do(greet).among(name="World")

# Override parameters on call
greeter(name="Alice")  # Will use "Alice" instead of "World"
```

### Custom Timing Function

```python
from time import time

# Use regular time() instead of monotonic()
custom_timer = Every(1.0).do(print_hello).using(time)

# Can also combine with parameters
custom_timer = Every(1.0).do(greet).among(name="World").using(time)
```

### Use as a decorator
```python
@Every.every(5.0, greets="Holla", timer_function=monotonic)
def greet(greets, name):
    print(f"{greets}, {name}!")

...
greet.reset().execute(name="Bob"): # reset the timer and execute the function immediately
...

while True:
    greet(name="Alex") # the parameter 'greets' got past in the decorator
    ...
```

### Timed While Loop
```python
counter: int = 0

@Every.While(5) # Execute function in a loop for 5s
def print_something(greet:str, name:str):
    nonlocal counter
    print(f"[{counter}] Hello, {name})
    counter += 1
    sleep(0.1)

# or, execute ones:
Every(5).do(print_something).do_while(greet="Hello", name="Alex")

# or, execute multiple times:
timed_print = Every(5).do(print_something).among(greet="Holla").using(time)
timed_print.do_while(name="Alex")
timed_print.do_while(name="Alice")
```

## API Reference

### Class: Every

#### Constructor

```python
Every(interval: float, execute_immediately: bool = False, keep_interval: bool = True)
```
- `interval`: Time between executions in seconds
- `execute_immediately`: Executes the function immediately upon the first call
- `keep_interval (bool)`: Keep correct time interval if set to True, else keep time distance after function call

#### Methods

- `do(action: Callable) -> Every`: Set the function to execute
  - Returns: The Every instance for method chaining

- `among(**kwargs)`: Set the function's static keyword arguments
  - Returns: The Every instance for method chaining

- `using(time_func: Callable) -> Every`: Optional - Set the time function (defaults to `monotonic`)
  - Returns: The Every instance for method chaining

- `do_while(*args, **kwargs) -> Any | None`: Runs the function in a loop until the specified time expires.
  - Returns: The function's result after the last call.

- `__call__(*args, **kwargs) -> bool`: Check if it's time to execute and run the function
  - Returns: Whether the function was executed. Use the `result` property to get the result of the function call.

- `reset()`: Resets the timer to start from current moment. 
  - Returns: The Every instance for method chaining, e.g. `.reset().execute()`

- `pause()`: Stop timed execution
  - Returns: The Every instance for method chaining

- `resume()`: Continue timed execution. This method can be chained
  - Returns: The Every instance for method chaining, e.g. `.resume().reset()` 

- `execute(*args, **kwargs)`: Execute the function immediately
  - Returns: The function's result

#### Properties

- `interval`: Get/set the time interval between executions
- `time_remaining`: Get the remaining time until the next execution (read only)
- `next_time`: Get the next execution time.
- `time_func`: Get the function for retrieving current time (read only)
- `is_decorator`: Check if this instance was created as a decorator or not (read only)
- `paused`: Check if the execution is paued (read only)
- `kwargs`: Get the stored keyword arguments (read only)
- `result`: Get the result of the last action call (read only)

## Notes

- The class uses `time.monotonic()` by default for precise and reliable timing
- Changing the interval resets the next execution time
- The class maintains consistent intervals by adding the interval to the last scheduled time, or optional add the interval after execution
- Additional keyword arguments can be passed both during initialization and execution


## License

This project is open source and available under the MIT License.