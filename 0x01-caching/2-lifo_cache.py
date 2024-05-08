#!/usr/bin/env python3
"""LIFO Caching"""

BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache(BaseCaching):
    """LIFO caching system"""

    def put(self, key, item):
        """Add new item to the cache"""
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            poped = self.cache_data.popitem()
            print(f"DISCARD: {poped[0]}")
        self.cache_data[key] = item

    def get(self, key):
        """Retrive item from the cache"""
        return self.cache_data.get(key)
