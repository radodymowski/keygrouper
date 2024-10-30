from django.db import models

class NameGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class NameEntity(models.Model):
    name_group = models.ForeignKey(NameGroup, related_name="names", on_delete=models.PROTECT)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
