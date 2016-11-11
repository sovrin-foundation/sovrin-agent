from json import dumps
from jsonschema import validate

from agent.schema.requestSchema import onboardSchema
from agent.common.errorMessages import ALREADY_REGISTERED
from agent.common.signatureValidation import validateSignature

async def onboard(data, app):
    validate(data, onboardSchema)

    # validate signature
    verified = validateSignature(data['signature'], data['publicKey'], data['sovrinId'])
    if verified != 'success':
        return verified
    users = app['users']
    user = data['publicKey']
    if user not in users:
        # Decide what properties to save with a user
        # once we have clarity to implement claims and links
        users[user] = {}
    else:
        return ALREADY_REGISTERED

    return dumps({"type": "register", "success": True, "status": 200})
