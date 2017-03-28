#!/usr/bin/python

import base64
import json
import requests
import sys

def get_admin_token():
    # consul http endpoint
    resp = requests.get('http://localhost:8500/v1/kv/admin_token')
    resp.raise_for_status()
    return base64.b64decode(resp.json()[0]['Value'])

def get_user(name, admin_token):
    url = 'http://localhost:35357/keystone_admin/v3/users?name=%s' % name
    resp = requests.get(url, headers={'x-auth-token': admin_token})
    resp.raise_for_status()
    return resp.json()['users'][0]

def main():
    """
    Update password based on consul watch json stdin like:
    [
        {
            "CreateIndex": 15909,
            "Flags": 0,
            "Key": "passwords/{username}",
            "LockIndex": 0,
            "ModifyIndex": 106495,
            "Session": "",
            "Value": "cGFzc3dvcmQx"
        }
    ]
    Value is new b64 encoded password.
    print statements go to the consul DEBUG log.
    """
    update_str = sys.stdin.read()
    print 'running %s with stdin:\n%s' % (sys.argv[0], update_str)
    update = json.loads(update_str)
    username = update[0]['Key'].split('/')[-1]
    new_password = base64.b64decode(update[0]['Value'])
    admin_token = get_admin_token()
    user = get_user(username, admin_token)
    url = 'http://localhost:35357/keystone_admin/v3/users/%s' % user['id']
    body = {'user': {'password': new_password}}
    headers = {
        'x-auth-token': admin_token,
        'content-type': 'application/json'
    }
    resp = requests.patch(url, headers=headers, data=json.dumps(body))
    resp.raise_for_status()

    print 'Successfully updated password for %s' % username

if __name__ == '__main__':
    sys.exit(main())
