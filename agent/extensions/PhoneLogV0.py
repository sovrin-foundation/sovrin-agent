from aiohttp.web import Application
from aiohttp.web_reqrep import json_response

from agent.extensions.APIExtension import APIExtension

def get_app(loop):

    async def update_handler(request):
        response = {'result':'good'}
        return json_response(data=response)


    subapp = Application(loop=loop)
    subapp.router.add_get('/update', update_handler)  # this is a GET on purpose, to handle webhook style updates.

    return subapp


class PhoneLogV0(APIExtension):

    def __init__(self):
        pass

    def get_designator(self):
        return "phonelog-v0.notsodistantfuture.com"

    def get_app(self, loop):

        subapp = Application(loop=loop)
        subapp.router.add_get('/update', self.update_handler)  # this is a GET on purpose, to handle webhook style updates.

        return subapp

    async def update_handler(self, request):
        response = {'result':'good'}
        return json_response(data=response)
