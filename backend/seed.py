import random
from datetime import datetime, timedelta, date, time
from main import create_app
from extensions import db
from models.user import User
from models.coach import CoachProfile
from models.member import MemberProfile
from models.team import Team
from models.session import TrainingSession
from models.enrollment import Enrollment
from models.notification import Notification

COACHES = [
    {"name": "Amina Hassan", "specialization": "Football", "experience": 8},
    {"name": "Daniel Osei", "specialization": "Basketball", "experience": 6},
    {"name": "Fatima Ali", "specialization": "Tennis", "experience": 10},
    {"name": "Lucas Mwangi", "specialization": "Swimming", "experience": 5},
    {"name": "Chloe Carter", "specialization": "Athletics", "experience": 7},
    {"name": "Mohamed Kamau", "specialization": "Volleyball", "experience": 6},
    {"name": "Sara Johnson", "specialization": "Gymnastics", "experience": 9},
    {"name": "Kwame Adu", "specialization": "Rugby", "experience": 7},
    {"name": "Lina Perez", "specialization": "Badminton", "experience": 4},
    {"name": "Diego Silva", "specialization": "Cricket", "experience": 8},
]

MEMBERS = [
    {"name": "Elijah Brown", "age": 22, "gender": "Male"},
    {"name": "Maya Patel", "age": 25, "gender": "Female"},
    {"name": "Noah Smith", "age": 20, "gender": "Male"},
    {"name": "Ava Lee", "age": 19, "gender": "Female"},
    {"name": "Liam Johnson", "age": 24, "gender": "Male"},
    {"name": "Sophia Kim", "age": 23, "gender": "Female"},
    {"name": "Ethan Nguyen", "age": 21, "gender": "Male"},
    {"name": "Olivia Green", "age": 26, "gender": "Female"},
    {"name": "Mason Torres", "age": 28, "gender": "Male"},
    {"name": "Chloe Martin", "age": 27, "gender": "Female"},
    {"name": "Aiden White", "age": 24, "gender": "Male"},
    {"name": "Isabella Walker", "age": 22, "gender": "Female"},
    {"name": "Lucas Lopez", "age": 29, "gender": "Male"},
    {"name": "Amelia Hall", "age": 20, "gender": "Female"},
    {"name": "Jacob Young", "age": 25, "gender": "Male"},
    {"name": "Harper King", "age": 21, "gender": "Female"},
    {"name": "Michael Adams", "age": 23, "gender": "Male"},
    {"name": "Avery Scott", "age": 22, "gender": "Female"},
    {"name": "William Nguyen", "age": 26, "gender": "Male"},
    {"name": "Grace Clark", "age": 24, "gender": "Female"},
    {"name": "James Allen", "age": 27, "gender": "Male"},
    {"name": "Ella Ramirez", "age": 20, "gender": "Female"},
    {"name": "Benjamin Evans", "age": 28, "gender": "Male"},
    {"name": "Lily Turner", "age": 23, "gender": "Female"},
    {"name": "Henry Baker", "age": 24, "gender": "Male"},
    {"name": "Zoe Young", "age": 21, "gender": "Female"},
    {"name": "Samuel Carter", "age": 22, "gender": "Male"},
    {"name": "Nora Bell", "age": 19, "gender": "Female"},
    {"name": "Owen Flores", "age": 25, "gender": "Male"},
    {"name": "Scarlett Cooper", "age": 26, "gender": "Female"},
    {"name": "Logan Kelly", "age": 23, "gender": "Male"},
    {"name": "Victoria Price", "age": 24, "gender": "Female"},
    {"name": "Caleb Foster", "age": 27, "gender": "Male"},
    {"name": "Hannah Bell", "age": 22, "gender": "Female"},
    {"name": "Jackson Brooks", "age": 28, "gender": "Male"},
    {"name": "Luna Rivera", "age": 20, "gender": "Female"},
    {"name": "Leo Barnes", "age": 24, "gender": "Male"},
    {"name": "Hazel Cox", "age": 23, "gender": "Female"},
    {"name": "Wyatt Powell", "age": 25, "gender": "Male"},
]

