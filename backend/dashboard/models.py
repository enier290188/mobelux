from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import (
    Manager,
    Model,
    ForeignKey,
    BigAutoField,
    BooleanField,
    CharField,
    ImageField,
    SET_NULL,
)
from django.conf import settings


class AlbumManager(Manager):
    pass


class AlbumModel(Model):
    id = BigAutoField(
        verbose_name='ID',
        primary_key=True,
    )
    name = CharField(
        verbose_name='name',
        max_length=64,
        null=False,
        blank=False,
        default='',
        help_text='Name of the album.',
    )
    is_public = BooleanField(
        verbose_name='is public',
        default=True,
        null=False,
        blank=False,
        help_text='Designates whether this album should be treated as public. Unselect this if you would like to be treated as private.',
    )
    user = ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name='user',
        null=True,
        blank=True,
        default=None,
        on_delete=SET_NULL,
        related_name='albums_user',
        related_query_name='album_user',
        help_text='Users.',
    )

    objects = AlbumManager()

    class Meta:
        db_table = 'mobelux_dashboard_album'
        ordering = ['name', ]
        verbose_name_plural = 'albums'
        verbose_name = 'album'
        default_permissions = []

    def __str__(self):
        return '{name}'.format(name=self.name)


class ImageManager(Manager):
    pass


IMAGES_FOLDER_NAME = 'images'
IMAGE_MAX_WIDTH = 960
IMAGE_MAX_HEIGHT = 960
IMAGE_MAX_SIZE = 1048576 // 1024  # 1048576bytes==1mb, 102400bytes==100kb


def image_file_upload_to(instance, filename):
    file_upload_to = '{folder_name}/{current_time}-{filename}'.format(folder_name=IMAGES_FOLDER_NAME, current_time=datetime.now().strftime("%Y%m%d%H%M%S"), filename=filename)
    return file_upload_to


def image_validate_size(avatar):
    size = avatar.size // 1024
    if size > IMAGE_MAX_SIZE:
        raise ValidationError('Maximum file size that can be uploaded is {max_size} KB.'.format(max_size=IMAGE_MAX_SIZE))


def image_validate_dimension(avatar):
    width = avatar.width
    height = avatar.height
    if width > IMAGE_MAX_WIDTH or height > IMAGE_MAX_HEIGHT:
        raise ValidationError('Dimensions are larger than what is allowed: {max_width}x{max_height} pixels.'.format(max_width=IMAGE_MAX_WIDTH, max_height=IMAGE_MAX_HEIGHT))


class ImageModel(Model):
    id = BigAutoField(
        verbose_name='ID',
        primary_key=True,
    )
    title = CharField(
        verbose_name='title',
        max_length=64,
        null=False,
        blank=False,
        default='',
        help_text='Title of the image.',
    )
    image = ImageField(
        upload_to=image_file_upload_to,
        null=True,
        blank=True,
        validators=[
            image_validate_size,
            image_validate_dimension,
        ],
        help_text='Maximum file size that can be uploaded is {max_size} KB. Maximum dimensions: {max_width}x{max_height} pixels.'.format(max_size=IMAGE_MAX_SIZE, max_width=IMAGE_MAX_WIDTH, max_height=IMAGE_MAX_HEIGHT),
    )
    album = ForeignKey(
        to=AlbumModel,
        verbose_name='album',
        null=True,
        blank=True,
        default=None,
        on_delete=SET_NULL,
        related_name='images_album',
        related_query_name='image_album',
        help_text='Select an album.',
    )
    user = ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name='user',
        null=True,
        blank=True,
        default=None,
        on_delete=SET_NULL,
        related_name='images_user',
        related_query_name='image_user',
        help_text='Users.',
    )

    objects = ImageManager()

    class Meta:
        db_table = 'mobelux_dashboard_image'
        ordering = ['title', ]
        verbose_name_plural = 'images'
        verbose_name = 'image'
        default_permissions = []

    def __str__(self):
        return '{title}'.format(title=self.title)
