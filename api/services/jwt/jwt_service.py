from jose import jwt
from api.services.jwt.constant import ALGORITHM, SECRET_KEY

def jwt_encode_data(data):    
    # to_encode = data.copy()
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 

def jwt_decode_data(token):
    decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_sub": False}) 
    return decoded_jwt


