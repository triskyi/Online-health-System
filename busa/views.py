from django.shortcuts import render, redirect
from .models import Candidates,  CandidateVote
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    candidates = Candidates.objects.all()
    return render(request, 'home.html', {'candidates': candidates})




@login_required
def vote(request, candidate_id):
    if request.method == 'POST':
        student_user = request.user

        try:
            candidate = Candidates.objects.get(pk=candidate_id)

            # Check if the user has already voted for this candidate
            existing_vote, created = CandidateVote.objects.get_or_create(candidate=candidate, voter=student_user)
            if not created:
                messages.error(request, 'You have already voted for this candidate.')
            else:
                # Register the user's vote
                candidate.vote += 1
                candidate.save()
                messages.success(request, 'Vote submitted successfully.')

        except Candidates.DoesNotExist:
            messages.error(request, 'Candidate not found.')

        return redirect('/')
    else:
        return redirect('/')


def candidate_list(request, position):
    candidates =  Candidates.objects.filter(place=position)
    context = {
        'candidates': candidates,
        'position': position,
    }
    return render(request, 'candidate_list.html', context)