TEAM_TEMPLATES = [
    {"name": "Falcons", "sport": "Football", "description": "Competitive football squad."},
    {"name": "Raptors", "sport": "Basketball", "description": "Agile court team."},
    {"name": "Aces", "sport": "Tennis", "description": "Precision and serves."},
    {"name": "Sharks", "sport": "Swimming", "description": "Speed training crew."},
    {"name": "Lightning", "sport": "Athletics", "description": "Track and field athletes."},
    {"name": "Spikers", "sport": "Volleyball", "description": "Net attack specialists."},
    {"name": "Stars", "sport": "Gymnastics", "description": "Artistry and strength."},
    {"name": "Warriors", "sport": "Rugby", "description": "Tough contact team."},
    {"name": "Birdies", "sport": "Badminton", "description": "Fast pace court team."},
    {"name": "Strikers", "sport": "Cricket", "description": "Precision batting and bowling."},
    {"name": "Titans", "sport": "Football", "description": "Endurance and teamwork."},
    {"name": "Comets", "sport": "Basketball", "description": "Dynamic court play."},
]

NOTIFICATION_TEMPLATES = [
    "Your next session starts in one hour.",
    "A new training session has been added for your team.",
    "Your attendance has been recorded.",
    "Please update your availability for next week.",
    "Club announcement: facility maintenance scheduled.",
]

MEMBERSHIP_TYPES = ["Standard", "Premium", "Elite"]


def seed_database():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(username="admin", email="admin@clubsync.local", role="admin")
        admin.set_password("Admin123!")
        db.session.add(admin)

        coaches = []
        for idx, coach_info in enumerate(COACHES, start=1):
            username = f"coach{idx}"
            email = f"coach{idx}@clubsync.local"
            user = User(username=username, email=email, role="coach")
            user.set_password("Coach123!")
            db.session.add(user)
            db.session.flush()

            coach_profile = CoachProfile(
                user_id=user.id,
                full_name=coach_info["name"],
                phone=f"+10000000{idx:02d}",
                specialization=coach_info["specialization"],
                experience=coach_info["experience"],
            )
            db.session.add(coach_profile)
            coaches.append(coach_profile)

        members = []
        for idx, member_info in enumerate(MEMBERS, start=1):
            username = f"member{idx}"
            email = f"member{idx}@clubsync.local"
            user = User(username=username, email=email, role="member")
            user.set_password("Member123!")
            db.session.add(user)
            db.session.flush()

            member_profile = MemberProfile(
                user_id=user.id,
                full_name=member_info["name"],
                phone=f"+11000000{idx:02d}",
                age=member_info["age"],
                gender=member_info["gender"],
                membership_type=random.choice(MEMBERSHIP_TYPES),
            )
            db.session.add(member_profile)
            members.append(member_profile)

        db.session.flush()

        teams = []
        for idx, template in enumerate(TEAM_TEMPLATES, start=1):
            coach_profile = random.choice(coaches)
            team = Team(
                coach_id=coach_profile.id,
                name=template["name"],
                sport=template["sport"],
                description=template["description"],
            )
            db.session.add(team)
            db.session.flush()
            teams.append(team)

        sessions = []
        for team in teams:
            for session_idx in range(1, 8):
                session_date = date.today() + timedelta(days=random.randint(1, 60))
                start_hour = random.randint(6, 18)
                training_session = TrainingSession(
                    team_id=team.id,
                    title=f"{team.name} Training {session_idx}",
                    date=session_date,
                    location="Club House",
                    capacity=random.choice([15, 20, 25]),
                    start_time=time(hour=start_hour, minute=0),
                    end_time=time(hour=start_hour + 1, minute=30),
                )
                db.session.add(training_session)
                db.session.flush()
                sessions.append(training_session)

        enrollments = []
        for _ in range(200):
            member = random.choice(members)
            training_session = random.choice(sessions)
            if Enrollment.query.filter_by(member_id=member.id, session_id=training_session.id).first():
                continue
            enrollment = Enrollment(
                member_id=member.id,
                session_id=training_session.id,
                attendance=random.choice([True, False]),
                fitness_score=random.randint(50, 100),
                payment_status=random.choice(["paid", "pending", "overdue"]),
                notes="Auto-generated enrollment.",
            )
            db.session.add(enrollment)
            enrollments.append(enrollment)

        db.session.flush()

        for idx in range(30):
            recipient = random.choice([admin] + [user for user in User.query.filter(User.role != "admin").all()])
            notification = Notification(
                user_id=recipient.id,
                title=f"Club announcement {idx + 1}",
                message=random.choice(NOTIFICATION_TEMPLATES),
            )
            db.session.add(notification)

        db.session.commit()
        print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()
