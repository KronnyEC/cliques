from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from invite_only.models import InviteCode


class InviteOnlyAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        invite_code = self._get_invite(request)
        # If None, return False
        return invite_code is not None

    def stash_verified_email(self, request, email):
        request.session['account_verified_email'] = email

    def is_email_verified(self, request, email):
        return True

    def save_user(self, request, user, form, commit=True):
        super(InviteAccountAdapter).save_user(request, user, form, commit=True)

    def _get_invite(self, request):
        """
        Returns the InviteCode object or None if it doesn't exist
        """
        invite_code = request.GET.get('invite_code')
        try:
            return InviteCode.objects.get(code=invite_code)
        except (InviteCode.MultipleObjectsReturned, InviteCode.DoesNotExist):
            return None
