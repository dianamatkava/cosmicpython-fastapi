from werkzeug.security import generate_password_hash

from auth.models import User
from extensions import db


def create_admin(email: str, pwd: str):
    try:
        admin = User(
            email=email,
            password=generate_password_hash(pwd)
        )
        db.session.add(admin)
        db.session.commit()
    except Exception as _ex:
        print(_ex)

# from auth.util.create_admin import create_admin as ad
# ad(email='admin@admin', pwd='admin')