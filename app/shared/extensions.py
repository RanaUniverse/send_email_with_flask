"""
app/shared/extensions.py

This is here i will keep flask-related extra things
"""

from flask_login import LoginManager  # type: ignore


from app.features.identity.operations import get_user_by_id

login_manager = LoginManager()


@login_manager.user_loader  # type: ignore
def load_user(user_id: str):
    """
    As per flask-login docs i need this which will get the value of the
    user_obj from the user_id stored in the session in encrypted way
    """
    obj = get_user_by_id(
        user_id=user_id,
    )
    return obj
