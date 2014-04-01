from django import forms
from django.views.generic import CreateView, FormView
from invite_only.models import InviteForm


class InviteCodeView(FormView):
    name = forms.CharField()
    email = forms.EmailField()
    form_class = InviteForm
    template_name = "invite_only/invite.html"
    success_url = "/"

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            self.object = form.save(self.request.user)
        return super(InviteCodeView, self).form_valid(form)