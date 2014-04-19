from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.shortcuts import render, render_to_response
# Create your views here.
from poll.models import Vote


def vote(request, submission_id):
    # if request.method != "POST":
    #     return HttpResponseBadRequest('Must be a POST')
    try:
        Vote(user=request.user.id, submission=submission_id).save()
    except:
        return HttpResponseForbidden({'error:': 'Already voted on this pic'})
    return render_to_response({'status': 'ok'})