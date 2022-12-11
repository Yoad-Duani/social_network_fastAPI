from fastapi.exceptions import RequestValidationError, ValidationError
from pydantic import BaseModel, validator

def validator_password(password: str) -> str:
    if password != None:
        special_characters = "[~\!@#\$%\^&\*\(\)_\+\":;'\[\]]}{"
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain at least 1 digit.')
        if not any(char.isalpha() for char in password):
            raise ValueError('Password must contain at least 1 letter.')
        if not any(char in special_characters for char in password):
            raise ValueError('Password must contain at least 1 special character.')
    return password