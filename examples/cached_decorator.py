import asyncio

from collections import namedtuple
import redis.asyncio as redis

from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer

Result = namedtuple('Result', "content, status")


@cached(
    ttl=10, cache=Cache.REDIS, key_builder=lambda *args, **kw: "key",
    serializer=PickleSerializer(), namespace="main", client=redis.Redis())
async def cached_call():
    return Result("content", 200)


async def test_cached():
    async with Cache(Cache.REDIS, namespace="main", client=redis.Redis()) as cache:
        await cached_call()
        exists = await cache.exists("key")
        assert exists is True
        await cache.delete("key")


if __name__ == "__main__":
    asyncio.run(test_cached())
