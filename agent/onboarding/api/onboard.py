from json import dumps, loads

from agent.schema.requestSchema import onboardSchema
from jsonschema import validate


async def onboard(request):
    data = loads(request)
    validate(data, onboardSchema)

    return dumps({"type": "register", "success": True, "status": 200})
