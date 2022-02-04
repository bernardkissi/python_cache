import redis

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class RedisClient(metaclass=Singleton):
    def __init__(self, host:str = 'localhost', port:int = 6379, db=0, decode_responses=True):
        self.__host = host
        self.__port = port
        self.client = redis.Redis(host=self.__host, port=self.__port, db=0)
        self.data = {}
        self.pub = self.client.pubsub()
        self.pub.run_in_thread(sleep_time=0.01)
        self.subscriber = self.pub.psubscribe(**{'data-changed*': self.createBackup()})


    def createBackup(self):
        self.__getAll()
        print(self.data)
        print('888888888888')

    def __getAll(self) -> None:
        keys = self.client.keys('*')
        values = self.client.mget(*keys)
        values = map(str, values)
        self.data.update(dict(zip(keys, values)))