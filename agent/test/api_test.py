from asyncio import get_event_loop, new_event_loop

import pytest

from json import dumps, loads
from functools import reduce

from jsonschema import ValidationError

from agent.api.apiServer import newApi
from agent.api.logic import Logic
from agent.test import sample


@pytest.fixture
def logic():
    return Logic(invitations=sample.invitations)


@pytest.fixture
def app(loop, logic):
    return newApi(loop, logic)


@pytest.fixture
def client(loop, app, test_client):
    # loop = new_event_loop()
    return loop.run_until_complete(test_client(app))


def test_onboardError(loop, logic):
    postData = dumps({
        'sovrinId': 'sovrinId',
        'publicKey': 'o9889899bs0y8asndjds99sd79sdndjs7=',
        'route': 'register'
    })
    with pytest.raises(ValidationError):
        loop.run_until_complete(logic._onboard(postData))


def test_loginError(loop, logic):
    postData = dumps({
        'signature': '979nknksdnknkskdsha797979878',
        'route': 'register'
    })
    with pytest.raises(ValidationError):
        loop.run_until_complete(logic._login(postData))


def test_claimError(loop, logic):
    postData = dumps({
        'signature': '979nknksdnknkskdsha797979878',
        'route': 'register'
    })
    with pytest.raises(ValidationError):
        loop.run_until_complete(logic._getClaim(postData))

    postData = {
        'signature': '979nknksdnknkskdsha797979878',
        'invitationId': '3W2465HP3OUPGkiNlTMl2iZ+NiMZegfUFIsl8372334',
        'route': 'getClaim'
    }
    response = loop.run_until_complete(logic._getClaim(postData))
    assert response['error']['status'] == 400
    assert response['error']['message'] == 'invalid claim'


def test_invitationError(loop, logic):
    postData = {
        'route': 'acceptInvitation',
        'signature': '979nknksdnknkskdsha797979878',
        'invitation': {
            'id': '3W2465HP3OUPGkiNlTMl2iZ+NiMZegfUFIsl8378KH4=',
            'publicKey': 'adfasdfuyaddfiaifd8f8d6f8df764svua',
            'signature': 'oiadmmat0-tvknaai7efa7f5aklfaf=adf8ff'
        }
    }
    with pytest.raises(ValidationError):
        loop.run_until_complete(logic._acceptInvitation(postData))

    postData = {
        'route': 'acceptInvitation',
        'signature': '979nknksdnknkskdsha797979878',
        'sovrinId': 'sovrinId',
        'invitation': {
            'id': '3W2465HP3OUPGkiNlTMl2iZ+NiMZegfUFIsl8378K875',
            'publicKey': 'adfasdfuyaddfiaifd8f8d6f8df764svua',
            'signature': 'oiadmmat0-tvknaai7efa7f5aklfaf=adf8ff'
        }
    }
    response = loop.run_until_complete(logic._acceptInvitation(postData))
    assert response['error']['status'] == 400
    assert response['error']['message'] == 'invalid invitation'


def test_onboardSuccess(loop, logic):
    # TODO:KS generate this signature, key from nacl
    postData = dumps({
        'signature': 'xTayONsFJnVNmgGH8CFIGbZcfI6ikR+w9kPuzUkAqFFTdkm6Eujy5AYx+PwEgwZkm5ob6nPDXYGS2aTCFyhcDHNvdnJpbklk',
        'sovrinId': 'sovrinId',
        'data': dumps({'message': 'sovrinId'}),
        'publicKey': 'eutTvvZLl5OmPkCl29WNFmwUpsJrDzuZUuS+hm36TJ4=',
        'route': 'register'
    })
    response = loop.run_until_complete(logic._onboard(loads(postData)))
    assert response['success']['status'] == 200
    assert 'success' in response['success']
    assert response['success']['success'] == True


def test_loginSuccess(loop, logic):
    # TODO:KS generate this signature from nacl generated secret key
    postData = dumps({
        'signature': '979nknksdnknkskdsha797979878',
        'sovrinId': 'sovrinId',
        'route': 'register'
    })
    response = loop.run_until_complete(logic._login(loads(postData)))
    assert response['success']['status'] == 200
    assert 'success' in response['success']
    assert response['success']['success'] == True


# TODO:SC test websocket connection
def test_acceptInvitationSuccess(loop, logic):
    postData = {
        'route': 'acceptInvitation',
        'signature': '979nknksdnknkskdsha797979878',
        'sovrinId': 'sovrinId',
        'invitation': {
            'id': '3W2465HP3OUPGkiNlTMl2iZ+NiMZegfUFIsl8378KH4=',
            'publicKey': 'adfasdfuyaddfiaifd8f8d6f8df764svua',
            'signature': 'oiadmmat0-tvknaai7efa7f5aklfaf=adf8ff'
        }
    }
    response = loop.run_until_complete(logic._acceptInvitation(postData))
    assert "claims" in response
    assert "cd40:98nkk86698688" in response["claims"]


# TODO:SC test websocket connection
def test_getClaimSuccess(loop, logic):
    postData = {
        'signature': '979nknksdnknkskdsha797979878',
        'invitationId': '3W2465HP3OUPGkiNlTMl2iZ+NiMZegfUFIsl8378KH4=',
        'route': 'getClaim'
    }
    response = loop.run_until_complete(logic._getClaim(postData))
    assert 'claims' in response
    claims = response['claims']
    assert len(claims) > 0
    claim = reduce((lambda x, y: y), list(filter(
        lambda x: x['identifier'] == 'cd40:98nkk86698688',
        claims
    )), {})
    assert 'degree' in claim['attributes']


def test_onboardSuccessHtpp(loop, client):
    # TODO:KS generate this signature, key from nacl
    postData = dumps({
        'signature': 'xTayONsFJnVNmgGH8CFIGbZcfI6ikR+w9kPuzUkAqFFTdkm6Eujy5AYx+PwEgwZkm5ob6nPDXYGS2aTCFyhcDHNvdnJpbklk',
        'sovrinId': 'sovrinId',
        'data': dumps({'message': 'sovrinId'}),
        'publicKey': 'eutTvvZLl5OmPkCl29WNFmwUpsJrDzuZUuS+hm36TJ4=',
        'route': 'register'
    })
    response = loop.run_until_complete(client.post('/v1/onboard', data=postData))
    assert response.status == 200
    responseJson = loop.run_until_complete(response.json())
    assert 'success' in responseJson
    assert responseJson['success']['success'] == True


def test_loginSuccessHttp(loop, client):
    # TODO:KS generate this signature from nacl generated secret key
    postData = dumps({
        'signature': '979nknksdnknkskdsha797979878',
        'sovrinId': 'sovrinId',
        'route': 'register'
    })
    response = loop.run_until_complete(client.post('/v1/login', data=postData))
    assert response.status == 200
    responseJson = loop.run_until_complete(response.json())
    assert 'success' in responseJson
    assert responseJson['success']['success'] == True


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


def test_acceptInvitationSuccessHttp(loop, client):
    postData = dumps({
        'route': 'acceptInvitation',
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


def test_getClaimSuccessHtpp(loop, client):
    postData = dumps({
        'signature': '979nknksdnknkskdsha797979878',
        'invitationId': '3W2465HP3OUPGkiNlTMl2iZ+NiMZegfUFIsl8378KH4=',
        'route': 'getClaim'
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
