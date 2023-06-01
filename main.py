from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from firebase_admin import auth
import secrets

secret_key = secrets.token_urlsafe(32)

app = FastAPI()
security = HTTPBearer()

@app.post('/register')
def register(email: str, password: str):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {'message': 'User registered successfully'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/login')
def login(credentials: HTTPAuthorizationCredentials):
    try:
        token = credentials.credentials
        decoded_token = jwt.decode(token, secret, algorithms=['HS256'])
        uid = decoded_token['uid']
        user = auth.get_user(uid)
        return {'message': 'Login successful', 'user': user.email}
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token')

@app.get('/protected')
def protected_route(credentials: HTTPAuthorizationCredentials):
    try:
        token = credentials.credentials
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        uid = decoded_token['uid']
        user = auth.get_user(uid)
        return {'message': 'Protected route accessed', 'user': user.email}
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
