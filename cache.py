from typing import Any, Union
from redisCI.redisClient import RedisClient
from datetime import timedelta
import json


class Cache(RedisClient):

    def __init__(self) -> None:
        RedisClient.__init__(self)
        self.cachedb = {}

    # Implementing the read through cache aside strategy
    def get(self, key: str, callback=None, duration: int = 0) -> Any:
        if self.has(key):
            data = self.client.get(key)
            return data
        if callable(callback):
            payload = callback()
            self.set(key, self.__encode(payload), duration)
            return payload

    # Implementing the write function
    def set(self, key: str, data: Any, expiry: int = 0):
        if data is not None:
            self.client.set(key, self.__encode(data), ex=timedelta(seconds=expiry))

    # Checks if the key passed exist in redis
    def has(self, key: str) -> bool:
        return self.client.exists(key)

    # Remove a specify key from redis
    def forget(self, *key: str) -> None:
        self.client.delete(key)

    # flush the entire redis store
    def flush(self) -> None:
        self.client.flushdb()

    # fetch all data in the redis cache
    def getAll(self) -> Union['dict', str]:
        keys = self.client.keys('*')
        if not keys:
            return "cache is empty"
        else:
            values = self.client.mget(*keys)
            values = map(str, values)
            self.cachedb.update(dict(zip(keys, values)))
        return self.cachedb

    @staticmethod
    def __encode(payload):
        if isinstance(payload, (dict, list, tuple, set)):
            return json.dumps(payload)
        elif isinstance(payload, bytes):
            return str(payload, encoding='utf-8')
        return payload
