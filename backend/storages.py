"""Custom storage classes for static and media files."""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Custom storage class for static files."""
    custom_domain = None
    location = settings.STATICFILES_LOCATION
    file_overwrite = True
    default_acl = 'private'


class MediaStorage(S3Boto3Storage):
    """Custom storage class for media files."""
    custom_domain = None
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False
    default_acl = 'private'
