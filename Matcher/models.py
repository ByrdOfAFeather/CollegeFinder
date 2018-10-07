from django.db import models


class University(models.Model):
	name = models.CharField(max_length=300, unique=True)
	average_gpa = models.FloatField()
	average_sat_score = models.IntegerField()
	sat_percentile_25 = models.IntegerField()
	sat_percentile_75 = models.IntegerField()
	average_act_score = models.IntegerField()
