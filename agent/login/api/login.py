from jsonschema import validate
from jsonschema.exceptions import ValidationError
from json import dumps, loads

from agent.schema.requestSchema import loginSchema
from agent.common.errorCodes import errorsMessages

async def login(request):
    data = loads(request)
    try:
        validate(data, loginSchema)
    except (TypeError, KeyError, ValidationError):
        return errorsMessages['INVALID_DATA']
    return dumps({"type": "login", "success": True, "status": 200})
