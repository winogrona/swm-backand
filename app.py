import hashlib
import random

from datetime import datetime, timedelta

from flask import Flask # type: ignore
from dataclasses import dataclass
from flask import request

from http import HTTPStatus

from config import config
from db import session as db, Products, Category, Materials

from enum import Enum

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

@app.route("/getProducts", methods=["GET"])
def get_products():
    products = db.query(Products).all()
    products_list = [product.__todict__() for product in products]
    response = Response(
        status=HTTPStatus.OK,
        data={
            "products": products_list
        }
    )
    return response.to_dict(), 200

@app.route("/getStatistick", methods=["GET"])
def get_statistick():
    statistics = {
        "total__recycled_products": 100,
        "total_categories": 10,
        "total_materials": 50,
        "most_popular_product": "Plastic Bottle"
    }
    response = Response(
        status=HTTPStatus.OK,
        data=statistics
    )
    return response.to_dict(), 200


if __name__ == '__main__':
    app.run()