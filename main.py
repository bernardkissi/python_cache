from redisClient import  RedisClient
from cache import Cache
import json
from datetime import timedelta
#
x= {"name":"bernard"}

#callback simulation data fetching from db
def save():
    data = json.dumps(x)
    with open('data.json', 'w') as f:
        f.write(data)
    return data



#instantiating Cache class and calling the get and set
cache = Cache()
data = cache.get('testing02', save, timedelta(seconds=30) )
results = cache.set('testing03', 'hello', timedelta(seconds=30) )


#accessing values directly from the redis store
redis1 = RedisClient().client.get('testing02')
redis2 = RedisClient().client.get('testing03')

#displaying the results of cache data
print(data)
print(redis1)
print(redis2)
