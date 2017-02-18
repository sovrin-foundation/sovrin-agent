from aiohttp.web import Application
from aiohttp.web_reqrep import json_response

from agent.extensions.APIExtension import APIExtension


class LocationV0(APIExtension):

    def __init__(self):
        pass

    def get_designator(self):
        return "location-v0.notsodistantfuture.com"

    def get_app(self, loop):

        subapp = Application(loop=loop)
        subapp.router.add_get('/timezone', self.timezone_handler)

        return subapp

    async def timezone_handler(self, request):
            timezone_bundle = {}
            return json_response(data=timezone_bundle)