
from typing import Any
import json

from redisCI.redisClient import RedisClient


class Publisher(RedisClient):
    def __init__(self):
        RedisClient.__init__(self)

    def writeMessage(self, message: Any = 'the message is passed'):
        self.client.publish('broadcast-updates2', json.dumps(message))
