import redis


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisClient(metaclass=Singleton):
    def __init__(self, host: str = 'localhost', port: int = 6379, db=0, decode_responses=True):
        self.__host = host
        self.__port = port
        self.client = redis.Redis(host=self.__host, port=self.__port, db=0)
