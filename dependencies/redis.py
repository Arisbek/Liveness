import redis
# from config import redis_port, redis_server
import os 

redis_server = os.environ.get("redis_server")
redis_port = os.environ.get("redis_port")

Redis_url = f"redis://{redis_server}:{redis_port}"

def Get_redis():
    return redis.Redis(host=redis_server, port=redis_port, decode_responses=True)
