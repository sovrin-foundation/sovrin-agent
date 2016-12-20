from jsonschema import validate
import json

from agent.schema.requestSchema import getClaimSchema
from agent.api.data.sample import invitations
from agent.common.errorMessages import INVALID_CLAIM

async def getClaim(data):
    validate(data, getClaimSchema)
    invitationId = data["invitationId"]
    if invitationId in invitations:
        invitation = invitations[invitationId]
        claims = list(invitation["claims"].values())
        print("sending Alice's claims----------------------")
        print(claims)
        return {"claims": claims, "type": 'getClaim'}

    return INVALID_CLAIM
