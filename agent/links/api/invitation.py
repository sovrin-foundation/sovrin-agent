from jsonschema import validate
import json

from agent.schema.requestSchema import acceptInvitationSchema
from agent.api.data.sample import invitations
from agent.common.errorCodes import errorsMessages

async def acceptInvitation(data):

    validate(data, acceptInvitationSchema)
    # get invitation from dummy data
    invitationId = data["invitation"]["id"]
    if invitationId in invitations:
        response = invitations[invitationId]
        response['type'] = data['route']
        return json.dumps({"type": data['route'],
                           "claims": invitations[invitationId]['claims'],
                           "linkId": data["invitation"]["id"]})

    return errorsMessages['INVALID_INVITATION']
