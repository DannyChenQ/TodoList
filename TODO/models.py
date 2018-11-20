from django.db import models
from django.contrib.auth.models import User


class list(models.Model):
	user = models.ForeignKey(User, related_name='user_list')
	content = models.TextField()
	level = models.CharField(max_length=10)
	add_time = models.CharField(max_length=150)
	complete_time = models.CharField(max_length=150)
	is_complete = models.CharField(max_length=10)
	is_send_mail = models.IntegerField()
	time_day = models.CharField(max_length=24)
	time_hours = models.CharField(max_length=60)
	time_minute = models.CharField(max_length=60)
	class Meta:
		ordering = ['-add_time']
