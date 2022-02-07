import json
from cache import Cache
from redisCI.publisher import Publisher
from redisCI.subscriber import Subscriber

##############################################
# CACHE FUNCTIONS (SET & GET DATA INTO CACHE)

cache: Cache = Cache()

# ADDING DATA TO CACHE
cache.set('Product:2', {"name": "sneakers", "price": 200}, 30)
#
cacheData = cache.getAll()
print(cacheData)

# RETRIEVING FROM CACHE
# scenario 1:  when cache key exist
product1 = cache.get('Product:2')
print("Product fetched from cache", product1)

# scenario 2: when cache key does not exist we make a call to db
# to fetch and store to cache
def fetchFromDB():
    with open('database.json') as db:
        data = db.read()
        results = json.loads(data)
        return results

# # callback is passed to the get method and the duration is set when callback data is set in cache
user1 = cache.get('User:1', fetchFromDB, 30)
print("User fetched from cache", user1)

###############################################
# CACHE BACKUP AND PREHEAT CACHE
# scenario : Assuming product1 changes locally based on product update
# 1. We update the cache 2
# 2. based on the ttl set we backup data
# cache.preHeatCacheFromBackup()
    # 2a. fetch all the data and we push into a json file as cache backup
    # 3a. we fetch everything from the backup and flush cache and set with db from backup

##############################################
# PUB/SUB TO UPDATE CACHE ON CHANGES AND MANAGE BACKUPS
# updates can be new resource added or item updated
subscriber = Subscriber()
publisher = Publisher()

publisher.writeMessage({'name': 'ice-cream', 'price': 400})
payload = subscriber.getMessage()
print('payload published data',payload)
# scenario new item added to the local database
if payload is not None:
    cache.set('Product:3', payload['data'], 60)
print(cache.get('Product:3'))

# scenario 1:  when cache key exist
product2 = cache.get('Product:3')
print("Product fetched from cache restored", product2)