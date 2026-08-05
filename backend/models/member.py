from extensions import db

class MemberProfile(db.Model):
    __tablename__ = "member_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    membership_type = db.Column(db.String(50), nullable=True)

    user = db.relationship("User", back_populates="member_profile")
    enrollments = db.relationship("Enrollment", back_populates="member", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "phone": self.phone,
            "age": self.age,
            "gender": self.gender,
            "membership_type": self.membership_type,
        }
