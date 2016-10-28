from aiohttp.web import json_response
from jsonschema import validate

from agent.schema.requestSchema import acceptInvitationSchema
from agent.api.data.sample import invitations

async def acceptInvitation(request, data):
    validate(data, acceptInvitationSchema)
    # get invitation from dummy data
    invitationId = data["invitation"]["id"]
    if invitationId in invitations:
        return json_response(data=invitations[invitationId])

    return json_response(data={"error": "No invitation found"})
