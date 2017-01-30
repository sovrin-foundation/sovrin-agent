from aiohttp.web import Application
from aiohttp.web_reqrep import json_response

extension_designator = "phonelog-v0.notsodistantfuture.com"

def get_app(loop):

    async def update_handler(request):
        response = {'result':'good'}
        return json_response(data=response)


    subapp = Application(loop=loop)
    subapp.router.add_get('/update', update_handler)  # this is a GET on purpose, to handle webhook style updates.

    return subapp
