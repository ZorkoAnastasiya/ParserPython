from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Resources(models.Model):
    objects = models.Manager()

    title = models.CharField(
        max_length = 150,
        db_index = True,
        verbose_name = "ресурс"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ресурс"
        verbose_name_plural = "ресурсы"
        ordering = ["id"]


class Articles(models.Model):
    objects = models.Manager()

    date = models.DateTimeField(blank = True)
    title = models.TextField(null = True)
    text = models.TextField(null = True)
    url = models.URLField(unique = True)
    resource = models.ForeignKey(Resources, on_delete = models.PROTECT)
    users = models.ManyToManyField(User, null = True)

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ["-date"]
