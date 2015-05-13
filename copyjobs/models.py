from django.db import models

# Create your models here.


class CopyJob(models.Model):

    copied_files              = models.IntegerField()
    corrupt_files             = models.IntegerField()
    elapsed_time              = models.FloatField() # seconds
    elapsed_copy_time         = models.FloatField() # seconds
    datavolume                = models.BigIntegerField()
    transfertime              = models.DateTimeField()


