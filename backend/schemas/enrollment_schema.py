from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.enrollment import Enrollment

class EnrollmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Enrollment
        load_instance = True
        include_fk = True
