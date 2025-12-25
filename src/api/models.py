from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    _password = db.Column(db.String(256), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_password):
        self._password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self._password, plain_password)

    def __repr__(self):
        return f"<User {self.email}>"

    def serialize(self):
        return {
            "email": self.email
        }
