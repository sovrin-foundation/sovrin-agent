import os
import signal
from functools import partial

import asyncio

from scripts import startApiServer, startApiServerDebug


def _test_start_script(script):
    args = script.parse_args("")
    loop = asyncio.new_event_loop()
    stop = partial(os.kill, os.getpid(), signal.SIGINT)
    loop.call_later(2, stop)
    script.run(args, loop=loop)


def test_startApiServer():
    _test_start_script(startApiServer)


def test_startApiServerDebug():
    _test_start_script(startApiServerDebug)
