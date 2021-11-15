from django.db import models
from django.utils.translation import gettext_lazy as _


class ChoicesQuestionType(models.TextChoices):
    MULTIPLE_CHOICES = '1', _('选择')
    FILL_IN_BLANK = '2', _('填空')
    MATRIX = '3', _('矩阵')
    SHORT_ANSWERS = '4', _('简答')
    TABLE = '5', _('表格')
    ATTACHMENTS = '6', _('附件')


class ChoicesQuestionRubric(models.TextChoices):
    AUTO = 'A', _('自动打分')
    EXPERT = 'E', _('专家打分')


class Question(models.Model):
    # 问题代码
    id = models.AutoField(primary_key=True)
    # 序号 (前端显示用)
    order = models.IntegerField(default=0, verbose_name="序号")
    # 所属问卷代码
    qnaire = models.ForeignKey("questionnaires.Questionnaire", on_delete=models.CASCADE, verbose_name="所属问卷ID")
    # 问题类型
    question_type = models.CharField(max_length=1, choices=ChoicesQuestionType.choices,
                                     default=ChoicesQuestionType.MULTIPLE_CHOICES, verbose_name="问题类型")
    # 标题
    title = models.CharField(max_length=255, verbose_name="标题")
    # 题干
    stem = models.TextField(verbose_name="题干")
    # 是否必答
    is_required = models.BooleanField(verbose_name="必答")
    # 最低分数
    min_score = models.DecimalField(decimal_places=6, max_digits=19, verbose_name="最低分数")
    # 最高分数
    max_score = models.DecimalField(decimal_places=6, max_digits=19, verbose_name="最高分数")
    # 打分方式
    rubric = models.CharField(max_length=1, choices=ChoicesQuestionRubric.choices,
                              default=ChoicesQuestionRubric.EXPERT, verbose_name="打分方式")
    # 打分细则
    rubric_detail = models.TextField(blank=True, null=True, verbose_name="打分细则")
    
    

    class Meta:
        managed = True
        db_table = "app_question"
        unique_together = (('stem','order','question_type'))
