from configs.core import settings
from controllers.auth.user import UsersControllers

UsersController = UsersControllers("users")

UsersController.add_user_endpoints()

if settings.OPEN_USERS:
    UsersController.add_default_endpoints()
