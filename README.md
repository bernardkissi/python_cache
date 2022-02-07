## PYTHON CACHE IMPLEMENTATION
Simple implementation of Cache system

### CACHE METHODS
``1.Get: retrieves information from redis cache``

``2.Set: set data into the redis cache``

### CACHE FUNCTIONS (SET & GET DATA INTO CACHE)

To use the cache class  
```
from cache import Cache

cache: Cache = Cache()
```

### ADDING DATA TO CACHE
To add data to the cache use the ```set``` method on the cache instance.
#### Method Signature
``` cache.set('key', data, expiryTime)```
#### Example 1
```
cache.set('Product:2', {"name": "sneakers", "price": 200}, 30)
```
### GETTING DATA FROM CACHE
To get data from the cache use the ```get``` method on the cache instance.
#### Method Signature
``` cache.get('key', callback, expiryTime)```
#### scenario 1:  when cache key exist
```
product1 = cache.get('Product:2')
print("Product fetched from cache", product1)
```

#### scenario 2: when cache key does not exist we make a call to DB/API
```
def fetchFromDB():
    with open('database.json') as db:
        data = db.read()
        results = json.loads(data)
        return results
```
callback is passed to the ```get``` method and the ```duration``` is set when callback data is set in cache
```
user1 = cache.get('User:1', fetchFromDB, 30)
print("User fetched from cache", user1)
```

## BACKUP AND RESTORE
I used pub/sub of redis to listen for any changes in data and react accordingly

```
subscriber = Subscriber()
publisher = Publisher()

publisher.writeMessage({'name': "something new"})
payload = subscriber.getMessage()
print(payload)
```
this prints new data we publish to the console and the subscriber listen to this channel and 
create a backup for the current cache data
