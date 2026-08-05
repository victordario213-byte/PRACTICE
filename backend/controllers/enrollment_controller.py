from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models.enrollment import Enrollment
from models.member import MemberProfile
from models.session import TrainingSession
from schemas.enrollment_schema import EnrollmentSchema
from .auth_utils import role_required

enrollment_schema = EnrollmentSchema()
enrollments_schema = EnrollmentSchema(many=True)

class EnrollmentListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        role = get_jwt().get("role")

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        if role == "member":
            member = MemberProfile.query.filter_by(user_id=user_id).first()
            if not member:
                return {"message": "Member profile not found."}, 404
            query = Enrollment.query.filter_by(member_id=member.id)
        else:
            query = Enrollment.query

        enrollments = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "enrollments": enrollments_schema.dump(enrollments.items),
            "page": enrollments.page,
            "per_page": enrollments.per_page,
            "total": enrollments.total,
        }, 200

    @jwt_required()
    @role_required("member")
    def post(self):
        payload = request.get_json() or {}
        errors = enrollment_schema.validate(payload)
        if errors:
            return {"message": "Invalid enrollment data.", "errors": errors}, 400

        member = MemberProfile.query.filter_by(user_id=get_jwt_identity()).first()
        if not member:
            return {"message": "Member profile not found."}, 404

        session = TrainingSession.query.get(payload.get("session_id"))
        if not session:
            return {"message": "Training session not found."}, 404

        if Enrollment.query.filter_by(member_id=member.id, session_id=session.id).first():
            return {"message": "Member is already enrolled in this session."}, 409

        enrollment = Enrollment(
            member_id=member.id,
            session_id=session.id,
            payment_status=payload.get("payment_status", "pending"),
            notes=payload.get("notes"),
        )
        db.session.add(enrollment)
        db.session.commit()

        return {"message": "Enrollment created successfully.", "enrollment": enrollment.to_dict()}, 201

class EnrollmentResource(Resource):
    @jwt_required()
    def get(self, enrollment_id):
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        return {"enrollment": enrollment.to_dict()}, 200

    @jwt_required()
    @role_required(["admin", "coach"])
    def put(self, enrollment_id):
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        payload = request.get_json() or {}

        if payload.get("attendance") is not None:
            enrollment.attendance = bool(payload["attendance"])
        if payload.get("fitness_score") is not None:
            enrollment.fitness_score = payload["fitness_score"]
        if payload.get("payment_status") is not None:
            enrollment.payment_status = payload["payment_status"]
        if payload.get("notes") is not None:
            enrollment.notes = payload["notes"]

        db.session.commit()
        return {"message": "Enrollment updated successfully.", "enrollment": enrollment.to_dict()}, 200

    @jwt_required()
    def delete(self, enrollment_id):
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        user_id = get_jwt_identity()
        role = get_jwt().get("role")

        if role == "member":
            member = MemberProfile.query.filter_by(user_id=user_id).first()
            if not member or member.id != enrollment.member_id:
                return {"message": "You can only cancel your own enrollment."}, 403

        db.session.delete(enrollment)
        db.session.commit()
        return {"message": "Enrollment deleted successfully."}, 200
