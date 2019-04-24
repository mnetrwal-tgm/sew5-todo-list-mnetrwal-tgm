import base64

from server.python.server import app as App

import pytest
import json

# Setup

@pytest.fixture
def client():
    client = App.test_client()
    yield client

@pytest.fixture
def authtoken(client):
    res = client.get('/login', headers={
        'Authorization': 'Basic ' + base64.b64encode('admin:Lorem'.encode('utf-8')).decode('utf-8')})
    authtoken = json.loads(res.data.decode('UTF-8'))['token']
    yield authtoken

@pytest.fixture
def saneid(client,authtoken):
    res = client.get('/todolists?token=%s'%authtoken)
    saneid = json.loads(res.data.decode('UTF-8'))[0]['id']
    yield saneid

# Sanity

def test_ping_code(client):
    res = client.get('/ping')
    assert res.status_code == 200

def test_ping_return(client):
    res = client.get('/ping')
    assert b'pong' == res.data

# Auth

def test_auth_denied(client):
    res=client.get('/todolists', headers={'Authorization': 'Basic ' + base64.b64encode('asamir:Lauriem'.encode('utf-8')).decode('utf-8')})
    assert 403 == res.status_code

def test_login_success(client):
    res=client.get('/login', headers={'Authorization': 'Basic ' + base64.b64encode('admin:Lorem'.encode('utf-8')).decode('utf-8')})
    assert 200 == res.status_code

def test_auth_has_token(client,authtoken):
    res=client.get('/todolists?token=%s'%authtoken)
    assert 200 == res.status_code

# Get


def test_get_lists(client,authtoken):
    res = client.get('/todolists?token=%s'%authtoken)
    assert 200 == res.status_code

def test_get_list(client,authtoken,saneid):
    res = client.get('/%s?token=%s'%(saneid,authtoken))
    assert 200 == res.status_code

def test_get_items(client,authtoken,saneid):
    res = client.get('/%s/items?token=%s'%(saneid,authtoken))
    assert 200 == res.status_code

# Post

def test_post_list(client,authtoken):
    res = client.post('/todolists?token=%s'%authtoken, json=json.dumps({'name':'Ich Bin Ein Test'}))
    assert 201 == res.status_code

def test_post_item(client,authtoken,saneid):
    res = client.post('/%s/items?token=%s'%(saneid,authtoken),json=json.dumps({'name':'Ich Bin Ein Test'}))
    assert 200 == res.status_code
