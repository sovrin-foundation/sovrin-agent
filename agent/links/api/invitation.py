from jsonschema import validate
import json

from agent.schema.requestSchema import acceptInvitationSchema
from agent.api.data.sample import invitations

async def acceptInvitation(data):
    validate(data, acceptInvitationSchema)
    # get invitation from dummy data
    invitationId = data["invitation"]["id"]
    if invitationId in invitations:
        response = invitations[invitationId]
        response['type'] = data['type']
        return json.dumps({"type": data['type'],
                           "claims": invitations[invitationId]['claims'],
                           "linkId": data["invitation"]["id"]})

    return json.dumps(data={"type": "error", "error": "No invitation found"})
