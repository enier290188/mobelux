import os
import shutil
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser as AuthUserModel,
    UserManager as AuthUserManager,
    Group as AuthGroup,
    Permission as AuthPermission,
)
from django.contrib.auth.validators import UnicodeUsernameValidator as AuthUnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db.models import (
    Model,
    ForeignKey,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ImageField,
    ManyToManyField,
    OneToOneField,
    CASCADE,
)
from django.utils import timezone

MEDIA_FOLDER_PATH = settings.MEDIA_ROOT if settings.LOCAL is True else settings.MEDIAFILES_LOCATION + '/'


def get_s3_resource():
    s3_resource = boto3.resource(
        service_name='s3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    return s3_resource


def get_s3_client(s3_resource):
    s3_client = s3_resource.meta.client
    return s3_client


def get_s3_bucket(s3_resource):
    s3_bucket = s3_resource.Bucket(name=settings.AWS_STORAGE_BUCKET_NAME)
    return s3_bucket


def exists_path(path):
    if settings.LOCAL is True:
        return os.path.exists(path=path)
    else:
        s3_bucket = get_s3_bucket(s3_resource=get_s3_resource())
        try:
            s3_bucket.Object(key=path).get()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                # The object does not exist.
                return False
            else:
                # Something else has gone wrong.
                raise Exception('Something else has gone wrong')
        else:
            return True


def create_folder_path(path):
    if settings.LOCAL is True:
        os.mkdir(path=path)
    else:
        s3_resource = get_s3_resource()
        s3_client = get_s3_client(s3_resource=s3_resource)
        s3_bucket = get_s3_bucket(s3_resource=s3_resource)
        s3_client.put_object(Bucket=s3_bucket.name, Key=path)


def delete_folder_path(path):
    if settings.LOCAL is True:
        shutil.rmtree(path=path)
    else:
        s3_resource = get_s3_resource()
        s3_bucket = get_s3_bucket(s3_resource=s3_resource)
        for obj in s3_bucket.objects.filter(Prefix=path):
            s3_resource.Object(bucket_name=s3_bucket.name, key=obj.key).delete()


def delete_file_path(path):
    if settings.LOCAL is True:
        os.remove(path=path)
    else:
        s3_resource = get_s3_resource()
        s3_bucket = get_s3_bucket(s3_resource=s3_resource)
        for obj in s3_bucket.objects.filter(Prefix=path):
            s3_resource.Object(bucket_name=s3_bucket.name, key=obj.key).delete()


def move_file_path(path, new_path):
    if settings.LOCAL is True:
        os.rename(path, new_path)
    else:
        s3_resource = get_s3_resource()
        s3_bucket = get_s3_bucket(s3_resource=s3_resource)
        # The source in CopySource=source had to be a full path from the bucket root to the actual file instead of a dictionary of bucket name and key.
        s3_resource.Object(bucket_name=s3_bucket.name, key=new_path).copy_from(CopySource=s3_bucket.name + '/' + path)


class UserManager(AuthUserManager):
    def create_user(self, username, password=None, **extra_fields):
        super(UserManager, self).create_user(username=username, password=password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        super(UserManager, self).create_superuser(username=username, password=password, **extra_fields)


class UserModel(AuthUserModel):
    first_name = CharField(
        verbose_name='first name',
        blank=True,
        max_length=150,
    )
    last_name = CharField(
        verbose_name='last name',
        blank=True,
        max_length=150,
    )
    username = CharField(
        verbose_name='username',
        unique=True,
        max_length=150,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[
            AuthUnicodeUsernameValidator(),
        ],
        error_messages={
            'unique': 'User with this username already exists.',
        },
    )
    email = EmailField(
        verbose_name='email',
        blank=True,
        max_length=254,
    )
    password = CharField(
        verbose_name='password',
        max_length=128,
    )
    groups = ManyToManyField(
        to=AuthGroup,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='user_set',
        related_query_name='user',
        through='UserGroupModel',
        through_fields=('user', 'group',),
    )
    user_permissions = ManyToManyField(
        to=AuthPermission,
        verbose_name='permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_set',
        related_query_name='user',
        through='UserPermissionModel',
        through_fields=('user', 'permission',),
    )
    is_superuser = BooleanField(
        verbose_name='superuser status',
        default=False,
        help_text='Designates that this user has all permissions without explicitly assigning them.',
    )
    is_staff = BooleanField(
        verbose_name='staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = BooleanField(
        verbose_name='active status',
        default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
    )
    date_joined = DateTimeField(
        verbose_name='date joined',
        default=timezone.now,
    )
    last_login = DateTimeField(
        verbose_name='last login',
        blank=True,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AuthUserModel.Meta):
        db_table = 'mobelux_security_user'
        verbose_name_plural = 'users'
        verbose_name = 'user'
        ordering = ['username', ]
        default_permissions = []

    def __str__(self):
        return self.get_full_name() or self.get_username()


PROFILES_FOLDER_NAME = 'profiles'
PROFILE_AVATAR_FILE_NAME = 'avatar'
PROFILE_AVATAR_FILE_EXT = 'png'
PROFILE_AVATAR_MAX_WIDTH = 960
PROFILE_AVATAR_MAX_HEIGHT = 960
PROFILE_AVATAR_MAX_SIZE = 102400 // 1024  # 1048576bytes==1mb, 102400bytes==100kb


def profile_avatar_file_upload_to(instance, filename):
    file_upload_to = instance.get_avatar_file_upload_to()
    file_path = instance.get_avatar_file_path()
    if exists_path(path=file_path):
        delete_file_path(path=file_path)
    return file_upload_to


def profile_avatar_validate_size(avatar):
    size = avatar.size // 1024
    if size > PROFILE_AVATAR_MAX_SIZE:
        raise ValidationError('Maximum file size that can be uploaded is {max_size} KB.'.format(max_size=PROFILE_AVATAR_MAX_SIZE))


def profile_avatar_validate_dimension(avatar):
    width = avatar.width
    height = avatar.height
    if width > PROFILE_AVATAR_MAX_WIDTH or height > PROFILE_AVATAR_MAX_HEIGHT:
        raise ValidationError('Dimensions are larger than what is allowed: {max_width}x{max_height} pixels.'.format(max_width=PROFILE_AVATAR_MAX_WIDTH, max_height=PROFILE_AVATAR_MAX_HEIGHT))


class ProfileModel(Model):
    user = OneToOneField(
        to=UserModel,
        on_delete=CASCADE,
        related_name='profile',
    )
    user_folder_name = CharField(
        verbose_name='user_folder_name',
        max_length=150,
        null=True,
        blank=True,
    )
    avatar = ImageField(
        upload_to=profile_avatar_file_upload_to,
        null=True,
        blank=True,
        validators=[
            profile_avatar_validate_size,
            profile_avatar_validate_dimension,
        ],
        help_text='Maximum file size that can be uploaded is {max_size} KB. Maximum dimensions: {max_width}x{max_height} pixels.'.format(max_size=PROFILE_AVATAR_MAX_SIZE, max_width=PROFILE_AVATAR_MAX_WIDTH, max_height=PROFILE_AVATAR_MAX_HEIGHT),
    )

    class Meta:
        db_table = 'mobelux_security_profile'
        verbose_name_plural = 'profiles'
        verbose_name = 'profile'
        ordering = ['user__username', ]
        default_permissions = []

    def __str__(self):
        return self.user.__str__()

    def get_user_folder_upload_to(self):
        return '{profiles_folder_name}{user_folder_name}'.format(
            profiles_folder_name=PROFILES_FOLDER_NAME + '/',
            user_folder_name=self.user_folder_name + '/',
        )

    def get_new_user_folder_upload_to(self):
        return '{profiles_folder_name}{new_user_folder_name}'.format(
            profiles_folder_name=PROFILES_FOLDER_NAME + '/',
            new_user_folder_name=self.user.username + '/',
        )

    def get_avatar_file_upload_to(self):
        return '{user_folder_upload_to}{avatar_file_name}.{avatar_file_ext}'.format(
            user_folder_upload_to=self.get_user_folder_upload_to(),
            avatar_file_name=PROFILE_AVATAR_FILE_NAME,
            avatar_file_ext=PROFILE_AVATAR_FILE_EXT,
        )

    def get_new_avatar_file_upload_to(self):
        return '{new_user_folder_upload_to}{avatar_file_name}.{avatar_file_ext}'.format(
            new_user_folder_upload_to=self.get_new_user_folder_upload_to(),
            avatar_file_name=PROFILE_AVATAR_FILE_NAME,
            avatar_file_ext=PROFILE_AVATAR_FILE_EXT,
        )

    def get_user_folder_path(self):
        return MEDIA_FOLDER_PATH + self.get_user_folder_upload_to()

    def get_new_user_folder_path(self):
        return MEDIA_FOLDER_PATH + self.get_new_user_folder_upload_to()

    def get_avatar_file_path(self):
        return MEDIA_FOLDER_PATH + self.get_avatar_file_upload_to()

    def get_new_avatar_file_path(self):
        return MEDIA_FOLDER_PATH + self.get_new_avatar_file_upload_to()

    def signal_profilemodel_pre_save(self):
        user_folder_path = self.get_user_folder_path()
        new_user_folder_path = self.get_new_user_folder_path()
        avatar_file_path = self.get_avatar_file_path()
        new_avatar_file_path = self.get_new_avatar_file_path()
        if not exists_path(path=user_folder_path):
            create_folder_path(path=user_folder_path)
        if user_folder_path == new_user_folder_path:
            if exists_path(path=avatar_file_path):
                if self.avatar:
                    self.avatar.name = self.get_avatar_file_upload_to()
                else:
                    delete_file_path(path=avatar_file_path)
        else:
            if exists_path(path=new_user_folder_path):
                delete_folder_path(path=new_user_folder_path)
            create_folder_path(path=new_user_folder_path)
            if exists_path(path=avatar_file_path):
                if self.avatar:
                    move_file_path(path=avatar_file_path, new_path=new_avatar_file_path)
                    self.avatar.name = self.get_new_avatar_file_upload_to()
                else:
                    delete_file_path(path=avatar_file_path)
            else:
                if self.avatar:
                    self.avatar.name = None
            delete_folder_path(path=user_folder_path)
            self.user_folder_name = self.user.username


class UserGroupModel(Model):
    user = ForeignKey(
        to=UserModel,
        on_delete=CASCADE,
    )
    group = ForeignKey(
        to=AuthGroup,
        on_delete=CASCADE,
    )

    class Meta:
        db_table = 'mobelux_security_user_group'
        ordering = ['user', 'group', ]
        default_permissions = []

    def __str__(self):
        return '<{user}> <{group}>'.format(user=self.user, group=self.group)


class UserPermissionModel(Model):
    user = ForeignKey(
        to=UserModel,
        on_delete=CASCADE,
    )
    permission = ForeignKey(
        to=AuthPermission,
        on_delete=CASCADE,
    )

    class Meta:
        db_table = 'mobelux_security_user_permission'
        ordering = ['user', 'permission', ]
        default_permissions = []

    def __str__(self):
        return '<{user}> <{permission}>'.format(user=self.user, permission=self.permission)
