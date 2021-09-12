

class CacheHandler:
    def __init__(self):
        self.cache = {}

    def set_cache(self, key, value):
        self.cache[key] = value

    def get_cache(self, key):
        return self.cache.get(key, None)