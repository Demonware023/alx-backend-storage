#!/usr/bin/env python3
"""
This module defines a Cache class with method call counting using Redis.
"""
import redis
import uuid
from typing import Union, Callable, Optional
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count in Redis
        for the given method using its qualified name.
        """
        # Use the method's __qualname__ to create a Redis key
        key = f"count:{method.__qualname__}"
        
        # Increment the count in Redis
        self._redis.incr(key)
        
        # Call the original method
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Cache class to store and retrieve data from Redis, with method call counting.
    """
    def __init__(self):
        """
        Initialize Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated key.

        Args:
            data (str, bytes, int, float): The data to store.

        Returns:
            str: The key associated with the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis and apply an optional transformation function.

        Args:
            key (str): The Redis key.
            fn (Callable, optional): A function to convert the data. Defaults to None.

        Returns:
            The converted value, or the original value if no conversion function is provided.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from Redis as a UTF-8 decoded string.

        Args:
            key (str): The Redis key.

        Returns:
            str: The decoded string value.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from Redis as an integer.

        Args:
            key (str): The Redis key.

        Returns:
            int: The integer value.
        """
        return self.get(key, int)
