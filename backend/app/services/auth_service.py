from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from app.core.result import Result
from app.core.logger import logger
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schema import LoginRequest, LoginResponse
import hashlib


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Business logic for login and authentication.
    """

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def hash_password(self, password: str) -> str:
        sha256_hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return pwd_context.hash(sha256_hashed)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        sha256_hashed = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return pwd_context.verify(sha256_hashed, hashed_password)

    async def login(self, payload: LoginRequest) -> Result:
        try:
            res = await self.repo.get_users_by_username(payload.user_name)
            if not res.success or not res.data:
                return Result.Fail("Invalid username or password", code=401)

            matched_user = None
            for user in res.data:
                if self.verify_password(payload.password, user.password_hash):
                    matched_user = user
                    break

            if not matched_user:
                return Result.Fail("Invalid username or password", code=401)

            login_time = datetime.now()
            await self.repo.save_login_log(matched_user.user_id, login_time)

            response = LoginResponse(
                bio_id=matched_user.bio_id,
                user_name=matched_user.user_name,
                login_time=login_time
            )
            return Result.Ok(response.dict(), message="Login successful", code=200)

        except SQLAlchemyError:
            logger.exception("Database error during login.")
            return Result.Fail("Database error during login", code=500)
        except Exception as e:
            logger.exception(str(e))
            return Result.Fail(str(e), code=500)

