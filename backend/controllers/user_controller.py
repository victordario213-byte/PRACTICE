from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from extensions import db
from models.user import User
from schemas.user_schema import UserSchema
from .auth_utils import role_required

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserListResource(Resource):
    @jwt_required()
    @role_required("admin")
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        users = User.query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "users": users_schema.dump(users.items),
            "page": users.page,
            "per_page": users.per_page,
            "total": users.total,
        }, 200

    @jwt_required()
    @role_required("admin")
    def post(self):
        payload = request.get_json() or {}
        errors = user_schema.validate(payload)
        if errors:
            return {"message": "Invalid user data.", "errors": errors}, 400

        if User.query.filter((User.username == payload.get("username")) | (User.email == payload.get("email"))).first():
            return {"message": "Username or email already exists."}, 409

        user = User(
            username=payload["username"],
            email=payload["email"],
            role=payload.get("role", "member"),
        )
        user.set_password(payload["password"])
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully.", "user": user.to_dict()}, 201

class UserResource(Resource):
    @jwt_required()
    @role_required("admin")
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {"user": user.to_dict()}, 200

    @jwt_required()
    @role_required("admin")
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        payload = request.get_json() or {}

        if payload.get("username"):
            user.username = payload["username"]
        if payload.get("email"):
            user.email = payload["email"]
        if payload.get("role"):
            user.role = payload["role"]
        if payload.get("password"):
            user.set_password(payload["password"])

        db.session.commit()
        return {"message": "User updated successfully.", "user": user.to_dict()}, 200

    @jwt_required()
    @role_required("admin")
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully."}, 200
