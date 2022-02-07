from redisCI.redisClient import RedisClient

class Subscriber(RedisClient):
    def __init__(self):
        RedisClient.__init__(self)
        self.pubsub = self.client.pubsub()
        self.pubsub.run_in_thread(sleep_time=0.01)
        self.pubsub.psubscribe(**{'broadcast': self.createBackup()})

    def getMessage(self) -> object:
        return self.pubsub.get_message()