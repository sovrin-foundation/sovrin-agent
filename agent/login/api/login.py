from jsonschema import validate
from json import dumps
from agent.common.errorMessages import USER_NOT_FOUND

from agent.schema.requestSchema import loginSchema
from agent.common.apiMessages import LOGIN_SUCCESS


async def login(data, app):
    validate(data, loginSchema)

    if data['publicKey'] in app['users']:
        return dumps(LOGIN_SUCCESS)

    return dumps(USER_NOT_FOUND)
