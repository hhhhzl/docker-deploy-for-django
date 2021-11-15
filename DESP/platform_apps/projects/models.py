from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class ChoicesProjectSendWith(models.TextChoices):
    ANONYMOUS = 'A', _('匿名邮件')
    LOGIN = 'L', _('登录系统')


class ChoicesProgressStatus(models.TextChoices):
    NOT_STARTED = '1', _('未开始')
    IN_PROGRESS = '2', _('进行中')
    FINISHED = '3', _('已结束')


class Project(models.Model):
    # 评估项目代码
    id = models.AutoField(primary_key=True)
    # 名称
    name = models.CharField(max_length=100, unique=True, verbose_name="名称")
    # 管理员
    admin = models.ForeignKey("users.DESPUser", on_delete=models.RESTRICT, verbose_name="管理员ID")
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 发放方式
    send_with = models.CharField(max_length=1,
                                 choices=ChoicesProjectSendWith.choices,
                                 default=ChoicesProjectSendWith.LOGIN,
                                 verbose_name="发放方式")
    # 是否计分
    will_mark = models.BooleanField(default=True, verbose_name="是否计分")
    # 是否启用
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    # 参评机构
    org = models.ManyToManyField("organizations.Organization", through="junctions.ProjectOrganization",
                                 related_name="project", verbose_name="参评机构")
    # 开始时间
    start_time = models.DateTimeField(default=now, verbose_name="开始时间")
    # 结束时间
    end_time = models.DateTimeField(default=now, verbose_name="结束时间")

    class Meta:
        managed = True
        db_table = 'app_project'


class Progress(models.Model):
    # 工作进度代码
    id = models.IntegerField(primary_key=True)
    # 所属项目代码
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="所属项目ID")
    # 名称
    name = models.CharField(max_length=100, unique=True, verbose_name="名称")
    # 状态
    status = models.CharField(max_length=1, choices=ChoicesProgressStatus.choices,
                              default=ChoicesProgressStatus.NOT_STARTED, verbose_name="状态")
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 创建者
    created_by = models.ForeignKey("users.DESPUser", on_delete=models.CASCADE, verbose_name="创建者")

    class Meta:
        managed = True
        db_table = "app_progress"
