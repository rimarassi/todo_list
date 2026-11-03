from datetime import datetime, timedelta, timezone

import jwt

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

security = HTTPBearer()

User = get_user_model()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenRequest(BaseModel):
    token: str


def create_token(user, token_type, expires_delta):
    payload = {
        'sub': str(user.pk),
        'type': token_type,
        'exp': datetime.now(timezone.utc) + expires_delta
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm='HS256'
    )


def decode_token(token, expected_type):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )

        if payload.get('type') != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Tipo de token inválido.'
            )

        return payload

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token inválido ou expirado.'
        )


@router.post('/login')
def login(data: LoginRequest):
    user = authenticate(
        username=data.username,
        password=data.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuário ou senha incorretos.'
        )

    access_token = create_token(
        user,
        'access',
        timedelta(hours=1)
    )

    refresh_token = create_token(
        user,
        'refresh',
        timedelta(days=7)
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }


@router.post('/refresh')
def refresh(data: TokenRequest):
    payload = decode_token(data.token, 'refresh')

    user = User.objects.filter(
        pk=payload['sub'],
        is_active=True
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuário não encontrado ou inativo.'
        )

    access_token = create_token(
        user,
        'access',
        timedelta(hours=1)
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }


@router.post('/verify')
def verify(data: TokenRequest):
    payload = decode_token(data.token, 'access')

    user = User.objects.filter(
        pk=payload['sub'],
        is_active=True
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuário não encontrado ou inativo.'
        )

    return {
        'valid': True,
        'user_id': user.pk,
        'username': user.get_username()
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    payload = decode_token(
        credentials.credentials,
        'access'
    )

    user = User.objects.filter(
        pk=payload['sub'],
        is_active=True
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuário não encontrado ou inativo.'
        )

    return user
