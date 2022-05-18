from enum import Enum

class UserRole(Enum):
    admin = "admin"
    director = "director"
    deputy = "deputy"
    worker = "worker"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)