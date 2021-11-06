from typing import Any

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


class Resources(models.Model):
    objects: Any = models.Manager()

    title: Any = models.CharField(
        max_length=150, db_index=True, verbose_name="ресурс"
    )

    def __str__(self) -> Any:
        return self.title

    def get_absolute_url(self) -> Any:
        return reverse_lazy("parse:resource", kwargs={"resource_id": self.pk})

    class Meta:
        verbose_name = "ресурс"
        verbose_name_plural = "ресурсы"
        ordering = ["id"]


# noinspection PyCallingNonCallable
class Articles(models.Model):
    objects: Any = models.Manager()

    date: Any = models.DateTimeField()
    date_update: Any = models.DateTimeField(auto_now=True)
    title: Any = models.TextField(null=True)
    text: Any = models.TextField(null=True)
    url: Any = models.URLField(unique=True)
    resource: Any = models.ForeignKey(Resources, on_delete=models.PROTECT)
    users: Any = models.ManyToManyField(User)
    owner: Any = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="my_article",
    )

    def __str__(self) -> Any:
        return self.title

    def get_absolute_url(self) -> Any:
        return reverse_lazy("parse:article", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ["-date", "id"]
