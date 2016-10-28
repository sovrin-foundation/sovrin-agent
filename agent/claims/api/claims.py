from aiohttp.web import json_response
from jsonschema import validate

from agent.schema.requestSchema import getClaimSchema
from agent.api.data.sample import invitations


async def getClaim(request, data):
    validate(data, getClaimSchema)
    invitationId = data["invitationId"]
    if invitationId in invitations:
        invitation = invitations[invitationId]
        claims = list(invitation["claims"].values())
        return json_response(data={"claims": claims})

    return json_response(data={"error": "No invitation found"})
