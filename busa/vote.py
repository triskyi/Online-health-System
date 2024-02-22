# busa/models.py

from django.db import models
from accounts.models import StudentUser
from .models import Candidates  # Import Candidates model

class CandidateVote(models.Model):
    candidate = models.ForeignKey(Candidates, on_delete=models.CASCADE)
    voter = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)
