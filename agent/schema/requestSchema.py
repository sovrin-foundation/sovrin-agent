from addict import Dict
from agent.common.constant import resourceStrings

onboardSchema = {
    "type": "object",
    "properties": {
        "signature": {
            "type": "string"
        },
        "sovrinId": {
            "type": "string"
        },
        "publicKey": {
            "type": "string"
        }
    },
    "required": ["signature", "sovrinId", "publicKey"]
}

loginSchema = {
    "type": "object",
    "properties": {
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
            "type": "string"
        },
        "signature": {
            "type": "string"
        }
    },
    "required": ["invitationId", "signature"]
}

# Decide b/w ProtoBuf and Avro

schemaDict = {
    resourceStrings.V1: {
        resourceStrings.ONBOARD: onboardSchema,
        resourceStrings.LOGIN: loginSchema,
        resourceStrings.ACCEPT_INVITATION: acceptInvitationSchema,
        resourceStrings.GET_CLAIM: getClaimSchema
    }
}

requestSchema = Dict(schemaDict)
