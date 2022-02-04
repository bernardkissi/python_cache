from redisCI.redisClient import RedisClient
from cache import Cache
import json
from datetime import timedelta

x= {"name":"bernard"}

#callback simulation data fetching from db
def save():
    data = json.dumps(x)
    with open('data.json', 'w') as f:
        f.write(data)
    return data

#
#
# #instantiating Cache class and calling the get and set
cache = Cache()
data = cache.get('testing02', save, timedelta(seconds=30) )
# results = cache.set('testing03', 'hello', timedelta(seconds=30) )
# # backup = cache.createBackup()
#
# #accessing values directly from the redis store
# redis1 = RedisClient().client.get('testing02')
# redis2 = RedisClient().client.get('testing03')
# redisStore = RedisClient().data

redis = RedisClient().client
pub = RedisClient().pub
redis.publish('data-changed1', 'poiiopip')
subscriber = RedisClient().subscriber
message = pub.get_message()
print('pub/sub')

#displaying the results of cache data
# print(data)
# print(redis1)
# print(redis2)
print('something from backup')
# print(redisStore)
print(message)