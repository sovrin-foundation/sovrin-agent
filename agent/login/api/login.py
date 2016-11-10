from jsonschema import validate
from json import dumps, loads

from agent.schema.requestSchema import loginSchema

async def login(request):
    data = loads(request)
    validate(data, loginSchema)
    return dumps({"type": "login", "success": True, "status": 200})
