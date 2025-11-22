"""
executing a function at regular intervals
Author: AlexL
License: MIT
Github: https://github.com/Hangover3832/every
"""

from time import monotonic
from typing import Callable, Any, Optional
from functools import wraps


class Every:
    """A simple class for executing a function at regular intervals.
    The Every class provides a mechanism to control periodic execution of a function,
    allowing for flexible timing control and parameter passing.
    Args:
        interval (float): The time interval in seconds between function executions.
        execute_immediately (bool): If True, the function will be executed immediately upon the first call.
        keep_interval (bool): Keep correct time interval if set to True, else keep temporal distance after function call
    Attributes:
        interval (float): The time interval between executions (readable/writable)
        time_func (Callable): The function used to get the current time (default is monotonic)
        time_remaining(float): The remaining time until the next execution (read only)
    Methods:
        do(action: Callable) -> 'Every': Sets the function to be executed 
        among(**kwargs) -> 'Every': Sets the keyword arguments for the funtion.
        using(time_func: Callable) -> 'Every': Sets a custom time function (default is monotonic).
        Note: When calling the instance, any keyword arguments passed will override those set in among().
    Returns:
        tuple[bool, Any]: A tuple containing:
            - bool: True if function was executed, False otherwise
            - Any: Return value from do() if executed, None otherwise
    Example:
        icluded in Demo() function below
    """

    @classmethod # decorator for class Every
    def every(cls,
            interval: float, 
            *, 
            timer_function: Callable[[], float] = monotonic, 
            execute_immediately: bool = False,
            keep_interval : bool = True,
            **kwargs: Optional[Any]
            ) -> Callable[[Callable], 'Every']:
        """Decorator to create an Every instance and set the kwargs.
        Args:
            interval (float): The time interval in seconds between function executions.
            execute_immediately (bool): If True, the function will be executed immediately upon the first call.
            keep_interval (bool): Keep correct time interval if set to True, else keep temporal distance after function call
            **kwargs: Additional keyword arguments to pass to the function.
        """
        @wraps(wrapped=cls)
        def wrapper(func: Callable[[], float]) -> 'Every':
            inst = cls(
                    interval, 
                    execute_immediately=execute_immediately, 
                    keep_interval=keep_interval
                    ).do(func
                    ).among(**kwargs
                    ).using(timer_function)
            inst._is_decorator = True
            return inst

        return wrapper


    def __init__(self, interval: float, *, execute_immediately: bool = False, keep_interval: bool = True) -> None:
        if interval <= 0:
            raise ValueError("Error: Interval must be positive.")

        self._interval: float = interval
        self._keep_interval: bool = keep_interval
        self._time_func: Callable[[], float] = monotonic
        self._action: Callable | None = None
        self._kwargs = {}
        self._paused: bool = False
        self._next_time: float = self._time_func() if execute_immediately else self._time_func() + interval
        self._is_decorator: bool = False


    def do(self, action: Callable) -> 'Every':
        """Sets the function to be executed."""
        self._action = action
        return self


    def among(self, **kwargs: Any) -> 'Every':
        self._kwargs = kwargs
        return self


    def using(self, time_func: Callable) -> 'Every':
        """Sets a custom time function (default is monotonic)."""
        self._time_func = time_func
        return self


    def reset(self) -> 'Every':
        """Reset the timer to start from current moment."""
        self._next_time = self._time_func() + self._interval
        return self


    def pause(self) -> 'Every':
        """Stop execution"""
        self._paused = True
        return self


    def resume(self) -> 'Every':
        """Continue execution"""
        self._paused = False
        return self


    def __call__(self, *args, **kwargs: Any) -> tuple[bool, Optional[Any]]:
        """
        Checks if the scheduled interval has passed and executes the stored function if so.

        Args:
            **kwargs: Additional keyword arguments to pass to the stored function.

        Returns:
            tuple[bool, Any]: A tuple containing:
                - bool: True if the function was executed, False otherwise.
                - Any: The return value from the function if executed, or None otherwise.
        """        
        if self._paused:
            return False, None

        if self._action is None:
            raise ValueError("No action has been set. Use the 'do' method to set a function to execute.")
        
        if self._time_func() >= self._next_time:
            self._next_time += self._interval # adding interval to keep correct time interval
            merged_kwargs = {**self._kwargs, **kwargs}
            result = self._action(*args, **merged_kwargs) # execute the function
            if not self._keep_interval:
                # If not keeping interval, reset next time to current time plus interval
                self._next_time = self._time_func() + self._interval
            return True, result

        return False, None


    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"Every(action={self._action}, interval={self._interval}, next_time={self._next_time}, is_decorator={self.is_decorator})"

    def execute(self, *args: Optional[Any], **kwargs: Optional[Any]) -> Optional[Any]:
        """Execute the function immediately"""
        if self._action is None:
            raise ValueError("No action has been set. Use the 'do' method to set a function to execute.")
        merged_kwargs = {**self._kwargs, **kwargs}
        return self._action(*args, **merged_kwargs)

    @property
    def interval(self) -> float:
        """The time interval between executions (readable/writable)"""
        return self._interval

    @interval.setter
    def interval(self, value: float) -> None:
        """
        Sets a new interval value and resets the next execution time.

        Args:
            value (float): The new time interval in seconds.
        """
        if value <= 0:
            raise ValueError("Interval must be positive")
        self._interval = value
        self.reset()
 
    @property
    def time_remaining(self) -> float:
        """Get the time remaining until next execution."""
        return max(0.0, self._next_time - self._time_func())
        
    @property
    def next_time(self) -> float:
        """Get the next execution time."""
        return self._next_time

    @property
    def paused(self)  -> bool:
        """Check if the timer is currently paused."""
        return self._paused

    @property
    def time_func(self) -> Callable[[], float]:
        """Get the current time function."""
        return self._time_func
    
    @property
    def is_decorator(self) -> bool:
        return self._is_decorator
