import logging

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from chat_server.models import ChatSession


logger = logging.getLogger()

@csrf_exempt
@login_required
def connect(request):
    logger.info("{} connected".format(request.user.username))
    try:
        session_key = ChatSession.objects.get(user=request.user.id).session_key
    except Exception:
        logger.exception("chat connection failed")
        return
    logger.info("Connect, token {}".format(session_key))


@csrf_exempt
@login_required
def disconnect(request):
    logger.info("{} disconnected".format(request.user.username))