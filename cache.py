from typing import Union, Any, Callable
from redisClient import RedisClient
from typing import Callable
from datetime import timedelta

class Cache(object):

    def __init__(self) -> None:
        self.redisCls = RedisClient()
        self.redis = self.redisCls.client
        # self.pub = self.redisCls.pub
        # self.pub.psubscribe(**{'data-changed*':self.createBackup()})
        self.restoreFromBackup()

    """ Implementing the read through cache aside strategy"""
    def get(self, key: str, callback:Callable[..., str], duration:'timedelta'=0) -> Union[Callable[[], str], Any]:
        if self.has(key):
            data = self.redis.get(key)
            return data
        if callable(callback):
            payload = callback()
            self.set(key, payload, duration)
            return payload

    """Impementing the write function"""
    def set(self, key: str, data: Any, duration:'timedelta'=0) -> None:
        self.redis.set(key, data, ex=duration)

    """Checks if the key passed exist in redis"""
    def has(self, key: str) -> bool:
        return self.redis.exists(key)

    """Remove a specify key from redis"""
    def forget(self, *key: str) -> None:
        self.redis.delete(key)

    # flush the entire redis store
    def flush(self) -> None:
        self.redis.flushdb()

    # def restoreFromBackup(self):
    #     pass
    #
    # """create a backup if data changes: """
    # def createBackup(self, payload):
    #     print('we are creating backup')
    # #

