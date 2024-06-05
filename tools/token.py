from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status

# Define la clave secreta para firmar el token
SECRET_KEY = "GatoCatGattoChatGatKatzeKotNekoKissaKediKakisGatosKucingGatzeGatzeCatGatto"

def create_jwt_token(data: dict , KEY = "GatoCatGattoChatGatKatzeKotNekoKissaKediKakisGatosKucingGatzeGatzeCatGatto"):
    expire = datetime.utcnow() + timedelta(minutes=600)  # Token válido por 10 horas
    payload = {
        **data,
        "exp": expire
    }
    token = jwt.encode(payload, KEY, algorithm="HS256")
    return token

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, "GatoCatGattoChatGatKatzeKotNekoKissaKediKakisGatosKucingGatzeGatzeCatGatto", algorithms=["HS256"])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")