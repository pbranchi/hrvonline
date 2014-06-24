import csv
import json
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import jsonfield
import os
from datetime import datetime, date, timedelta

# Create your models here.

class SubmittedProcess(models.Model):
    process_id = models.AutoField(primary_key=True)
    galaxy_key = models.CharField(max_length=40)
    pipeline = models.CharField(max_length=40)
    pipeline_id = models.CharField(max_length=40)
    user = models.CharField(max_length=40)
    user_id = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    submitted = models.CharField(max_length=40)

