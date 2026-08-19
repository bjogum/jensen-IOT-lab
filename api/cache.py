import json
import os
import redis

client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)


def get_latest_from_cache(device_id):
    # TODO M2:
    # Läs senaste mätvärdet från Redis.

    redis_key = f"latest:{device_id}"
    cached_data = client.get(redis_key)

    if cached_data:
        return json.loads(cached_data)

    return None


def set_latest_in_cache(device_id, measurement):
    # TODO M2:
    # Spara senaste mätvärdet i Redis.
    redis_key = f"latest:{device_id}"

    data_string = json.dumps(measurement)
    client.set(redis_key, data_string, ex=180)

