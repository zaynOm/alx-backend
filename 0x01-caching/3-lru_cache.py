#!/usr/bin/env python3
"""LRU Caching"""

BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """LRU caching system"""

    def __init__(self):
        """Init"""
        super().__init__()
        self.cumbersome = []

    def put(self, key, item):
        """Add new item to the cache"""
        if key is None or item is None:
            return

        if key in self.cumbersome:
            self.cumbersome.remove(key)
        self.cumbersome.append(key)

        if (
            len(self.cumbersome) > BaseCaching.MAX_ITEMS
            and key not in self.cache_data
        ):
            poped = self.cumbersome.pop(0)
            self.cache_data.pop(poped)
            print(f"DISCARD: {poped}")
        self.cache_data[key] = item

    def get(self, key):
        """Retrive an item from the cache"""
        if key in self.cache_data:
            self.cumbersome.remove(key)
            self.cumbersome.append(key)
        return self.cache_data.get(key)
