from typing import Union, Any
from redisCI.redisClient import RedisClient
from typing import Callable
from datetime import timedelta
from collections.abc import Iterable
import json


class Cache(RedisClient):

    def __init__(self) -> None:
        RedisClient.__init__(self)
        self.restoreFromBackup()

    # Implementing the read through cache aside strategy
    def get(self, key: str, callback: Callable[..., str], duration: 'timedelta' = 0) -> Union[Callable[[], str], Any]:
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
    def set(self, key: str, data: Any, duration: 'timedelta' = 0) -> None:
        self.client.set(key, data, ex=duration)

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
