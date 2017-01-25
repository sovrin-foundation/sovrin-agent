from jsonschema import validate

from agent.api.data.sample import invitations
from agent.common.apiMessages import LOGIN_SUCCESS, REGISTER_SUCCESS
from agent.common.errorMessages import INVALID_CLAIM, INVALID_INVITATION, \
    ALREADY_REGISTERED
from agent.common.signatureValidation import validateSignature
from agent.schema.requestSchema import getClaimSchema, acceptInvitationSchema, \
    loginSchema, onboardSchema


async def handleMsg(kind, data, app):
    handler = routeMap[kind]
    return await handler(data, app)


async def getClaim(data, app=None):
    validate(data, getClaimSchema)
    invitationId = data["invitationId"]
    if invitationId in invitations:
        invitation = invitations[invitationId]
        claims = list(invitation["claims"].values())
        return {"claims": claims, "type": 'getClaim'}
    return INVALID_CLAIM


async def acceptInvitation(data, app=None):

    validate(data, acceptInvitationSchema)
    # get invitation from dummy data
    invitationId = data["invitation"]["id"]
    if invitationId in invitations:
        response = invitations[invitationId]
        response['type'] = data['route']
        return {"type": data['route'],
                           "claims": invitations[invitationId]['claims'],
                           "linkId": data["invitation"]["id"]}

    return INVALID_INVITATION


async def login(data, app=None):
    validate(data, loginSchema)
    return LOGIN_SUCCESS


async def onboard(data, app=None):
    validate(data, onboardSchema)

    # validate signature
    verified, message = validateSignature(data['signature'], data['publicKey'], data['data'])
    if not verified:
        return message
    users = app['users']
    user = data['publicKey']
    if user not in users:
        # Decide what properties to save with a user
        # once we have clarity to implement claims and links
        users[user] = {}
    else:
        return ALREADY_REGISTERED

    return REGISTER_SUCCESS


routeMap = {
    'acceptInvitation': acceptInvitation,
    'getClaim': getClaim,
    'login': login,
    'register': onboard,
    'onboard': onboard
}
