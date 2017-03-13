#! /usr/bin/env python3

import errno
import traceback
import argparse

from asyncio import get_event_loop

import sys
from aiohttp import web
from agent.api.apiServer import newApi

from agent.api.logic import Logic


def run(args):
    agentApi = newApi(get_event_loop(), Logic())
    try:
        web.run_app(agentApi, host=args.host, port=args.port)
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            traceback.print_exc()
            exit(2)
        else:
            raise

def parse_args(args):
    parser = argparse.ArgumentParser(description="Start agent api server")

    parser.add_argument("host", nargs="?", default="0.0.0.0")
    parser.add_argument("port", nargs="?", type=int, default=8080)

    return parser.parse_args(args)


if __name__ == '__main__':
    run(parse_args(sys.argv[1:]))
