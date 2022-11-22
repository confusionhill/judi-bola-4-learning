import bcrypt
from services.authentication.authHandler import config


class AuthService:
    secret_pass = config["HASH-PASS"]

    def hash_password(self, password) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

    def validate_password(self, password, hashed) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


authService = AuthService();
