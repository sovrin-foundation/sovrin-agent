from aiohttp.web import json_response
from jsonschema import validate

from agent.schema.requestSchema import loginSchema

async def login(request, data):
    validate(data, loginSchema)
    return json_response(data={"success": True})
