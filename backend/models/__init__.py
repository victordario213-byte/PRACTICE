from extensions import db

# Models are imported when the package is initialized to register them with SQLAlchemy.
from .user import User
from .member import MemberProfile
from .coach import CoachProfile
from .team import Team
from .session import TrainingSession
from .enrollment import Enrollment
from .notification import Notification
