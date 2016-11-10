from jsonschema import validate
import json

from agent.schema.requestSchema import getClaimSchema
from agent.api.data.sample import invitations
from agent.common.errorMessages import errorsMessages

async def getClaim(data):
    validate(data, getClaimSchema)
    invitationId = data["invitationId"]
    if invitationId in invitations:
        invitation = invitations[invitationId]
        claims = list(invitation["claims"].values())
        return json.dumps({"claims": claims, "type": 'getClaim'})

    return errorsMessages['INVALID_CLAIM']
