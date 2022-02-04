import redis

class RedisClient:
    def __init__(self, host:str = 'localhost', port:int = 6379, db:int = 0):
        self.host = host
        self.port = port
        self.client = redis.Redis(host=self.host, port=self.port, db=0)