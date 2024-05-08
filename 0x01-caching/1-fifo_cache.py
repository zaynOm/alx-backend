#!/usr/bin/env python3
"""FIFO caching"""

BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """FIFO caching system"""

    def put(self, key, item):
        """Add new item to the cache"""
        if key is None or item is None:
            return

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            k = next(iter(self.cache_data))
            self.cache_data.pop(k)
            print(f"DISCARD: {k}")

    def get(self, key):
        """Retrive an item from the cache"""
        return self.cache_data.get(key, None)
