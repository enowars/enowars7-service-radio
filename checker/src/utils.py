import asyncio
from logging import LoggerAdapter
from httpx import AsyncClient, ConnectTimeout, NetworkError, PoolTimeout, Response
from json import JSONDecodeError
from enochecker3 import ChainDB, MumbleException, OfflineException
from enochecker3.utils import assert_equals, assert_in
import base64


def decode_from_base64(encoded_string, logger):
    try:
        # Convert base64 string to bytes
        decoded_bytes = base64.b64decode(encoded_string)

        # Convert bytes to string
        decoded_string = decoded_bytes.decode()

        return decoded_string
    except:
        logger.warning("Decoding flag failed " + encoded_string)
        raise MumbleException("Encoding error")


def encode_to_base64(input_string, logger):
    # Convert string to bytes
    try:
        input_bytes = input_string.encode()

        # Encode bytes to base64
        encoded_bytes = base64.b64encode(input_bytes)

        # Convert base64 bytes to string
        encoded_string = encoded_bytes.decode()

        return encoded_string
    except:
        logger.warning("Encoding flag failed " + input_string)
        raise MumbleException("Encoding error")


# Find flag
def find_string_between_flags(input_string, find_first: False):
    # Find the indices of the first occurrence of "FLAG" and the first occurrence of "FLAGEND"
    if find_first:
        flag_start = input_string.find("FLAG")
    else:
        # Find the indices of the second occurrence of "FLAG" and the first occurrence of "FLAGEND"
        flag_start = input_string.find("FLAG", input_string.find("FLAG") + 1)
    flag_end = input_string.find("FLAGEND")

    # Check if both flags are found
    if flag_start != -1 and flag_end != -1:
        # Extract the substring between the flags
        substring = input_string[flag_start + len("FLAG") : flag_end]

        return substring

    # Return None if either flag is not found
    return None


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
        # We expect to get a 200 and be redirected
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
        # We expect to get a 200 and be redirected
        response = await client.post(
            "/login",
            data={"email": username, "password": password},
            follow_redirects=True,
        )
    except Exception as e:
        logger.warning("LOGIN FAILED")
        handle_RequestError(e, "request error while logging in")
    # We should get redirected else something failed
    # Ensure registration was successful
    logger.info("Login request got status: " + str(response.status_code))
    if response.status_code > 399:
        logger.info("Response message was: " + response.text)
    assert_equals(response.status_code, 200, "login failed")
    logger.info("Login succeeded for " + username)
    return response
