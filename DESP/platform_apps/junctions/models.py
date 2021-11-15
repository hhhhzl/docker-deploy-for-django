from django.db import models


class ProjectOrganization(models.Model):
    # 评估项目
    project = models.ForeignKey("projects.Project", related_name="project_membership",
                                on_delete=models.RESTRICT, null=False, verbose_name="评估项目ID")
    # 机构
    org = models.ForeignKey("organizations.Organization", related_name="project_membership",
                            on_delete=models.RESTRICT, null=False, verbose_name="机构ID")
    # 是否已提交
    is_submitted = models.BooleanField(default=False, verbose_name="已提交")

    class Meta:
        managed = True
        db_table = "app_project_organization"
        unique_together = (("project", "org"),)


class QuestionExpert(models.Model):
    # 问题
    question = models.ForeignKey("questions.Question", on_delete=models.CASCADE, null=False, verbose_name="问题ID")
    # 专家
    expert = models.ForeignKey("users.DESPUser", on_delete=models.CASCADE, null=False, verbose_name="专家ID")

    class Meta:
        managed = True
        db_table = "app_question_expert"
        unique_together = (("question", "expert"),)
