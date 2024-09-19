#!/usr/bin/env python3
"""
This module defines a get_page function to fetch and cache HTML content of URLs
using Redis.
"""
import redis
import requests
from typing import Callable
import functools

# Create Redis client instance
r = redis.Redis()

def cache_page(method: Callable) -> Callable:
    """
    Decorator to cache the result of a URL fetch in Redis and track how many
    times the URL is accessed.
    
    Args:
        method (Callable): The function to be decorated.
    
    Returns:
        Callable: The wrapped function.
    """
    @functools.wraps(method)
    def wrapper(url: str) -> str:
        # Redis keys for counting and caching
        cache_key = f"cached:{url}"
        count_key = f"count:{url}"

        # Increment the access count in Redis
        r.incr(count_key)

        # Try to get the cached content from Redis
        cached_content = r.get(cache_key)
        if cached_content:
            print(f"Cache hit for {url}")
            return cached_content.decode('utf-8')

        # If no cache, fetch the content and cache it
        print(f"Cache miss for {url}. Fetching content...")
        content = method(url)

        # Cache the content with a 10-second expiration time
        r.setex(cache_key, 10, content)
        return content

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL using the requests module and returns it.
    
    Args:
        url (str): The URL to fetch the content from.
    
    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url)
    return response.text
