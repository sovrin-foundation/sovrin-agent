from json import dumps

from agent.schema.requestSchema import onboardSchema
from jsonschema import validate


async def onboard(data, app):
    validate(data, onboardSchema)

    # validate signature
    # check if user is registered, then return already registered
    # else add user to app['user'] set, along with publicKey

    return dumps({"type": "register", "success": True, "status": 200})
