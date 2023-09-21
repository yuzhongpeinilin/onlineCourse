import datetime

import jwt

jwt_password = '123456789'


# 创建token
def create_token(account,type):
    body = {
        'account':account,
        'type': type,
        "exp": datetime.datetime.now() + datetime.timedelta(seconds=30),
    }
    # token 编码
    token = jwt.encode(body,jwt_password,algorithm='HS256')
    return token

def pares_token(token):
    account = ''
    type = ''
    errMsg = ''
    if token == None or token == '':
        errMsg = 'token is null'
        return account, type, errMsg
    try:
        body = jwt.decode(token,jwt_password,algorithms=["HS256"])
        # 判断key在不在
        if 'account' not in body:
            errMsg = 'account is null'
            return account, type, errMsg

        # 判断值在不在
        if body["account"] is None or body["account"] == '':
            errMsg = 'account is null'
            return account, type, errMsg
        account = body["account"]
        type = body['type']

    except:
        errMsg = 'token 已经失效'
        return account,type,errMsg
    errMsg = 'ok'
    return account,type,errMsg



