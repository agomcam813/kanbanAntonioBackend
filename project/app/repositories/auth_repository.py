import json
import os

from app.core.redis.redis_client import r
from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import User
from app.utils.timer_helper import utc_now

REFRESH_TOKEN_TTL = int(os.getenv("REFRESH_TOKEN_TTL"))


class AuthRepository:
    @staticmethod
    async def create_user(user_data: dict) -> User:
        return await DatabaseModule.post_entity(User, user_data)

    @staticmethod
    async def get_user_by_email(email: str) -> User | None:
        return await DatabaseModule.get_entity_filtered(User, {"email": email})

    @staticmethod
    async def create_session(
        user_id: int, refresh_token: str, user_agent: str | None = None
    ) -> dict:
        """
        Guarda el refresh token en Redis como JSON, con TTL.
        """
        key = f"user:{user_id}:refresh_token:{refresh_token}"
        value = json.dumps(
            {"user_agent": user_agent, "created_at": utc_now().isoformat()}
        )
        r.set(key, value, ex=REFRESH_TOKEN_TTL)

        # Devuelve un dict con info de la sesión
        return {
            "user_id": user_id,
            "refresh_token": refresh_token,
            "user_agent": user_agent,
            "created_at": utc_now(),
        }

    @staticmethod
    async def get_session(user_id: int, refresh_token: str) -> dict | None:
        """
        Recupera la sesión desde Redis.
        Devuelve dict con metadata si existe, None si no.
        """
        key = f"user:{user_id}:refresh_token:{refresh_token}"
        data = r.get(key)
        if not data:
            return None
        return json.loads(data)

    @staticmethod
    async def delete_session(user_id: int, refresh_token: str) -> None:
        """
        Borra la sesión de Redis.
        """
        key = f"user:{user_id}:refresh_token:{refresh_token}"
        r.delete(key)
