import json
import uuid
import jwt
import datetime
import os

from functools import wraps

from flask import Flask, request
from flask_api import status
from flask_cors import CORS

from passlib.apps import custom_app_context as pwd_context


# configuration
DEBUG = True



# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

TODOLISTS = [
    {
        'id': uuid.uuid4().hex,
        'name': 'Test',
        'lock': False,
        'items': [
            {'name': 'Bin am Laufen','status':True}, {'name': 'Ich bin done','status':False}
        ]
    },
{
        'id': uuid.uuid4().hex,
        'name': 'Test2',
        'lock': False,
        'items': [
            {'name': 'Bin am Laufen','status':True}, {'name': 'Ich bin done','status':False}
        ]
    }
]

def hash_password(password):
    return pwd_context.hash(password)

USERS = [
    {
        'uname':'admin',
        'pwd':hash_password('Lorem')
    }
]


try:
    with open("data.json",'r') as file:
        TODOLISTS=json.load(file)
except Exception:
    pass

# Auth

app.config['SECRET_KEY']=os.urandom(24)

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=request.args.get('token')
        if not token:
            return "Token missing. Visit /login",status.HTTP_403_FORBIDDEN
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return "Token invalid",status.HTTP_403_FORBIDDEN
        return f(*args,**kwargs)
    return decorated

@app.route('/login')
def login():
    try:
        auth = request.authorization
        authcorrect=False
        for user in USERS:
            if auth.username == user['uname']:
                pwd_context.verify(auth.password, user['pwd'])
                authcorrect=True
                break
        if authcorrect:
            token=jwt.encode({'user': auth.username, 'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
            return json.dumps({'token':token.decode("UTF-8")}),status.HTTP_200_OK
        return status.HTTP_401_UNAUTHORIZED
    except:
        return status.HTTP_400_BAD_REQUEST

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return "pong",status.HTTP_200_OK



def checkItemOnList(listid,post_data):
    ret=False
    if post_data['itemname']!="":
        for list in TODOLISTS:
            if list['id']==listid:
                ret=True
                for item in list['items']:
                    if item['name'] == post_data['itemname']:
                        ret=False
                break
    return ret


@app.route('/todolists', methods=['GET', 'POST'])
@token_required
def all_lists():
    if request.method == 'POST':
        post_data = request.get_json()
        TODOLISTS.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'lock': False,
            'items': []
        })
        saveData()
        return status.HTTP_201_CREATED
    else:
        return json.dumps(TODOLISTS), status.HTTP_200_OK



@app.route('/<listid>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def single_todolist(listid):
    if request.method == 'GET':
        for todolist in TODOLISTS:
            if todolist['id'] == listid:
                return json.dumps(todolist), status.HTTP_200_OK
        return status.HTTP_404_NOT_FOUND
    if request.method == 'PUT':
        post_data = request.get_json()
        for idx,list in enumerate(TODOLISTS):
            if list['id']==listid:
                if not list['lock']:
                    list['name'] = post_data['name']
                    list['lock'] = post_data['lock']
                    list['items'] = post_data['items']
                elif list['lock'] != post_data['lock']:
                    list['lock'] = not post_data['lock']
                else:
                    return 'List locked', status.HTTP_400_BAD_REQUEST
                TODOLISTS[idx]=list
                saveData()
                return status.HTTP_200_OK
    if request.method == 'DELETE':
        if remove_list(listid):
            return status.HTTP_200_OK
        else:
            return status.HTTP_404_NOT_FOUND

@app.route('/<listid>/items', methods=['GET', 'POST'])
@token_required
def all_todoitems(listid):
    if request.method == 'POST':
        post_data = request.get_json()
        if checkItemOnList(listid,post_data):
            for idx,list in enumerate(TODOLISTS):
                if list['id'] == listid:
                    list['items'].append({
                        'name':post_data['itemname'],
                        'status':True
                    })
                    TODOLISTS[idx]=list
            saveData()
            return status.HTTP_201_CREATED
        else:
            return status.HTTP_404_NOT_FOUND
    else:
        for list in TODOLISTS:
            if list['id']==listid:
                return json.dumps(list['items']), status.HTTP_200_OK

@app.route('/<listid>/<itemname>', methods=['PUT', 'DELETE','GET'])
@token_required
def one_todoitem(listid,itemname):
    if request.method in ['PUT','DELETE','GET']:
        post_data = request.get_json()
        if checkItemOnList(listid,post_data):
            for idx,list in enumerate(TODOLISTS):
                if list['id'] == listid:
                    for item in list['items']:
                        if item['name']==itemname:
                            itemdupe=item
                            if request.method=='DELETE':
                                list['items'].remove(item)
                            if request.method=='PUT':
                                itemdupe['name']=post_data['name']
                                itemdupe['status']=post_data['status']
                                list.append(itemdupe)
                            if request.method=='GET':
                                return json.dumps(itemdupe)
                            TODOLISTS[idx]=list
                            saveData()
                            return status.HTTP_200_OK
        else:
            return status.HTTP_404_NOT_FOUND
    return status.HTTP_404_NOT_FOUND


def remove_list(listid):
    for list in TODOLISTS:
        if list['id'] == listid:
            TODOLISTS.remove(list)
            saveData()
            return True
    return False


def saveData():
    with open("data.json",'w') as file:
        file.write(json.dumps(TODOLISTS))


if __name__ == '__main__':
    app.run()
