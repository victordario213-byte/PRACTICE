from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models.team import Team
from models.coach import CoachProfile
from schemas.team_schema import TeamSchema
from .auth_utils import role_required

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)

class TeamListResource(Resource):
    @jwt_required()
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        teams = Team.query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "teams": teams_schema.dump(teams.items),
            "page": teams.page,
            "per_page": teams.per_page,
            "total": teams.total,
        }, 200

    @jwt_required()
    @role_required(["admin", "coach"])
    def post(self):
        payload = request.get_json() or {}
        errors = team_schema.validate(payload)
        if errors:
            return {"message": "Invalid team data.", "errors": errors}, 400

        user_id = get_jwt_identity()
        role = get_jwt().get("role")

        if role == "coach":
            coach = CoachProfile.query.filter_by(user_id=user_id).first()
            if not coach:
                return {"message": "Coach profile not found."}, 404
            coach_id = coach.id
        else:
            coach_id = payload.get("coach_id")
            if not coach_id:
                return {"message": "coach_id is required for admin-created teams."}, 400

        team = Team(
            coach_id=coach_id,
            name=payload["name"],
            sport=payload["sport"],
            description=payload.get("description"),
        )
        db.session.add(team)
        db.session.commit()

        return {"message": "Team created successfully.", "team": team.to_dict()}, 201

class TeamResource(Resource):
    @jwt_required()
    def get(self, team_id):
        team = Team.query.get_or_404(team_id)
        return {"team": team.to_dict()}, 200

    @jwt_required()
    @role_required(["admin", "coach"])
    def put(self, team_id):
        team = Team.query.get_or_404(team_id)
        user_id = get_jwt_identity()
        role = get_jwt().get("role")

        if role == "coach":
            coach = CoachProfile.query.filter_by(user_id=user_id).first()
            if not coach or coach.id != team.coach_id:
                return {"message": "You can only update your own teams."}, 403

        payload = request.get_json() or {}
        if payload.get("name"):
            team.name = payload["name"]
        if payload.get("sport"):
            team.sport = payload["sport"]
        if payload.get("description") is not None:
            team.description = payload["description"]
        db.session.commit()

        return {"message": "Team updated successfully.", "team": team.to_dict()}, 200

    @jwt_required()
    @role_required(["admin", "coach"])
    def delete(self, team_id):
        team = Team.query.get_or_404(team_id)
        user_id = get_jwt_identity()
        role = get_jwt().get("role")

        if role == "coach":
            coach = CoachProfile.query.filter_by(user_id=user_id).first()
            if not coach or coach.id != team.coach_id:
                return {"message": "You can only delete your own teams."}, 403

        db.session.delete(team)
        db.session.commit()
        return {"message": "Team deleted successfully."}, 200
