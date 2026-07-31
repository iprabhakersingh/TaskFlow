from app.core.redis_client import redis_client

redis_client.set("test", "NatHabit")
print(redis_client.get("test"))