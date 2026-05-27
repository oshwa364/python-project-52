from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Task status'
        ordering = ['id']
