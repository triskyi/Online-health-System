# busa/models.py
from django.db import models
from accounts.models import StudentUser

class Candidates(models.Model):
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    image = models.ImageField(upload_to='candidate_images/')
    vote = models.IntegerField(default=0)

    def total_votes(self):
        return self.vote

class CandidateVote(models.Model):
    candidate = models.ForeignKey(Candidates, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)
    