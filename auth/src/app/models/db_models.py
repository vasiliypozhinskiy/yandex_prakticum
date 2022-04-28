import uuid
from datetime import datetime

from app.core import db
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)

    email = db.Column(db.String, unique=True, index=True)

    first_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    history_entries = db.relationship("LoginHistory", backref="user")
    roles = db.relationship(
        "Role", secondary="users_roles", backref=db.backref("users", lazy="dynamic")
    )

    def __repr__(self):
        return f"<User: {self.login}>"


class LoginHistory(db.Model):
    __tablename__ = "login_history"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_agent = db.Column(db.String)
    refresh_token = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(User.id))

    def __repr__(self):
        return f"<LoginHistory: {self.user_id} {self.created_at}>"


class Role(db.Model):
    __tablename__ = "roles"

    title = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)

    def __repr__(self):
        return f"<Role: {self.title}>"


users_roles = db.Table(
    "users_roles",
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("users.id")),
    db.Column("role_id", db.String, db.ForeignKey("roles.title")),
)
