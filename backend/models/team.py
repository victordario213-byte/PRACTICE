from extensions import db

class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey("coach_profiles.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    sport = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)

    coach = db.relationship("CoachProfile", back_populates="teams")
    sessions = db.relationship("TrainingSession", back_populates="team", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "coach_id": self.coach_id,
            "name": self.name,
            "sport": self.sport,
            "description": self.description,
        }
