from jsonschema import validate
import json

from agent.schema.requestSchema import acceptInvitationSchema
from agent.api.data.sample import invitations
from agent.common.errorMessages import INVALID_INVITATION

async def acceptInvitation(data, session, url):

    validate(data, acceptInvitationSchema)
    # get invitation from dummy data
    invitationId = data["invitation"]["id"]
    if invitationId in invitations:
        claim = {
            'route': 'getClaims',
            'invitationId': invitationId,
            'signature': 'hjskcdshvbdvqfvqvvervtvw46gbbeyh65'
        }
        async with session.post(url, data=json.dumps(claim)) as response:
            return await response.text()
        #response = invitations[invitationId]
        # response['type'] = data['route']
        # return json.dumps({"type": data['route'],
        #                    "claims": invitations[invitationId]['claims'],
        #                    "linkId": data["invitation"]["id"]})

    return INVALID_INVITATION
