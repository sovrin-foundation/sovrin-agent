from aiohttp.web import json_response
from jsonschema import validate
from json import dumps, loads

from agent.schema.requestSchema import loginSchema
from agent.common.apiMessages import LOGIN_SUCCESS


async def login(request):
    data = loads(request)
    validate(data, loginSchema)
    return dumps(LOGIN_SUCCESS)


async def loginHttp(request, data):
    validate(data, loginSchema)
    return json_response(data=LOGIN_SUCCESS)