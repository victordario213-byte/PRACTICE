from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.coach import CoachProfile

class CoachProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CoachProfile
        load_instance = True
        include_fk = True
