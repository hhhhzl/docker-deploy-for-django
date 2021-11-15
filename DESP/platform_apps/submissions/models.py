from django.db import models


class Submission(models.Model):
    # 问题
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, null=False, verbose_name="问题ID")
    # 机构
    org = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, null=False, verbose_name="机构ID")
    # 答案
    answer = models.TextField(blank=True, null=True, verbose_name="答案")
    # 附件
    attachment = models.TextField(blank=True, null=True, verbose_name="附件")
    # 上次更新时间
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="上次更新时间")
    # 上次更新者
    last_updated_by = models.ForeignKey("users.DESPUser", on_delete=models.CASCADE, verbose_name="上次更新者")
    # 最终分数
    final_score = models.DecimalField(decimal_places=6, max_digits=19, null=True, verbose_name="最终分数")

    class Meta:
        managed = True
        db_table = "app_submission"
        unique_together = (("question", "org"),)
