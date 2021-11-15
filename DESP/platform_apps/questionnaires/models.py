from django.db import models


class Questionnaire(models.Model):
    # 问卷代码
    id = models.AutoField(primary_key=True)
    # 所属项目代码
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, verbose_name="所属项目ID")
    # 标题
    title = models.CharField(max_length=255, verbose_name="标题")
    # 描述
    description = models.TextField(verbose_name="描述")
    # 标识符
    identifier = models.CharField(max_length=50, verbose_name="标识符")

    class Meta:
        managed = True
        db_table = "app_questionnaire"


class Indicator(models.Model):
    # 指标代码
    id = models.AutoField(primary_key=True)
    # 所属问卷代码
    qnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, verbose_name="所属问卷ID")
    # 名称
    name = models.CharField(max_length=255, verbose_name="名称")
    # 权重
    weight = models.IntegerField(verbose_name="权重")
    # 上级指标
    parent_indicator = models.ForeignKey("self", on_delete=models.CASCADE, null=True, verbose_name="上级指标")
    # 指向问题
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, null=True, verbose_name="指向问题")

    class Meta:
        managed = True
        db_table = "app_indicator"
        constraints = [
            models.CheckConstraint(
                name="app_indicator_parent_question_null",
                check=~models.Q(parent_indicator__isnull=False, question__isnull=False)
            )
        ]
