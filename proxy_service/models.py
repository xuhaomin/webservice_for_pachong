from django.db import models


class VPS(models.Model):
    scvp_id = models.AutoField(primary_key=True)
    scvp_vps_proxy = models.CharField(max_length=30)
    scvp_vps_name = models.CharField(max_length=50)
    scvp_create_time = models.DateTimeField()

    def ip(self):
        return self.scvp_vps_proxy
