from extensions import db

class CoachProfile(db.Model):
    __tablename__ = "coach_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    specialization = db.Column(db.String(120), nullable=True)
    experience = db.Column(db.Integer, nullable=True)

    user = db.relationship("User", back_populates="coach_profile")
    teams = db.relationship("Team", back_populates="coach", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "phone": self.phone,
            "specialization": self.specialization,
            "experience": self.experience,
        }
