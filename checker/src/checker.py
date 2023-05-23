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
import exploit
import utils

checker = Enochecker("t3chn0r4d10", 8000)


@checker.putflag(0)
async def putflag_test(
    task: PutflagCheckerTaskMessage,
    client: AsyncClient,
    db: ChainDB,
) -> None:
    # First Flag Connect to DB and add a flag
    pass


@checker.getflag(0)
async def getflag_test(
    task: GetflagCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> None:
    pass


@checker.exploit(0)
async def exploit_test(searcher: FlagSearcher, client: AsyncClient) -> Optional[str]:
    pass


@checker.putflag(1)
async def putflag_test(
    task: PutflagCheckerTaskMessage,
    client: AsyncClient,
    db: ChainDB,
) -> None:
    # Second file is in config which gets loaded from a file,
    # to set it we need to upload a file
    # with open("flag.txt", "w") as text_file:
    #    text_file.write("%s" % task.flag)
    # TODO can I share memory with other docker?
    pass


@checker.getflag(1)
async def getflag_test(
    task: GetflagCheckerTaskMessage, client: AsyncClient, db: ChainDB
) -> None:
    pass


@checker.exploit(1)
async def exploit_test(searcher: FlagSearcher, client: AsyncClient) -> Optional[str]:
    # Creates a malicious mp3 file named "exploit.mp3"
    exploit.create_malicious_file()
    # TODO add logger
    logger = None
    # register
    url = utils.register_user_and_open_main_page(client, logger)
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
