import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from website.models import UserProfile
from website.utils import render_to_json

logger = logging.getLogger(__name__)


@api_view(['GET'])
def get_token(request):
    user = UserProfile.objects.get(id=  request.user.id)
    token = Token.objects.get_or_create(user=user)
    return render_to_json(request, {
        'id': request.user.id,
        'username': request.user.username,
        'token': token[0].key
    })


def get_cookie(request):
    # A way for Angular to get the CSRF cookie
    return render_to_json(request, {'user_id': request.user.id})


@api_view(['POST'])
def check_in(request):
    print "CHECKIN", request.user
    request.user.save()
    logger.info('{} checked in '.format(request.user))
    return HttpResponse(status=201)
