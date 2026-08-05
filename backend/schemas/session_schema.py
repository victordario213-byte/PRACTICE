from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.session import TrainingSession

class TrainingSessionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingSession
        load_instance = True
        include_fk = True
