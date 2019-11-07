from functools import wraps

from flask import current_app, request


def get_logger():
    return current_app.logger


def debug(msg, *args, **kwargs):
    get_logger().debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    get_logger().info(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    get_logger().warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    get_logger().error(msg, *args, **kwargs)


def log_request_response(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            info(request.url + " " + str(request.json))
        except RuntimeError:
            error("Error logging request")

        response = function(*args, **kwargs)
        try:
            info(response.status + " " + str(response.json))
        except RuntimeError:
            error("Error logging response")

        return response
    return wrapper
