from aiohttp.web import Application
from aiohttp.web_reqrep import json_response

extension_designator = "location-v0.notsodistantfuture.com"

def get_app(loop):
    async def timezone_handler(request):
        timezone_bundle = {}
        return json_response(data=timezone_bundle)


    locationapp = Application(loop=loop)
    locationapp.router.add_get('/timezone', timezone_handler)

    return locationapp