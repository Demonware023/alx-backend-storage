#!/usr/bin/env python3
"""
This module defines a Cache class for interacting with Redis.
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """
    Cache class to store and retrieve data from Redis.
    """
    def __init__(self):
        """
        Initialize Redis client and flush database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
