## PYTHON CACHE IMPLEMENTATION
Simple implementation of Cache system

### CACHE METHODS
``1.Get: retrieves information from redis cache``

``2.Set: set data into the redis cache``

### Get from cache
This method takes a key and return data from the redis cache
if key not found, the callback will be run to fetch data from the 
database and set data in redis cache with the duration

```cache.get(key:str, callback:Callable[..., str], duration:'timedelta'=0) -> Union[Callable[[], str], Any]``` 

### Set from cache
This method takes a key and set data in the redis cache


```cache.set(key:str, data, duration:'timedelta'=0) -> None```
