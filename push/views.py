import logging

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger()

@csrf_exempt
@login_required
def connect(request):
    logger.info("{} connected".format(request.user.username))


@csrf_exempt
@login_required
def disconnect(request):
    logger.info("{} disconnected".format(request.user.username))