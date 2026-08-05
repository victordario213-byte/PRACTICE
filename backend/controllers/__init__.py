from flask import Blueprint


def create_api_blueprint():
    return Blueprint("api", __name__, url_prefix="/api")


def register_resources(api):
    from .auth_controller import RegisterResource, LoginResource
    from .user_controller import UserListResource, UserResource
    from .team_controller import TeamListResource, TeamResource
    from .session_controller import SessionListResource, SessionResource
    from .enrollment_controller import EnrollmentListResource, EnrollmentResource
    from .notification_controller import NotificationListResource, NotificationResource
    from .coach_controller import CoachListResource, CoachResource, CoachMembersResource
    from .member_controller import MemberListResource, MemberResource

    api.add_resource(RegisterResource, "/auth/register")
    api.add_resource(LoginResource, "/auth/login")
    api.add_resource(UserListResource, "/users")
    api.add_resource(UserResource, "/users/<int:user_id>")
    api.add_resource(TeamListResource, "/teams")
    api.add_resource(TeamResource, "/teams/<int:team_id>")
    api.add_resource(SessionListResource, "/sessions")
    api.add_resource(SessionResource, "/sessions/<int:session_id>")
    api.add_resource(EnrollmentListResource, "/enrollments")
    api.add_resource(EnrollmentResource, "/enrollments/<int:enrollment_id>")
    api.add_resource(NotificationListResource, "/notifications")
    api.add_resource(NotificationResource, "/notifications/<int:notification_id>")
    api.add_resource(CoachListResource, "/coaches")
    api.add_resource(CoachResource, "/coaches/<int:coach_id>")
    api.add_resource(CoachMembersResource, "/coach/members")
    api.add_resource(MemberListResource, "/members")
    api.add_resource(MemberResource, "/members/<int:member_id>")
