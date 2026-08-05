from extensions import db

class TrainingSession(db.Model):
    __tablename__ = "training_sessions"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(120), nullable=True)
    capacity = db.Column(db.Integer, nullable=False, default=20)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    team = db.relationship("Team", back_populates="sessions")
    enrollments = db.relationship("Enrollment", back_populates="session", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "team_id": self.team_id,
            "title": self.title,
            "date": self.date.isoformat() if self.date else None,
            "location": self.location,
            "capacity": self.capacity,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }
