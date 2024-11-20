from cachetools import LRUCache

prolog_process_cache = LRUCache(maxsize=10)
