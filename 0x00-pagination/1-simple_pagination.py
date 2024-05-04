#!/usr/bin/env python3
"Simple pagination"


import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    "Return the start and end indexes"
    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Implement simple pagination"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        data = []
        start_index, end_index = index_range(page, page_size)
        with open(self.DATA_FILE, "r") as f:
            reader = csv.reader(f)
            for _ in range(start_index + 1):
                if next(reader, None) is None:
                    return []

            for _ in range(end_index - start_index):
                data.append(next(reader))

        return data
