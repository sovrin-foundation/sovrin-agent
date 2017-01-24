from aiohttp.web import json_response
from jsonschema import validate
from json import dumps

from agent.schema.requestSchema import acceptInvitationSchema
from agent.api.data.sample import invitations
from agent.common.errorMessages import INVALID_INVITATION


async def acceptInvitation(data):

    validate(data, acceptInvitationSchema)
    # get invitation from dummy data
    invitationId = data["invitation"]["id"]
    if invitationId in invitations:
        response = invitations[invitationId]
        response['type'] = data['route']
        return dumps({"type": data['route'],
                           "claims": invitations[invitationId]['claims'],
                           "linkId": data["invitation"]["id"]})

    return dumps(INVALID_INVITATION)


async def acceptInvitationHttp(request, data):
    validate(data, acceptInvitationSchema)
    invitationId = data["invitation"]["id"]
    if invitationId in invitations:
        return json_response(data={"type": data['route'],
                                   "claims": invitations[invitationId]['claims'],
                                   "linkId": data["invitation"]["id"]})

    return json_response(data=INVALID_INVITATION)