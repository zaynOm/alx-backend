#!/usr/bin/env python3
"""MRU Caching"""

BaseCaching = __import__("base_caching").BaseCaching


class MRUCache(BaseCaching):
    """MRU caching system"""

    def __init__(self) -> None:
        """Init"""
        super().__init__()
        self.mru = ""

    def put(self, key, item):
        """Add new item to the cache"""
        if not key or not item:
            return

        if (
            len(self.cache_data) >= BaseCaching.MAX_ITEMS
            and key not in self.cache_data
        ):
            self.cache_data.pop(self.mru)
            print(f"DISCARD: {self.mru}")
        self.mru = key
        self.cache_data[key] = item

    def get(self, key):
        """Retrive an item from cache"""
        self.mru = key
        return self.cache_data.get(key)
