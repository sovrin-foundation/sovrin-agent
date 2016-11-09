from json import dumps, loads

from jsonschema import ValidationError

from agent.schema.requestSchema import onboardSchema
from jsonschema import validate
from agent.common.errorCodes import errorsMessages


async def onboard(request):
    data = loads(request)
    try:
        validate(data, onboardSchema)
    except (TypeError, KeyError, ValidationError):
        return errorsMessages['INVALID_DATA']

    return dumps({"type": "register", "success": True, "status": 200})
