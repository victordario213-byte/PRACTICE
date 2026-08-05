from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.team import Team

class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        load_instance = True
        include_fk = True
