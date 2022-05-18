from django.db.models import manager

from django.contrib.auth.models import UserManager


class AdminManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="admin")



class DirectorManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role="director")



class DeputyManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role="deputy")


class WorkerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role="worker")