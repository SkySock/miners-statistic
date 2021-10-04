from django.db import models


class Miner(models.Model):
    name = models.CharField(max_length=40)
    worker = models.CharField(max_length=40, db_index=True)
    is_online = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ('-name',)
        verbose_name = 'miner'
        verbose_name_plural = 'miners'

    def __str__(self):
        return self.name


class HashRate(models.Model):
    miner = models.ForeignKey(Miner, on_delete=models.CASCADE, related_name='hrs')
    hr = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-time',)
        verbose_name = 'hashrate'

    def __str__(self):
        return self.miner.worker + ": " + str(self.hr)


class TimeStart(models.Model):
    name = models.CharField(max_length=40, blank=True, db_index=True)
    time = models.DateTimeField()

    class Meta:
        ordering = ('-time',)
        verbose_name = 'timestart'


class Balance(models.Model):
    value = models.IntegerField()
    description = models.CharField(max_length=30, db_index=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated',)
