from core.utils.generic_enum_utils import EnumChoices

class UserRoleEnums(EnumChoices):
    READ = "READ"
    WRITE = "WRITE"
    ADMIN = "ADMIN"

class FriendRequestStatusEnums(EnumChoices):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
