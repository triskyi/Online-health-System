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

            # Check if the user has already voted for a candidate in this position/widget
            existing_vote = CandidateVote.objects.filter(voter=student_user, candidate__place=candidate.place).exists()
            if existing_vote:
                messages.error(request, 'You have already voted for a candidate in this position.')
            else:
                # Register the user's vote
                CandidateVote.objects.create(candidate=candidate, voter=student_user)
                candidate.vote += 1
                candidate.save()
                messages.success(request, 'Vote submitted successfully.')

        except Candidates.DoesNotExist:
            messages.error(request, 'Candidate not found.')

        return redirect('/')
    else:
        return redirect('/')
    
    from django.shortcuts import render
from .models import Candidates
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def search_results(request):
    query = request.GET.get('query')

    if query:
        candidates = Candidates.objects.filter(name__icontains=query) | Candidates.objects.filter(place__icontains=query)
        # You can add more fields to search by, like status, etc.
    else:
        candidates = Candidates.objects.all()

    return render(request, 'home.html', {'candidates': candidates})


