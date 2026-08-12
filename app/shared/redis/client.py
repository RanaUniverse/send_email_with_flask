"""
app/shared/redis/client.py

Here i will make the client obj to use in many places

i will import this obj in differnet places this will just nothing do else
"""

import redis


from app.config import settings

if settings.redis.password:
    password_value = settings.redis.password.get_secret_value()
else:
    password_value = None


id_pass_credential_obj = redis.UsernamePasswordCredentialProvider(
    username=settings.redis.username,
    password=password_value,
)

redis_client = redis.Redis(
    host=settings.redis.host,
    db=settings.redis.db,
    port=settings.redis.port,
    decode_responses=True,
    credential_provider=id_pass_credential_obj,
)
