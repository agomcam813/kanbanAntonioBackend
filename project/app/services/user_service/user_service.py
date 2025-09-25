from app.core.supabase.supabase_client import get_supabase_admin
from app.modules.database_module.models.default import User
from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserOutputSchema, UserUpdateSchema
from app.services.user_service.user_service_exception import (
    UserServiceException,
    UserServiceExceptionInfo,
)


class UserService:
    @staticmethod
    async def get_user_by_email(email: str) -> UserOutputSchema:
        # Fetch user by email from the local database
        user = await UserRepository.get_user_by_email(email)
        if not user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)
        # Return user data as a schema instance
        return UserOutputSchema(**user.__dict__)

    @staticmethod
    async def get_user_by_email_model(email: str) -> User:
        # Fetch user by email from the local database
        user = await UserRepository.get_user_by_email(email)
        if not user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)
        # Return user data as a schema instance
        return user

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserOutputSchema:
        # Fetch user by ID from the local database
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)
        # Return user data as a schema instance
        return UserOutputSchema(**user.__dict__)

    @staticmethod
    async def update_user(user_id: int, data: UserUpdateSchema) -> UserOutputSchema:
        # Update user fields in the local database
        user = await UserRepository.update_user(user_id, data.model_dump())
        if not user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)
        # Return the updated user as a schema instance
        return UserOutputSchema(**user.__dict__)

    @staticmethod
    async def delete_user(sub: str, email: str) -> UserOutputSchema:
        user = await UserRepository.get_user_by_email(email)
        if not user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)

        await AuthRepository.delete_all_sessions(user.id)

        supabase = await get_supabase_admin()
        try:
            await supabase.auth.admin.delete_user(sub)
        except Exception:
            raise UserServiceException(
                UserServiceExceptionInfo.ERROR_DELETING_USER_SUPABASE
            )

        deleted_user = await UserRepository.delete_user(user.id)
        if not deleted_user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)

        return UserOutputSchema(**deleted_user.__dict__)
