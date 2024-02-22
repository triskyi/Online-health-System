
from .models import Candidates
from django.contrib import admin

def reset_voters(modeladmin, request, queryset):
    for candidate in queryset:
        candidate.voters.clear()
        candidate.vote = 0
        candidate.save()

reset_voters.short_description = "Reset Voters and Votes to Zero"

class CandidatesAdmin(admin.ModelAdmin):
    actions = [reset_voters]

# Register the Candidates model with the custom admin class




admin.site.register(Candidates)