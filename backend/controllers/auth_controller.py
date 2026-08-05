from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from extensions import db
from models.user import User
from models.member import MemberProfile
from models.coach import CoachProfile
from schemas.user_schema import UserSchema

user_schema = UserSchema()

class RegisterResource(Resource):
    def post(self):
        payload = request.get_json() or {}
        errors = user_schema.validate(payload)
        if errors:
            return {"message": "Invalid registration data.", "errors": errors}, 400

        if User.query.filter((User.username == payload.get("username")) | (User.email == payload.get("email"))).first():
            return {"message": "Username or email already exists."}, 409

        user = User(
            username=payload["username"],
            email=payload["email"],
            role=payload.get("role", "member"),
        )
        user.set_password(payload["password"])
        db.session.add(user)
        db.session.flush()

        role = payload.get("role", "member")
        if role == "member":
            profile = MemberProfile(
                user_id=user.id,
                full_name=payload.get("full_name", payload["username"]),
                phone=payload.get("phone"),
                age=payload.get("age"),
                gender=payload.get("gender"),
                membership_type=payload.get("membership_type", "Standard"),
            )
            db.session.add(profile)
        elif role == "coach":
            profile = CoachProfile(
                user_id=user.id,
                full_name=payload.get("full_name", payload["username"]),
                phone=payload.get("phone"),
                specialization=payload.get("specialization", "General"),
                experience=payload.get("experience", 0),
            )
            db.session.add(profile)

        db.session.commit()
        return {"message": "User registered successfully.", "user": user.to_dict()}, 201

class LoginResource(Resource):
    def post(self):
        payload = request.get_json() or {}
        username = payload.get("username")
        password = payload.get("password")

        if not username or not password:
            return {"message": "Username and password are required."}, 400

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {"message": "Invalid credentials."}, 401

        access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
        return {
            "message": "Login successful.",
            "access_token": access_token,
            "user": user.to_dict(),
        }, 200
