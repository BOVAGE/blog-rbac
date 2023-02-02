from flask_login import current_user
from flask import request
from functools import wraps
from . import permify
from flask import abort

def create_post_check(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # call permify func to check for permission
        can = permify.check_permission(
            {"type": "organization", "id": str(kwargs.get("organ_id"))},
            "create_post",
            {"type": "user", "id": str(current_user.id), "relation": ""},
        )
        if can == "RESULT_ALLOWED":
            return view_func(*args, **kwargs)
        return abort(403)

    return wrapper


def delete_post_check(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # due to the route chaining used in the views
        # we need to distinguish between each request
        # so a delete action access check won't impair the edit access
        # check
        if request.method == "DELETE":
            # call permify func to check for permission
            can = permify.check_permission(
                {"type": "post", "id": str(kwargs.get("post_id"))},
                "delete",
                {"type": "user", "id": str(current_user.id), "relation": ""},
            )
            if can == "RESULT_ALLOWED":
                return view_func(*args, **kwargs)
            return abort(403)
        return view_func(*args, **kwargs)

    return wrapper


def edit_post_check(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if request.method == "PUT":
            # call permify func to check for permission
            can = permify.check_permission(
                {"type": "post", "id": str(kwargs.get("post_id"))},
                "edit",
                {"type": "user", "id": str(current_user.id), "relation": ""},
            )
            if can == "RESULT_ALLOWED":
                return view_func(*args, **kwargs)
            return abort(403)
        return view_func(*args, **kwargs)
    return wrapper
