import bcrypt

class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Transforma una contraseña plana en un hash seguro usando bcrypt puro."""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        return hashed_bytes.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Compara una contraseña ingresada con el hash guardado para el Login."""
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        return bcrypt.checkpw(plain_bytes, hashed_bytes)