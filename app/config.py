import os

from authx import AuthX, AuthXConfig


config = AuthXConfig(
    JWT_ALGORITHM=os.getenv('JWT_ALGORITHM', default='HS256'),
    JWT_SECRET_KEY=os.getenv(
        'JWT_SECRET_KEY', default='secret_key',
    ),
    JWT_TOKEN_LOCATION=['cookies'],
    JWT_COOKIE_CSRF_PROTECT=False
)

auth = AuthX(config=config)