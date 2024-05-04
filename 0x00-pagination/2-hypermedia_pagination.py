#!/usr/bin/env python3
"Simple pagination"


import csv
import math
from typing import Dict, List, Optional, Tuple, TypedDict


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

        start_index, end_index = index_range(page, page_size)
        return self.dataset()[start_index:end_index]

    HyperDataType = TypedDict(
        "HyperDataType",
        {
            "page_size": int,
            "page": int,
            "data": List[List],
            "next_page": Optional[int],
            "prev_page": Optional[int],
            "total_pages": int,
        },
    )

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Hypermedia pagination"""

        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages,
        }
