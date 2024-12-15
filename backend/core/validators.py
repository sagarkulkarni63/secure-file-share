from rest_framework.exceptions import ValidationError

def validate_username(username: str):
    if len(username) < 3:
        raise ValidationError("Username too short.")
    if " " in username:
        raise ValidationError("Username must not contain spaces.")
    return username

def validate_password(password: str):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters.")
    return password
