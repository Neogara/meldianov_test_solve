import redis

redis_server = None


def get_redis():
    global redis_server
    if not redis_server:
        run_redis_server()
    return redis_server


def run_redis_server():
    global redis_server
    print("Run Redis server")
    redis_server = redis.Redis(host="redis", port=6379, db=0)
    print(f"Redis server: {redis_server}")
