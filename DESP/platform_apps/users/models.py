from django.apps import apps
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class ChoicesUserSex(models.TextChoices):
    MALE = 'M', _('男')
    FEMALE = 'F', _('女')


class ChoicesUserDegree(models.TextChoices):
    PHD = '1', _('博士')
    MASTER = '2', _('硕士')
    BACHELOR = '3', _('大学本科')
    VOCATION = '4', _('大学专科')
    HS = '5', _('高中、职中、中专')
    MS = '6', _('初中或以下')


class ChoicesUserType(models.TextChoices):
    SUPERVISOR = 'S', _('超级管理员')
    ADMINISTRATOR = 'A', _('管理员')
    EXPERT = 'E', _('专家用户')
    MANAGER = 'M', _('机构领导')
    USER = 'U', _('机构用户')


class DESPUserManager(BaseUserManager):

    def create_user(self,
                    username, email, last_name, first_name, sex, mobile_number, degree, org, user_type,
                    tel_number=None, position=None, field=None, password=None, **kwargs):
        # 创建用户
        user = self.model(
            username=username, email=self.normalize_email(email), last_name=last_name, first_name=first_name,
            sex=sex, mobile_number=mobile_number, tel_number=tel_number, degree=degree, org=org,
            position=position, field=field, user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         username, email, last_name, first_name, sex, mobile_number, degree,
                         tel_number=None, position=None, field=None, password=None, **kwargs):
        # 查找机构
        Organization = apps.get_model("organizations", "Organization")
        org_instance = Organization.objects.get(id=1)
        # 创建用户
        user = self.model(
            username=username, email=self.normalize_email(email), last_name=last_name, first_name=first_name,
            sex=sex, mobile_number=mobile_number, tel_number=tel_number, degree=degree, org=org_instance,
            position=position, field=field, user_type='S'
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class DESPUser(AbstractUser):
    # 用户名
    username = models.CharField(max_length=25, unique=True,
                                validators=[RegexValidator("^[A-Za-z0-9_]{4,25}$")],
                                verbose_name="用户名")
    # 邮箱
    email = models.EmailField(unique=True, verbose_name="邮箱")
    # 姓
    last_name = models.CharField(max_length=20, verbose_name="姓")
    # 名
    first_name = models.CharField(max_length=20, verbose_name="名")
    # 性别
    sex = models.CharField(max_length=1, choices=ChoicesUserSex.choices,
                           default=ChoicesUserSex.MALE, verbose_name="性别")
    # 手机号码
    mobile_number = models.CharField(max_length=11,
                                     validators=[RegexValidator("^[0-9]{11}$")],
                                     verbose_name="手机号码")
    # 座机号码
    tel_number = models.CharField(max_length=15, blank=True, null=True,
                                  validators=[RegexValidator("^[0-9]{7,15}$")],
                                  verbose_name="座机号码")
    # 学历
    degree = models.CharField(max_length=1, choices=ChoicesUserDegree.choices,
                              default=ChoicesUserDegree.PHD, verbose_name="学历")
    # 所属机构
    org = models.ForeignKey("organizations.Organization", on_delete=models.RESTRICT,
                            related_name="users", verbose_name="所属机构")
    # 职位
    position = models.CharField(max_length=50, blank=True, null=True, verbose_name="职位")
    # 工作领域
    field = models.CharField(max_length=50, blank=True, null=True, verbose_name="工作领域")
    # 用户类型
    user_type = models.CharField(max_length=1, choices=ChoicesUserType.choices,
                                 default=ChoicesUserType.USER, verbose_name="用户类型")

    # 重写默认值
    objects = DESPUserManager()
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "last_name", "first_name", "sex", "mobile_number", "org", "degree", "user_type"]

    class Meta:
        managed = True
        db_table = 'app_user'


@receiver(models.signals.post_save, sender=DESPUser)
def create_token(sender, instance=None, created=False, **kwargs):
    """
    Generate a token for the user instance immediately after its creation.
    https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
    """
    if created:
        Token.objects.create(user=instance)
