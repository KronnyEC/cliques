from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from website.utils import render_to_json


@csrf_exempt
@login_required
def get_token(request):
    token = Token.objects.get_or_create(user=request.user)
    return render_to_json(request, {
        'id': request.user.id,
        'username': request.user.username,
        'token': token[0].key
    })


def get_cookie(request):
    # A way for Angular to get the CSRF cookie
    return render_to_json(request, {'user_id': request.user.id})