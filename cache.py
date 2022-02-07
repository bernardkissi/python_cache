from typing import Union, Any, Dict
from redisCI.redisClient import RedisClient
from datetime import timedelta
from collections.abc import Iterable
import json


class Cache(RedisClient):

    def __init__(self) -> None:
        RedisClient.__init__(self)
        self.cachedb = {}

    # Implementing the read through cache aside strategy
    def get(self, key: str, callback=None, duration: int = 0) -> Any:
        if callback is None:
            callback = {}
        if self.has(key):
            data = self.client.get(key)
            return data
        if callable(callback):
            payload = callback()
            if isinstance(payload, Iterable):
                payload = json.dumps(payload)
            self.set(key, payload, duration)
            return payload

    # Implementing the write function
    def set(self, key: str, data: Any, expiry: int = 0) -> None:
        if isinstance(data, Iterable):
            data = json.dumps(data)
        self.client.set(key, data, ex=timedelta(seconds=expiry))

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
    def getAll(self) -> dict:
        keys = self.client.keys('*')
        if not keys:
            return "cache is empty"
        else:
            values = self.client.mget(*keys)
            values = map(str, values)
            self.cachedb.update(dict(zip(keys, values)))
        return self.cachedb

    #  Simulating pre-heating cache with backup data
    def preHeatCacheFromBackup(self):
        # self.flush()
        pass


