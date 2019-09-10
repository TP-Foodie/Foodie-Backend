from flask import jsonify
from marshmallow import ValidationError


def validation_error_handler(e):
    return jsonify(e.messages), 400


def error_handler(e):
    return "Internal error", 500


exception_handler = {
    Exception: error_handler,
    ValidationError: validation_error_handler
}

