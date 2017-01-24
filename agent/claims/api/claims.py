from jsonschema import validate
from aiohttp.web import json_response
from json import dumps

from agent.schema.requestSchema import getClaimSchema
from agent.api.data.sample import invitations
from agent.common.errorMessages import INVALID_CLAIM


async def getClaim(data):
    validate(data, getClaimSchema)
    invitationId = data["invitationId"]
    if invitationId in invitations:
        invitation = invitations[invitationId]
        claims = list(invitation["claims"].values())
        return dumps({"claims": claims, "type": 'getClaim'})

    return dumps(INVALID_CLAIM)


async def getClaimHttp(request, data):
    validate(data, getClaimSchema)
    invitationId = data["invitationId"]
    if invitationId in invitations:
        invitation = invitations[invitationId]
        claims = list(invitation["claims"].values())
        return json_response(data={"claims": claims, "type": 'getClaim'})

    return json_response(data=INVALID_CLAIM)