from flask import session


def validate_user(username: str, psw: str) -> bool:
    # Define method to access db and verify user
    session["logged_in_user"] = username
    return True
