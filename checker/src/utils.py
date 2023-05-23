import asyncio
from logging import LoggerAdapter
from httpx import AsyncClient, ConnectTimeout, NetworkError, PoolTimeout, Response
from json import JSONDecodeError
from enochecker3 import ChainDB, MumbleException, OfflineException
from enochecker3.utils import assert_equals, assert_in


def handle_RequestError(err, msg):
    if any(isinstance(err, T) for T in [ConnectTimeout, NetworkError, PoolTimeout]):
        raise OfflineException(
            msg + ": " + str(err) + " " + type(err).__name__ + " the service is offline"
        )

    raise MumbleException(msg + ": " + str(err) + " " + type(err).__name__)


async def register_user_and_open_main_page(client: AsyncClient, logger: LoggerAdapter):
    try:
        # We expect to get a 302 and be redirected
        response = await client.get("/login", follow_redirects=True)
    except Exception as e:
        handle_RequestError(e, "request error while registering")
    # Check if the request was redirected
    if response.is_redirect:
        return response.url
    # We should get redirected else something failed
    raise MumbleException("Redirection from login to main page failed")


def response_ok(response: Response, message: str, logger: LoggerAdapter) -> dict:
    try:
        json = response.json()
    except JSONDecodeError:
        raise MumbleException(message)

    assert_in("status", json, message + "response json contained no status code")

    if "output" in json:
        logger.info("Request returned output: " + json["output"])
    assert_equals(
        json["status"],
        "ok",
        message + " status was not ok: (was: " + json["status"] + ")",
    )

    assert_equals(response.status_code, 200, message + " status code was not 200")

    return json
