from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.member import MemberProfile

class MemberProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MemberProfile
        load_instance = True
        include_fk = True
