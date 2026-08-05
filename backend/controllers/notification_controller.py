from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models.notification import Notification
from models.user import User
from schemas.notification_schema import NotificationSchema
from .auth_utils import role_required

notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)

class NotificationListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        role = get_jwt().get("role")

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        if role == "admin":
            query = Notification.query
        else:
            query = Notification.query.filter_by(user_id=user_id)

        notifications = query.order_by(Notification.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return {
            "notifications": notifications_schema.dump(notifications.items),
            "page": notifications.page,
            "per_page": notifications.per_page,
            "total": notifications.total,
        }, 200

    @jwt_required()
    @role_required("admin")
    def post(self):
        payload = request.get_json() or {}
        errors = notification_schema.validate(payload)
        if errors:
            return {"message": "Invalid notification data.", "errors": errors}, 400

        user_id = payload.get("user_id")
        if not User.query.get(user_id):
            return {"message": "User not found."}, 404

        notification = Notification(
            user_id=user_id,
            title=payload["title"],
            message=payload["message"],
        )
        db.session.add(notification)
        db.session.commit()

        return {"message": "Notification sent successfully.", "notification": notification.to_dict()}, 201

class NotificationResource(Resource):
    @jwt_required()
    def put(self, notification_id):
        notification = Notification.query.get_or_404(notification_id)
        role = get_jwt().get("role")
        user_id = get_jwt_identity()

        if role != "admin" and notification.user_id != user_id:
            return {"message": "You can only update your own notifications."}, 403

        payload = request.get_json() or {}
        if payload.get("is_read") is not None:
            notification.is_read = bool(payload["is_read"])
        db.session.commit()
        return {"message": "Notification updated successfully.", "notification": notification.to_dict()}, 200

    @jwt_required()
    @role_required("admin")
    def delete(self, notification_id):
        notification = Notification.query.get_or_404(notification_id)
        db.session.delete(notification)
        db.session.commit()
        return {"message": "Notification deleted successfully."}, 200
