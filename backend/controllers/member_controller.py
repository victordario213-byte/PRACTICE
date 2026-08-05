from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models.member import MemberProfile
from schemas.member_schema import MemberProfileSchema
from .auth_utils import role_required

member_schema = MemberProfileSchema()
members_schema = MemberProfileSchema(many=True)

class MemberListResource(Resource):
    @jwt_required()
    @role_required("admin")
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        members = MemberProfile.query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "members": members_schema.dump(members.items),
            "page": members.page,
            "per_page": members.per_page,
            "total": members.total,
        }, 200

    @jwt_required()
    @role_required("admin")
    def post(self):
        payload = request.get_json() or {}
        errors = member_schema.validate(payload)
        if errors:
            return {"message": "Invalid member profile data.", "errors": errors}, 400

        member = MemberProfile(
            user_id=payload["user_id"],
            full_name=payload["full_name"],
            phone=payload.get("phone"),
            age=payload.get("age"),
            gender=payload.get("gender"),
            membership_type=payload.get("membership_type", "Standard"),
        )
        db.session.add(member)
        db.session.commit()
        return {"message": "Member profile created.", "member": member_schema.dump(member)}, 201

class MemberResource(Resource):
    @jwt_required()
    def get(self, member_id):
        member = MemberProfile.query.get_or_404(member_id)
        role = get_jwt().get("role")
        user_id = get_jwt_identity()

        if role != "admin" and member.user_id != user_id:
            return {"message": "Access denied."}, 403

        return {"member": member_schema.dump(member)}, 200

    @jwt_required()
    def put(self, member_id):
        member = MemberProfile.query.get_or_404(member_id)
        role = get_jwt().get("role")
        user_id = get_jwt_identity()

        if role != "admin" and member.user_id != user_id:
            return {"message": "Access denied."}, 403

        payload = request.get_json() or {}
        if payload.get("full_name"):
            member.full_name = payload["full_name"]
        if payload.get("phone") is not None:
            member.phone = payload["phone"]
        if payload.get("age") is not None:
            member.age = payload["age"]
        if payload.get("gender") is not None:
            member.gender = payload["gender"]
        if payload.get("membership_type") is not None:
            member.membership_type = payload["membership_type"]

        db.session.commit()
        return {"message": "Member profile updated.", "member": member_schema.dump(member)}, 200

    @jwt_required()
    @role_required("admin")
    def delete(self, member_id):
        member = MemberProfile.query.get_or_404(member_id)
        db.session.delete(member)
        db.session.commit()
        return {"message": "Member profile deleted."}, 200
