from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name="Название метки")

    def __str__(self):
        return self.name
