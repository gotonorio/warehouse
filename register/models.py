from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.dispatch import receiver


class User(AbstractUser):
    pass


@receiver(models.signals.post_save, sender=User)
def post_save_user_signal_handler(sender, instance, created, **kwargs):
    """ シグナルによってUserにgroupを追加する。
    https://stackoverflow.com/questions/51974276/how-to-automatically-add-group-and-staff-permissions-when-user-is-created/51975193
    """
    if created:
        try:
            group = Group.objects.get(name='guest')
        except ObjectDoesNotExist:
            pass
        else:
            instance.groups.add(group)
            instance.save()
