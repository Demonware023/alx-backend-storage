#!/usr/bin/env python3
"""
This module defines a Cache class for interacting with Redis.
"""
import redis
import uuid
from typing import Union

class Cache:
    """
    Cache class to store data in Redis.
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
