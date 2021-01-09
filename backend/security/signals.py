from django.contrib.auth import get_user_model
from django.db.models.signals import (
    post_save,
    pre_save,
)
from django.dispatch import receiver
from .models import ProfileModel


@receiver(signal=post_save, sender=get_user_model())
def signal_usermodel_post_save(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'profile'):
        ProfileModel(user=instance, user_folder_name=instance.username).save()
    else:
        instance.profile.save()


@receiver(signal=pre_save, sender=ProfileModel)
def signal_profilemodel_pre_save(sender, instance, **kwargs):
    instance.signal_profilemodel_pre_save()
