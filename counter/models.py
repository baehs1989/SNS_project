from django.db import models

# Create your models here.
class Visitor(models.Model):
    visitors = models.IntegerField(default=1)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def count_up(self):
        self.visitors = self.visitors + 1
        super().save()
