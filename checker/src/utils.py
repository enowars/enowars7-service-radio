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


async def register_user_and_login(client: AsyncClient, username, password, logger):
    # Registration
    logger.info("REGISTER")
    try:
        # We expect to get a 302 and be redirected
        response = await client.post(
            "/register",
            data={"username": username, "password": password},
            follow_redirects=True,
        )

    except Exception as e:
        logger.warning("REGISTRATION FAILED, Admin can't be created!")
        handle_RequestError(e, "request error while registering")
    # Ensure registration was successful
    logger.info(
        "Registration request was sent! For user " + username + " PW: " + str(password)
    )
    assert_equals(response.status_code, 200, "registration failed")
    logger.info("Registration request got status: " + str(response.status_code))
    response = await login(client, username, password, logger)
    return response


async def login(client: AsyncClient, username, password, logger):
    # Login
    try:
        # We expect to get a 302 and be redirected
        response = await client.post(
            "/login",
            data={
                "email": username,
                "password": password,
            },
            follow_redirects=True,
        )
    except Exception as e:
        handle_RequestError(e, "request error while logging in")
    # We should get redirected else something failed
    # Ensure registration was successful
    assert_equals(response.status_code, 200, "login failed")
    logger.info("Login request got status: " + str(response.status_code))

    return response


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
