import os
import redis

conn = redis.Redis(host='0.0.0.0', db=0)
print(conn.keys())
