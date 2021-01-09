from django.contrib.auth.backends import ModelBackend as AuthModelBackend


class UserBackend(AuthModelBackend):
    # An inactive user is one that has its is_active field set to False.
    # The ModelBackend and RemoteUserBackend authentication backends prohibits these users from authenticating.
    # If a custom user model doesn’t have an is_active field, all users will be allowed to authenticate.
    # You can use AllowAllUsersModelBackend or AllowAllUsersRemoteUserBackend if you want to allow inactive users to authenticate.
    def user_can_authenticate(self, user):
        return True
