from app.db.database import session_factory
from app.db.models import User
from typing import Optional, List


def add_user(name: str, email: str):
    with session_factory() as session:
        user = User(
            name=name,
            email=email
        )
        session.add(user)
        session.commit()
        
        
def get_user_by_id(id: int):
    with session_factory() as session:
        user = session.query(User).filter(User.id == id).first()
    return user


def get_all_users():
    with session_factory() as session:
        users = session.query(User).all()
    return users


def update_user(id: int, new_name: Optional[str]=None, new_email: Optional[str]=None):
    user = get_user_by_id(id)
    if new_name:
        user.name = new_name
    if new_email:
        user.email = new_email
    with session_factory() as session:
        session.add(user)
        session.commit()
        
    
def detele_user(id: int):
    user = get_user_by_id(id)
    with session_factory() as session:
        session.delete(user)
        session.commit()