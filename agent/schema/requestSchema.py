from addict import Dict
from agent.common.constant import resourceStrings

onboardSchema = {
    "type": "object",
    "properties": {
        # TODO:SC Remove common schema and put it on request
        # and check it for each web socket request
        "route": {
            "type": "string"
        },
        "signature": {
            "type": "string"
        },
        "sovrinId": {
            "type": "string"
        },
        "publicKey": {
            "type": "string"
        },
        "data": {
            "type": "string"
        }
    },
    "required": ["signature", "sovrinId", "publicKey"]
}

loginSchema = {
    "type": "object",
    "properties": {
        "route": {
            "type": "string"
        },
        "signature": {
            "type": "string"
        },
        "sovrinId": {
            "type": "string"
        }
    },
    "required": ["signature", "sovrinId"]
}

acceptInvitationSchema = {
    "type": "object",
    "properties": {
        "route": {
            "type": "string"
        },
        "signature": {
            "type": "string"
        },
        "sovrinId": {
            "type": "string"
        },
        "invitation": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string"
                },
                "publicKey": {
                    "type": "string"
                },
                "signature": {
                    "type": "string"
                }
            },
            "required": ["id", "signature", "publicKey"]
        }
    },
    "required": ["signature", "sovrinId", "invitation"]
}

getClaimSchema = {
    "type": "object",
    "properties": {
        "invitationId": {
            "route": {
                "type": "string"
            },
            "type": "string"
        },
        "signature": {
            "type": "string"
        }
    },
    "required": ["invitationId", "signature"]
}

# Decide among ProtoBuf, Avro and thrift

schemaDict = {
    resourceStrings.V1: {
        resourceStrings.ONBOARD: onboardSchema,
        resourceStrings.LOGIN: loginSchema,
        resourceStrings.ACCEPT_INVITATION: acceptInvitationSchema,
        resourceStrings.GET_CLAIM: getClaimSchema
    }
}

requestSchema = Dict(schemaDict)
