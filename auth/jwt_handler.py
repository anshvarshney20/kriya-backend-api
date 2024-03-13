# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict
from auth.database import users_collection
import jwt
from decouple import config
from auth.security import hash_password

JWT_SECRET = '7fca8e96c31b381f278f0e3979651421f6678de210ac5c1c53b8ab7d856fa54f928b83d6d96522a12d638a022a1d1ebf6473de397792165cebd3064add6c65d92d2ffe833f4f12aec8930e5bbb2aceef34d3a040838081d6cb48b14e179e804c91371e59e61812c58a7d94f90008fa8b6b3d2f6a821fe127235202d5703e5f689b141bee0bca1e477652696d634a85ec766cb0f54bee4f7ae2c9895633cf19abe6f165818e56b922b2b482f5fe23778a7d224850404b9ac7b7847a4d4fc914cb1cce2e860eb6244fdaa37ac9097aeeb3bb6809a52460d0e90f00d04a687c7c165d5de0646242dca135cebaf0300cad3efb54985bc1571887969f53ffe2bd592b'
JWT_ALGORITHM = 'HS256'


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    # Adding 24 hours' worth of seconds (24 * 60 * 60)
    expiration_time = time.time() + (24 * 60 * 60)
    payload = {
        "user_id": user_id,
        "expires": expiration_time
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token
        else:
            raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.ExpiredSignatureError:
        # Handle token expiration error
        raise
    except jwt.InvalidTokenError:
        # Handle other token validation errors
        raise
    except Exception as e:
        # Handle unexpected errors
        raise RuntimeError("Failed to decode JWT: {}".format(e))
