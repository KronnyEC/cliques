from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, render_to_response
# Create your views here.
from django.views.generic import CreateView, DetailView
from poll.models import Vote, Submission, SubmissionForm, Poll
import logging

logger = logging.getLogger()


def vote(request, poll_stub, submission_id):
    #TODO(pcsforeducation) make this AJAX and POST only.
    # if request.method != "POST":
    #     return HttpResponseBadRequest('Must be a POST')
    try:
        submission = Submission.objects.get(id=submission_id)
        vote_ob, created = Vote.objects.get_or_create(
            user=request.user, submission=submission)
    except:
        logging.exception('Already voted')
        return HttpResponseForbidden({'error:': 'Already voted on this pic'})
    if not created:
        vote_ob.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cron(request):
    pass


class PollDetailView(DetailView):
    model = Poll
    slug_field = 'stub'
    slug_url_kwarg = 'stub'
    template_name = 'poll/submission.html'

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        try:
            context['vote'] = Vote.objects.get(user=self.request.user.id)
        except Vote.DoesNotExist:
            pass
        context['form'] = SubmissionForm
        return context


class SubmissionFormView(CreateView):
    model = Submission
    success_url = '/'
    fields = ['title', 'url']
    # template_name = 'website/post.html'

    def form_valid(self, form):
        stub = self.kwargs.get('stub')
        user_model = get_user_model()
        form.instance.user = user_model.objects.get(id=self.request.user.id)
        form.instance.poll = Poll.objects.get(stub=stub)
        self.object = form.save()
        self.success_url = "/poll/{}/".format(stub)
        return super(SubmissionFormView, self).form_valid(form)

