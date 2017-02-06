import redis

host = "168.168.1.91"
port = 6379
r = redis.StrictRedis(host=host, port=port, db=1)



r.set('foo','bar')
print(r.get('foo'))