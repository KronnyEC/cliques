from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.shortcuts import render, render_to_response
# Create your views here.
from django.views.generic import CreateView
from poll.models import Vote, Submission


def vote(request, submission_id):
    # if request.method != "POST":
    #     return HttpResponseBadRequest('Must be a POST')
    try:
        Vote(user=request.user.id, submission=submission_id).save()
    except:
        return HttpResponseForbidden({'error:': 'Already voted on this pic'})
    return render_to_response({'status': 'ok'})


def cron(request):
    pass


class SubmissionCreateView(CreateView):
    model = Submission
    fields = ['title', 'url']