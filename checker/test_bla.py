import asyncio
from logging import LoggerAdapter
from httpx import AsyncClient, ConnectTimeout, NetworkError, PoolTimeout, Response
from json import JSONDecodeError
from enochecker3 import ChainDB, MumbleException, OfflineException
from enochecker3.utils import assert_equals, assert_in


async def main():
    async with AsyncClient() as client:
        response = await client.get(
            "http://localhost:5000/dd7ff8d6-8b2c-432c-965d-f2ba2a82bfb9"
        )
        print(response)


asyncio.run(main())
