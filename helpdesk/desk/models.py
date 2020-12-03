from django.db import models

# Create your models here.


class Query(models.Model):
    name = models.CharField(max_length=50)
    contact = models.IntegerField()
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='not completed')
    feedback = models.CharField(max_length=20, default='none')
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
