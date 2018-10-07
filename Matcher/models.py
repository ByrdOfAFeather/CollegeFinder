from django.db import models


class University(models.Model):
	name = models.CharField(max_length=300, unique=True)
	average_gpa = models.FloatField()
	average_sat_score = models.IntegerField()
	sat_percentile_25 = models.IntegerField()
	sat_percentile_75 = models.IntegerField()
	average_act_score = models.IntegerField()

	class Meta:
		verbose_name_plural = "Universities"

	def __str__(self):
		return f"{self.name}"


class ExtraCirculars(models.Model):
	category = models.CharField(max_length=100)
	university_percentage = models.FloatField()
	university = models.ForeignKey(University, on_delete="cascade", related_name="extras")
