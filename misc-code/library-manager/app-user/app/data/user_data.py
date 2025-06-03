from app.models.user_orm import User


def add_user(db_session, first_name, last_name):
    """
    Add user to the database
    """
    user = User(first_name=first_name, last_name=last_name)
    db_session.add(user)
    return user