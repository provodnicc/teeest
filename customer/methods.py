import jwt, datetime
from Config.config import API_SECRET
def getToken(user):

    payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, API_SECRET, algorithm='HS256')

    return token

def getPayload(token):
    payload = jwt.decode(token, API_SECRET, algorithms=['HS256'])

    return payload
