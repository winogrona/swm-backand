import hashlib
import random

from datetime import datetime, timedelta

from flask import Flask # type: ignore
from dataclasses import dataclass
from flask import request

from http import HTTPStatus

from config import config
from db import session as db, User, Token

# We are not responsible for any psychological harm
# induced by reviewing this code.

# heeey saefjwehfhwe

class Response:
    status: int
    message: str
    data: dict

    def __init__(self, status: HTTPStatus, data: dict, message: str | None = None):
        self.status = status.value

        if message is None:
            self.message = status.phrase
        else:
            self.message = message

        self.data = data

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }

app = Flask(__name__)

@app.route("/register", methods=["GET"])
def register():
    username = request.args.get("username")
    password = request.args.get("password")

    if username is None or password is None:
        response = Response(
            status=HTTPStatus.BAD_REQUEST,
            data={}
        )
        return response.to_dict(), 400

    salt = random.randbytes(16).hex()
    password_hash = hashlib.sha256((salt + password).encode()).hexdigest()

    user = User(
        username=username,
        password_hash=password_hash,
        salt=salt,
        created_at=datetime.now()
    )
    db.add(user)
    db.commit()

    response = Response(
        status=HTTPStatus.OK,
        data={
            "user_id": user.id
        }
    )
    return response.to_dict(), 200

@app.route("/authorize", methods=["GET"])
def authorize(): # args: username: String, password: String
    username = request.args.get("username")
    password = request.args.get("password")

    if username is None or password is None:
        response = Response(
            status=HTTPStatus.BAD_REQUEST,
            data={}
        )
        return response.to_dict(), 400
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        response = Response(
            status=HTTPStatus.NOT_FOUND,
            data={}
        )
        return response.to_dict(), 404
    
    password_hash = hashlib.sha256((user.salt + password).encode()).hexdigest()
    if password_hash != user.password_hash:
        response = Response(
            status=HTTPStatus.UNAUTHORIZED,
            data={}
        )
        return response.to_dict(), 401
    
    token = Token(
        id=user.id,
        user_id=user.id,
        token=random.randbytes(32).hex(),
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(seconds=config["user"]["token_expiration"])
    )
    db.add(token)
    db.commit()
    
    response = Response(
        status=HTTPStatus.OK,
        data={
            "token": token.token,
            "expires_at": token.expires_at.isoformat()
        }
    )
    return response.to_dict(), 200

if __name__ == '__main__':
    app.run()