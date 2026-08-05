from datetime import date, time
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models.session import TrainingSession
from models.team import Team
from models.coach import CoachProfile
from schemas.session_schema import TrainingSessionSchema
from .auth_utils import role_required

session_schema = TrainingSessionSchema()
sessions_schema = TrainingSessionSchema(many=True)

class SessionListResource(Resource):
    @jwt_required()
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        sessions = TrainingSession.query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "sessions": sessions_schema.dump(sessions.items),
            "page": sessions.page,
            "per_page": sessions.per_page,
            "total": sessions.total,
        }, 200

    @jwt_required()
    @role_required(["admin", "coach"])
    def post(self):
        payload = request.get_json() or {}
        errors = session_schema.validate(payload)
        if errors:
            return {"message": "Invalid session data.", "errors": errors}, 400

        team_id = payload.get("team_id")
        team = Team.query.get(team_id)
        if not team:
            return {"message": "Team not found."}, 404

        user_id = get_jwt_identity()
        role = get_jwt().get("role")

        if role == "coach":
            coach = CoachProfile.query.filter_by(user_id=user_id).first()
            if not coach or coach.id != team.coach_id:
                return {"message": "Coaches may only create sessions for their own teams."}, 403

        try:
            session_date = date.fromisoformat(payload["date"])
            start_time = time.fromisoformat(payload["start_time"])
            end_time = time.fromisoformat(payload["end_time"])
        except (KeyError, ValueError):
            return {"message": "Date and time fields must be ISO-formatted."}, 400

        training_session = TrainingSession(
            team_id=team_id,
            title=payload["title"],
            date=session_date,
            location=payload.get("location"),
            capacity=payload.get("capacity", 20),
            start_time=start_time,
            end_time=end_time,
        )
        db.session.add(training_session)
        db.session.commit()

        return {"message": "Training session created successfully.", "session": training_session.to_dict()}, 201

class SessionResource(Resource):
    @jwt_required()
    def get(self, session_id):
        training_session = TrainingSession.query.get_or_404(session_id)
        return {"session": training_session.to_dict()}, 200

    @jwt_required()
    @role_required(["admin", "coach"])
    def put(self, session_id):
        training_session = TrainingSession.query.get_or_404(session_id)
        user_id = get_jwt_identity()
        role = get_jwt().get("role")

        if role == "coach":
            coach = CoachProfile.query.filter_by(user_id=user_id).first()
            if not coach or coach.id != training_session.team.coach_id:
                return {"message": "Coaches may only update sessions owned by their teams."}, 403

        payload = request.get_json() or {}
        if payload.get("title"):
            training_session.title = payload["title"]
        if payload.get("location") is not None:
            training_session.location = payload["location"]
        if payload.get("capacity") is not None:
            training_session.capacity = payload["capacity"]
        if payload.get("date"):
            try:
                training_session.date = date.fromisoformat(payload["date"])
            except ValueError:
                return {"message": "The date must be ISO-formatted."}, 400
        if payload.get("start_time"):
            try:
                training_session.start_time = time.fromisoformat(payload["start_time"])
            except ValueError:
                return {"message": "The start_time must be ISO-formatted."}, 400
        if payload.get("end_time"):
            try:
                training_session.end_time = time.fromisoformat(payload["end_time"])
            except ValueError:
                return {"message": "The end_time must be ISO-formatted."}, 400

        db.session.commit()
        return {"message": "Session updated successfully.", "session": training_session.to_dict()}, 200

    @jwt_required()
    @role_required(["admin", "coach"])
    def delete(self, session_id):
        training_session = TrainingSession.query.get_or_404(session_id)
        user_id = get_jwt_identity()
        role = get_jwt().get("role")

        if role == "coach":
            coach = CoachProfile.query.filter_by(user_id=user_id).first()
            if not coach or coach.id != training_session.team.coach_id:
                return {"message": "Coaches may only delete sessions owned by their teams."}, 403

        db.session.delete(training_session)
        db.session.commit()
        return {"message": "Training session deleted successfully."}, 200
