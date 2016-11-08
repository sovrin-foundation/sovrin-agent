import pytest

from json import dumps
from functools import reduce
from agent.api.apiServer import api


@pytest.fixture
def client(loop, test_client):
    return loop.run_until_complete(test_client(api(loop)))


@pytest.mark.parametrize('url, status, key, errorMessage', [
    ('/v1/onboard', 400, 'error', "None is not of type 'object'"),
    ('/v1/login', 400, 'error', "None is not of type 'object'"),
    ('/v1/acceptInvitation', 400, 'error', "None is not of type 'object'"),
    ('/v1/getClaim', 400, 'error', "None is not of type 'object'")
])
def test_routeFailure(loop, client, url, status, key, errorMessage):
    response = loop.run_until_complete(client.post(url))
    assert response.status == status
    responseText = loop.run_until_complete(response.json())
    assert key in responseText
    assert responseText[key] == errorMessage


def test_noIndexRoute(loop, client):
    response = loop.run_until_complete(client.get('/'))
    assert response.status == 404


def test_onboardSuccess(loop, client):
    # TODO:KS generate this signature, key from nacl
    postData = dumps({
        'signature': '979nknksdnknkskdsha797979878',
        'sovrinId': 'sovrinId',
        'publicKey': 'o9889899bs0y8asndjds99sd79sdndjs7='
    })
    response = loop.run_until_complete(client.post('/v1/onboard', data=postData))
    assert response.status == 200
    responseJson = loop.run_until_complete(response.json())
    assert 'success' in responseJson
    assert responseJson['success'] == True


def test_loginSuccess(loop, client):
    # TODO:KS generate this signature from nacl generated secret key
    postData = dumps({
        'signature': '979nknksdnknkskdsha797979878',
        'sovrinId': 'sovrinId'
    })
    response = loop.run_until_complete(client.post('/v1/login', data=postData))
    assert response.status == 200
    responseJson = loop.run_until_complete(response.json())
    assert 'success' in responseJson
    assert responseJson['success'] == True


def test_acceptInvitationSuccess(loop, client):
    postData = dumps({
        'signature': '979nknksdnknkskdsha797979878',
        'sovrinId': 'sovrinId',
        'invitation': {
            'id': '3W2465HP3OUPGkiNlTMl2iZ+NiMZegfUFIsl8378KH4=',
            'publicKey': 'adfasdfuyaddfiaifd8f8d6f8df764svua',
            'signature': 'oiadmmat0-tvknaai7efa7f5aklfaf=adf8ff'
        }
    })
    response = loop.run_until_complete(client.post(
        "/v1/acceptInvitation",
        data=postData
    ))
    assert response.status == 200
    responseJson = loop.run_until_complete(response.json())
    assert "claims" in responseJson
    assert "cd40:98nkk86698688" in responseJson["claims"]


def test_getClaimSuccess(loop, client):
    postData = dumps({
        'signature': '979nknksdnknkskdsha797979878',
        'invitationId': '3W2465HP3OUPGkiNlTMl2iZ+NiMZegfUFIsl8378KH4='
    })
    response = loop.run_until_complete(client.post(
        '/v1/getClaim',
        data=postData
    ))
    assert response.status == 200
    responseJson = loop.run_until_complete(response.json())
    assert 'claims' in responseJson
    claims = responseJson['claims']
    assert len(claims) > 0
    claim = reduce((lambda x, y: y), list(filter(
        lambda x: x['identifier'] == 'cd40:98nkk86698688',
        claims
    )), {})
    assert 'degree' in claim['attributes']

