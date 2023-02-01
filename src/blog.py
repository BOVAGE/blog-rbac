from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from .models import Post, Organization
from . import db
from .decorators import create_post_check, edit_post_check, delete_post_check
from . import permify

blog = Blueprint("views", __name__)


@blog.get("/")
def status():
    return jsonify({"status": "Up and running"}), 200


@blog.post("/organizations/<int:organ_id>/posts")
@login_required
@create_post_check
def create_post(organ_id):
    print("type of organ_id ", organ_id)
    organization = Organization.query.get(organ_id)
    print("type of organ_id ", organ_id)
    if organization is None:
        return (
            jsonify(
                {"status": "ERROR", "message": "Organization not found", "data": None}
            ),
            404,
        )
    data = request.json
    title = data.get("title")
    content = data.get("content")
    author_id = current_user.id
    post = Post(
        title=title,
        content=content,
        author_id=author_id,
        organization_id=organ_id,
    )
    db.session.add(post)
    db.session.commit()
    # create authorization data in permify
    snap_token_1 = permify.create_relational_tuple(
        {
            "type": "post",
            "id": str(post.id),  # id of the newly created post in our db
        },
        "author",
        {"type": "user", "id": str(post.author_id), "relation": ""},
    )
    snap_token_2 = permify.create_relational_tuple(
        {
            "type": "post",
            "id": str(post.id),  # id of the newly created post in our db
        },
        "organization",
        {"type": "organization", "id": str(post.organization_id), "relation": "..."},
    )
    return (
        jsonify(
            {
                "status": "SUCCESS",
                "message": f"Post created successfully",
                "data": {
                    "id": post.id,
                    "title": post.title,
                    "date_created": post.date_created,
                    "content": post.content,
                    "author": post.author_id,
                    "organization": post.organization_id,
                },
            }
        ),
        201,
    )


@edit_post_check
@delete_post_check
@blog.route("/posts/<int:post_id>", methods=["GET", "PUT", "DELETE"])
def post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return (
            jsonify({"status": "ERROR", "message": "Post not found", "data": None}),
            404,
        )
    if request.method == "GET":
        return (
            jsonify(
                {
                    "status": "SUCCESS",
                    "message": f"Post with id: {post_id} retrieved successfully",
                    "data": {
                        "id": post.id,
                        "title": post.title,
                        "date_created": post.date_created,
                        "content": post.content,
                        "author": post.author_id,
                        "organization": post.organization_id,
                    },
                }
            ),
            200,
        )
    elif request.method == "PUT":
        data = request.json
        post.title = data.get("title")
        post.date_created = data.get("date_created")
        post.content = data.get("content")
        post.author_id = data.get("author_id")
        post.organization_id = data.get("organization_id")
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "SUCCESS",
                    "message": f"Post with id: {post_id} updated successfully",
                    "data": {
                        "id": post.id,
                        "title": post.title,
                        "date_created": post.date_created,
                        "content": post.content,
                        "author": post.author_id,
                        "organization": post.organization_id,
                    },
                }
            ),
            200,
        )
    elif request.method == "DELETE":
        db.session.delete(post)
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "SUCCESS",
                    "message": f"Post with id: {post_id} retrieved successfully",
                    "data": None,
                }
            ),
            200,
        )
    return jsonify({"status": "Up and running"}), 200
