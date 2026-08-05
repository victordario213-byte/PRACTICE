from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.user import User

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        exclude = ("password_hash",)

    password = fields.String(
        load_only=True,
        required=True,
        validate=validate.Length(min=6)
    )
    role = fields.String(validate=validate.OneOf(["admin", "coach", "member"]))
