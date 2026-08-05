from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models.coach import CoachProfile
from models.member import MemberProfile
from models.team import Team
from models.enrollment import Enrollment
from models.session import TrainingSession
from schemas.coach_schema import CoachProfileSchema
from .auth_utils import role_required

coach_schema = CoachProfileSchema()
coaches_schema = CoachProfileSchema(many=True)

class CoachListResource(Resource):
    @jwt_required()
    @role_required("admin")
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        coaches = CoachProfile.query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "coaches": coaches_schema.dump(coaches.items),
            "page": coaches.page,
            "per_page": coaches.per_page,
            "total": coaches.total,
        }, 200

class CoachResource(Resource):
    @jwt_required()
    def get(self, coach_id):
        coach = CoachProfile.query.get_or_404(coach_id)
        role = get_jwt().get("role")
        user_id = get_jwt_identity()

        if role != "admin" and coach.user_id != user_id:
            return {"message": "Access denied."}, 403

        return {"coach": coach_schema.dump(coach)}, 200

    @jwt_required()
    def put(self, coach_id):
        coach = CoachProfile.query.get_or_404(coach_id)
        role = get_jwt().get("role")
        user_id = get_jwt_identity()

        if role != "admin" and coach.user_id != user_id:
            return {"message": "Access denied."}, 403

        payload = request.get_json() or {}
        if payload.get("full_name"):
            coach.full_name = payload["full_name"]
        if payload.get("phone") is not None:
            coach.phone = payload["phone"]
        if payload.get("specialization") is not None:
            coach.specialization = payload["specialization"]
        if payload.get("experience") is not None:
            coach.experience = payload["experience"]

        db.session.commit()
        return {"message": "Coach profile updated.", "coach": coach_schema.dump(coach)}, 200

    @jwt_required()
    @role_required("admin")
    def delete(self, coach_id):
        coach = CoachProfile.query.get_or_404(coach_id)
        db.session.delete(coach)
        db.session.commit()
        return {"message": "Coach profile deleted."}, 200

class CoachMembersResource(Resource):
    @jwt_required()
    @role_required("coach")
    def get(self):
        user_id = get_jwt_identity()
        coach = CoachProfile.query.filter_by(user_id=user_id).first()
        if not coach:
            return {"message": "Coach profile not found."}, 404

        members = (
            db.session.query(MemberProfile)
            .join(Enrollment, Enrollment.member_id == MemberProfile.id)
            .join(TrainingSession, TrainingSession.id == Enrollment.session_id)
            .join(Team, Team.id == TrainingSession.team_id)
            .filter(Team.coach_id == coach.id)
            .distinct()
            .all()
        )

        member_data = [
            {
                "id": member.id,
                "full_name": member.full_name,
                "phone": member.phone,
                "age": member.age,
                "gender": member.gender,
                "membership_type": member.membership_type,
            }
            for member in members
        ]

        return {"members": member_data}, 200
