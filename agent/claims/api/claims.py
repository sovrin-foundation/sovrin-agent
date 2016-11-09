from jsonschema import ValidationError
from jsonschema import validate
import json

from agent.schema.requestSchema import getClaimSchema
from agent.api.data.sample import invitations
from agent.common.errorCodes import errorsMessages

async def getClaim(data):
    try:
        validate(data, getClaimSchema)
    except (TypeError, KeyError, ValidationError):
        return errorsMessages['INVALID_DATA']

    invitationId = data["invitationId"]
    if invitationId in invitations:
        invitation = invitations[invitationId]
        claims = list(invitation["claims"].values())
        return json.dumps({"claims": claims, "type": 'getClaim'})

    return errorsMessages['INVALID_CLAIM']
