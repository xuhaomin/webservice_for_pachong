from django.db import models


class Machine(models.Model):

    machine_name = models.CharField(max_length=30, primary_key=True)
    machine_ip = models.CharField(max_length=30)

    def __str__(self):
        return self.machine_name


class Spider(models.Model):

    spider_name = models.CharField(max_length=30, primary_key=True)
    site = models.CharField(max_length=30)

    def __str__(self):
        return self.spider_name


class Task(models.Model):
    spider = models.ForeignKey(Spider)
    is_running = models.BooleanField()
    machine = models.ForeignKey(Machine)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True)
    pid = models.CharField(max_length=20)
