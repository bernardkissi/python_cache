from typing import Union, Any
from redisCI.redisClient import RedisClient
from typing import Callable
from datetime import timedelta
from collections.abc import Iterable
import json

class Cache(object):

    def __init__(self) -> None:
        self.redisCls = RedisClient()
        self.redis = self.redisCls.client
        self.restoreFromBackup()

    # Implementing the read through cache aside strategy
    def get(self, key: str, callback:Callable[..., str], duration:'timedelta'=0) -> Union[Callable[[], str], Any]:
        if self.has(key):
            data = self.redis.get(key)
            return data
        if callable(callback):
            payload = callback()
            if isinstance(payload, Iterable):
                payload = json.dumps(payload)
            self.set(key, payload, duration)
            return payload

    # Impementing the write function
    def set(self, key: str, data: Any, duration:'timedelta'=0) -> None:
        self.redis.set(key, data, ex=duration)

    # Checks if the key passed exist in redis
    def has(self, key: str) -> bool:
        return self.redis.exists(key)

    # Remove a specify key from redis
    def forget(self, *key: str) -> None:
        self.redis.delete(key)

    # flush the entire redis store
    def flush(self) -> None:
        self.redis.flushdb()

    # fetch all data in the redis cache
    # def __getAll(self) -> None:
    #     keys = self.redis.keys('*')
    #     values = self.redis.mget(*keys)
    #     values = map(str, values)
    #     self.redisCls.data.update(dict(zip(keys, values)))

    # # simulating restoration from external drive
    def restoreFromBackup(self):
        with open('data.json') as f:
            data = f.read()
            print(data)


