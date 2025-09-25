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
        """
        Get a user by their email address.

        Retrieves a user object from the database using their email address.

        Parameters:
        - email: Email address of the user to retrieve

        Returns:
        - User object if found, or None if not found
        """
        return await DatabaseModule.get_entity_filtered(User, {"email": email})

    @staticmethod
    async def create_session(
        user_id: int, refresh_token: str, user_agent: str | None = None
    ) -> dict:
        """
        Create a new session in Redis.

        Parameters:
        - user_id: ID of the user associated with the session
        - refresh_token: Refresh token associated with the session
        - user_agent: User agent string associated with the session (optional)

        Returns:
        - Session data as a dictionary
        """
        key = f"user:{user_id}:refresh_token:{refresh_token}"
        value = json.dumps(
            {"user_agent": user_agent, "created_at": utc_now().isoformat()}
        )
        r.set(key, value, ex=REFRESH_TOKEN_TTL)

        return {
            "user_id": user_id,
            "refresh_token": refresh_token,
            "user_agent": user_agent,
            "created_at": utc_now(),
        }

    @staticmethod
    async def get_session(user_id: int, refresh_token: str) -> dict | None:
        """
        Get session data from Redis.

        Parameters:
        - user_id: ID of the user associated with the session
        - refresh_token: Refresh token associated with the session

        Returns:
        - Session data as a dictionary if the session exists, or None if it doesn't
        """
        key = f"user:{user_id}:refresh_token:{refresh_token}"
        data = r.get(key)
        if not data:
            return None
        return json.loads(data)

    @staticmethod
    async def delete_session(user_id: int, refresh_token: str) -> None:
        """
        delete session in redis.
        """
        key = f"user:{user_id}:refresh_token:{refresh_token}"
        r.delete(key)

    @staticmethod
    async def delete_all_sessions(user_id: int) -> None:
        """
        delete all user session
        """

        pattern = f"user:{user_id}:refresh_token:*"
        keys = r.keys(pattern)

        if keys:
            r.delete(*keys)
