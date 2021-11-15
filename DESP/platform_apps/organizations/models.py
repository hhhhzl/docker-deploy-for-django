from django.db import models
from django.utils.translation import gettext_lazy as _


class ChoicesOrganizationType(models.TextChoices):
    INSTITUTE = 'I', _('研究所')
    BRANCH = 'B', _('分院')
    SUPPORT = 'S', _('支撑单位')
    UNIVERSITY = 'U', _('学校')


class Organization(models.Model):
    # 机构代码
    id = models.AutoField(primary_key=True)
    # 机构名称
    name = models.CharField(max_length=100, unique=True, verbose_name="机构名称")
    # 机构类别
    org_type = models.CharField(max_length=1, choices=ChoicesOrganizationType.choices,
                                default=ChoicesOrganizationType.INSTITUTE, verbose_name="机构类别")
    # 是否启用
    is_active = models.BooleanField(default=True, verbose_name="有效")
    # 上级机构
    parent_org = models.ForeignKey("self", on_delete=models.RESTRICT, blank=True, null=True, verbose_name="上级机构")
    # 地址
    address = models.CharField(max_length=100, null=True, verbose_name="地址")
    # 邮编
    postcode = models.CharField(max_length=6, null=True, verbose_name="邮编")
    # 所属部门
    department = models.CharField(max_length=255, null=True, verbose_name="部门")
    # 电话号码
    phone = models.CharField(max_length=15, null=True, verbose_name="电话号码")

    class Meta:
        managed = True
        db_table = 'app_organization'
