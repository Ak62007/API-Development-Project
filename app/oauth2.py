from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# SECRET KEY - THIS WILL BE KEPT IN THE SERVER.
# ALGORITHM
# EXPIRATION TIME - MAX TIME FOR THE TOKEN TO BE VALID

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TIME = settings.access_time_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TIME)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def verify_access_token(token: str, credencial_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        
        if id is None:
            raise credencial_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credencial_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credencial_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate the credentials", headers={"WWW-Authenticate":"Bearer"})
    
    token_data = verify_access_token(token=token, credencial_exception=credencial_exception)
    current_user = db.query(models.Users).filter(models.Users.id == token_data.id).first()
    
    return current_user
    