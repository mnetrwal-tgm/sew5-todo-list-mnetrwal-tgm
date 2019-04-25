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
    return saneid

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
# Don't work for some reason. I don't fucking know why, but werkzeug doesn't like post

def test_post_list(client,authtoken):
    data={'name':'Ich Bin Ein Test'}
    res = client.post('/todolists?token=%s'%authtoken, json=data)
    assert 201 == res.status_code

def test_post_item(client,authtoken,saneid):
    res = client.post('/%s/items?token=%s'%(saneid,authtoken),json={'name':'Ich Bin Ein Test'})
    assert 201 == res.status_code

# Put

def test_put_list(client,authtoken,saneid):
    res = client.get('/%s?token=%s' % (saneid, authtoken))
    data=json.loads(res.data)
    data['name']="Lorem"
    res = client.put('/%s?token=%s'%(saneid,authtoken), json=data)
    assert 200 == res.status_code

def test_put_item(client,authtoken,saneid):
    res = client.get('/%s?token=%s' % (saneid, authtoken))
    data=json.loads(res.data)
    data['items'][len(data['items'])-1]['status']=False
    itname=str(data['items'][len(data['items'])-1]['name'])
    res = client.put('/%s/%s?token=%s'%(saneid,itname,authtoken), json=data['items'][0])
    assert 200 == res.status_code

# Lock

def test_lock(client,authtoken,saneid):
    res = client.get('/%s?token=%s' % (saneid, authtoken))
    data = json.loads(res.data)
    data['lock'] = True
    res = client.put('/%s?token=%s' % (saneid, authtoken), json=data)
    assert 200 == res.status_code
    res = client.put('/%s?token=%s' % (saneid, authtoken), json=data)
    assert 400 == res.status_code

# Delete

def test_delete_item(client,authtoken,saneid):
    res = client.get('/%s?token=%s' % (saneid, authtoken))
    data = json.loads(res.data)
    itname = str(data['items'][len(data['items'])-1]['name'])
    res = client.delete('/%s/%s?token=%s' % (saneid, itname, authtoken))
    assert 200 == res.status_code

def test_delete_list(client,authtoken,saneid):
    res = client.delete('/%s?token=%s' % (saneid, authtoken))
    assert 200 == res.status_code