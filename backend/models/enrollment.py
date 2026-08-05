from datetime import datetime
from extensions import db

class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member_profiles.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("training_sessions.id"), nullable=False)
    attendance = db.Column(db.Boolean, default=False)
    fitness_score = db.Column(db.Integer, nullable=True)
    payment_status = db.Column(db.String(50), nullable=True, default="pending")
    enrollment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)

    member = db.relationship("MemberProfile", back_populates="enrollments")
    session = db.relationship("TrainingSession", back_populates="enrollments")

    def to_dict(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "session_id": self.session_id,
            "attendance": self.attendance,
            "fitness_score": self.fitness_score,
            "payment_status": self.payment_status,
            "enrollment_date": self.enrollment_date.isoformat(),
            "notes": self.notes,
        }
