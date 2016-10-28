from aiohttp.web import json_response

from agent.schema.requestSchema import onboardSchema
from jsonschema import validate


async def onboard(request, data):
    validate(data, onboardSchema)
    return json_response(data={"success": True})
