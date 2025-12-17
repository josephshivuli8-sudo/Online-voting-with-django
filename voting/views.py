from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib import messages
from django.utils.text import slugify
import logging

from .models import Position, Candidate, Voter, Votes
from account.views import account_login

logger = logging.getLogger(__name__)


# =========================
# HOME / REDIRECT
# =========================
def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse('account_login'))

    if request.user.user_type == '1':
        return redirect(reverse('adminDashboard'))

    return redirect(reverse('voterDashboard'))


# =========================
# BALLOT GENERATION
# =========================
def generate_ballot(display_controls=False):
    positions = Position.objects.order_by('priority').all()
    output = ""
    num = 1

    for position in positions:
        candidates_data = ""
        candidates = Candidate.objects.filter(position=position)

        for candidate in candidates:
            if position.max_vote > 1:
                instruction = f"You may select up to {position.max_vote} candidates"
                input_box = (
                    f'<input type="checkbox" value="{candidate.id}" '
                    f'class="flat-red {slugify(position.name)}" '
                    f'name="{slugify(position.name)}[]">'
                )
            else:
                instruction = "Select only one candidate"
                input_box = (
                    f'<input type="radio" value="{candidate.id}" '
                    f'class="flat-red {slugify(position.name)}" '
                    f'name="{slugify(position.name)}">'
                )

            # Removed candidate image
            candidates_data += f"""
                <li>
                    {input_box}
                    <span>{candidate.fullname}</span>
                </li>
            """

        output += f"""
        <div class="box box-solid" style="background-color: #f0f4f8; border-radius: 8px; padding: 10px; margin-bottom: 15px;">
            <div class="box-header with-border">
                <h3 class="box-title" style="color: #1f2937;"><b>{position.name}</b></h3>
            </div>
            <div class="box-body">
                <p style="color: #4b5563;">{instruction}</p>
                <ul style="list-style-type: none; padding-left: 0;">{candidates_data}</ul>
            </div>
        </div>
        """

        # Update priority
        position.priority = num
        position.save()
        num += 1

    return output


def fetch_ballot(request):
    return JsonResponse(generate_ballot(True), safe=False)


# =========================
# DASHBOARD
# =========================
def dashboard(request):
    voter = request.user.voter

    if voter.voted:
        votes = Votes.objects.filter(voter=voter).select_related('candidate', 'position')
        context = {
            'my_votes': votes,
        }
        return render(request, "voting/voter/result.html", context)

    return redirect(reverse('show_ballot'))


# =========================
# VOTING
# =========================
def show_ballot(request):
    voter = request.user.voter

    if voter.voted:
        messages.error(request, "You have already voted")
        return redirect(reverse('voterDashboard'))

    context = {
        'ballot': generate_ballot(False)
    }
    return render(request, "voting/voter/ballot.html", context)


def preview_vote(request):
    if request.method != 'POST':
        return JsonResponse({"error": True, "list": ""})

    form = dict(request.POST)
    form.pop('csrfmiddlewaretoken', None)
    output = ""

    for position in Position.objects.all():
        key = slugify(position.name)
        values = form.get(key) or form.get(f"{key}[]")

        if not values:
            continue

        if not isinstance(values, list):
            values = [values[0]]

        for cid in values:
            candidate = Candidate.objects.filter(id=cid).first()
            if candidate:
                output += f"<p>{position.name}: {candidate.fullname}</p>"

    if output == "":
        return JsonResponse({"error": True, "list": ""})

    return JsonResponse({"error": False, "list": output})


def submit_ballot(request):
    if request.method != 'POST':
        messages.error(request, "Invalid request")
        return redirect(reverse('show_ballot'))

    voter = request.user.voter

    if voter.voted:
        messages.error(request, "You have already voted")
        return redirect(reverse('voterDashboard'))

    form = dict(request.POST)
    form.pop('csrfmiddlewaretoken', None)
    form.pop('submit_vote', None)

    if not form:
        logger.warning(f"User {voter.admin.email} submitted empty ballot")
        messages.error(request, "Please select at least one candidate")
        return redirect(reverse('show_ballot'))

    vote_count = 0

    for position in Position.objects.all():
        key = slugify(position.name)
        values = form.get(key) or form.get(f"{key}[]")

        if not values:
            continue

        if not isinstance(values, list):
            values = [values[0]]

        if len(values) > position.max_vote:
            messages.error(
                request,
                f"You can only select {position.max_vote} for {position.name}"
            )
            return redirect(reverse('show_ballot'))

        for cid in values:
            candidate = Candidate.objects.filter(id=cid).first()
            if candidate:
                Votes.objects.create(
                    voter=voter,
                    position=position,
                    candidate=candidate
                )
                vote_count += 1

    if vote_count == 0:
        messages.error(request, "No votes recorded")
        return redirect(reverse('show_ballot'))

    voter.voted = True
    voter.save()

    messages.success(request, "Thanks for voting!")
    return redirect(reverse('voterDashboard'))
