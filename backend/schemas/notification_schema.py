from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.notification import Notification

class NotificationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True
        include_fk = True
