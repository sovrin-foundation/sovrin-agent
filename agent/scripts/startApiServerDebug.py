import argparse

from asyncio import get_event_loop
from aiohttp import web
from agent.api.apiServer import newApi

# get host and port from command line
parser = argparse.ArgumentParser(description="Start agent api server")

parser.add_argument("name", nargs="?", default="Faber")
parser.add_argument("seed", nargs="?", default="Faber000000000000000000000000000")
parser.add_argument("host", nargs="?", default="0.0.0.0")
parser.add_argument("port", nargs="?", type=int, default=8080)

args = parser.parse_args()

# run api
agentApi = newApi(get_event_loop(), args.name, args.seed)
web.run_app(agentApi, host=args.host, port=args.port)
