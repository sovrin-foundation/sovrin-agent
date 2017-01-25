from jsonschema import validate

from agent.api.data.sample import invitations
from agent.common.apiMessages import LOGIN_SUCCESS, REGISTER_SUCCESS
from agent.common.errorMessages import INVALID_CLAIM, INVALID_INVITATION, \
    ALREADY_REGISTERED
from agent.common.signatureValidation import validateSignature
from agent.schema.requestSchema import getClaimSchema, acceptInvitationSchema, \
    loginSchema, onboardSchema


class Logic:
    def __init__(self, users=None):
        self._users = users or {}
        # TODO Logic shouldn't know about app at all.
        self._routeMap = {
            'acceptInvitation': self.acceptInvitation,
            'getClaim': self.getClaim,
            'login': self.login,
            'register': self.onboard,
            'onboard': self.onboard
        }

    async def handleMsg(self, kind, data):
        handler = self._routeMap[kind]
        return await handler(data)

    async def getClaim(self, data):
        validate(data, getClaimSchema)
        invitationId = data["invitationId"]
        if invitationId in invitations:
            invitation = invitations[invitationId]
            claims = list(invitation["claims"].values())
            return {"claims": claims, "type": 'getClaim'}
        return INVALID_CLAIM

    async def acceptInvitation(self, data):
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

    async def login(self, data):
        validate(data, loginSchema)
        return LOGIN_SUCCESS

    async def onboard(self, data):
        validate(data, onboardSchema)
        # validate signature
        verified, message = validateSignature(data['signature'],
                                              data['publicKey'],
                                              data['data'])
        if not verified:
            return message
        user = data['publicKey']
        if user not in self._users:
            # Decide what properties to save with a user
            # once we have clarity to implement claims and links
            self._users[user] = {}
        else:
            return ALREADY_REGISTERED
        return REGISTER_SUCCESS
