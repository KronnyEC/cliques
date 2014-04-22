from collections import defaultdict
import operator
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, render_to_response
# Create your views here.
from django.views.generic import CreateView, DetailView
from poll.models import Vote, Submission, SubmissionForm, Poll
import logging
from website.models import Post, UserProfile

logger = logging.getLogger()


def vote(request, poll_stub, submission_id):
    #TODO(pcsforeducation) make this AJAX and POST only.
    # if request.method != "POST":
    #     return HttpResponseBadRequest('Must be a POST')
    try:
        submission = Submission.objects.get(id=submission_id)
    except:
        return HttpResponseNotFound("Submission does not exist: {}".format(
            submission_id
        ))
    try:
        prev_vote = Vote.objects.get(user=request.user)
    except Vote.DoesNotExist:
        # First vote
        Vote(user=request.user, submission=submission).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    try:
        # Switch vote or undo vote
        if prev_vote.submission == submission:
            # Undo
            prev_vote.delete()
        else:
            # Switch
            prev_vote.delete()
            Vote(user=request.user, submission=submission).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        logging.exception('Could not switch vote')
        raise


def cron(request):
    # Get all the votes (may need to improve filtering on poll here).
    #TODO(pcsforeducation) support multiple polls
    poll = Poll.objects.all()[0]
    submissions = defaultdict(int)
    votes = Vote.objects.all()
    for vote in votes:
        submissions[vote.submission.id] += 1
    # Eww.
    top_submissions = list(reversed(sorted(submissions.iteritems(),
                                    key=operator.itemgetter(1))))
    logging.info("Top submissions: {}".format(top_submissions))
    if top_submissions:
        top_votes = top_submissions[0][1]
        if top_votes > 0:
            for submission in top_submissions:
                logging.info("Testing submission: {}, top_votes: {}, equal? {}"
                             .format(submission, top_votes,
                                     submission[0] == top_votes))
                if submission[1] == top_votes:
                    _post_winning_submission(poll, submission[0])

        # Delete the votes
        votes.delete()
    return HttpResponse('ok')


def _post_winning_submission(poll, submission_id):
    user = UserProfile.objects.get(username=poll.bot_name)
    submission = Submission.objects.get(id=submission_id)
    post = Post(user=user,
                category=poll.category,
                title=poll.title,
                url=submission.url,
                type='image')
    post.save()


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

