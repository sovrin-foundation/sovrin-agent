from addict import Dict

# this list is maintained because we need to use these constants
# for version management and API name, we will resolve schema for specific API
# as well using these constants
resourceStrings = Dict({
    "V1": "v1",
    "ONBOARD": "onboard",
    "LOGIN": "login",
    "ACCEPT_INVITATION": "acceptInvitation",
    "GET_CLAIM": "getClaim"
})
