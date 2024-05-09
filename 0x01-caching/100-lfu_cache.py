#!/usr/bin/env python3
"""LFU Caching"""


BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """LFU caching system"""

    def __init__(self) -> None:
        super().__init__()
        self.cumbersome = {}

    def put(self, key, item):
        """Add new item to the cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.cumbersome[key] += 1
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                min_freq = min(self.cumbersome.values())
                least_freq_keys = [
                    k for k, v in self.cumbersome.items() if v == min_freq
                ]
                lfu_key = min(least_freq_keys, key=self.cumbersome.get)
                self.cache_data.pop(lfu_key)
                self.cumbersome.pop(lfu_key)
                print("DISCARD:", lfu_key)

            self.cache_data[key] = item
            self.cumbersome[key] = 1

        # if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
        #     frequency = sorted(
        #         self.cumbersome.items(), key=lambda item: item[1]
        #     )
        #     lfu = frequency[0]
        #     if lfu[1] == frequency[1][1]:
        #         to_remove = next(
        #             k for k, v in self.cumbersome.items() if v == lfu[1]
        #         )
        #         self.cumbersome.pop(to_remove)
        #         self.cache_data.pop(to_remove)
        #         print(f"DISCARD: {to_remove}")
        #     else:
        #         self.cumbersome.pop(lfu[0])
        #         self.cache_data.pop(lfu[0])
        #         print(f"DISCARD: {lfu[0]}")
        # self.cumbersome[key] = self.cumbersome.get(key, 0) + 1
        # self.cumbersome.move_to_end(key)
        # self.cache_data[key] = item

    def get(self, key):
        """Retrive an item from cache"""
        if key in self.cache_data:
            self.cumbersome[key] += 1
            # self.cumbersome.move_to_end(key)
        return self.cache_data.get(key)
