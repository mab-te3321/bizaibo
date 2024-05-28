import redis

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0)

# Test the connection
client.set('test', 'Hello Redis!')
value = client.get('test')
print(value.decode('utf-8'))
