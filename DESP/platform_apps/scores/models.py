from django.db import models


class Score(models.Model):
    # 问题
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, null=False, verbose_name="问题ID")
    # 机构
    org = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, null=False, verbose_name="机构ID")
    # 专家
    expert = models.ForeignKey("users.DESPUser", on_delete=models.CASCADE, null=False, verbose_name="专家ID")
    # 分数
    score = models.DecimalField(decimal_places=6, max_digits=19, null=True, verbose_name="分数")

    class Meta:
        managed = True
        db_table = "app_score"
        unique_together = (("question", "org", "expert"),)
