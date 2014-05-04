import datetime
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from google.appengine.api import channel
import logging
from django.views.decorators.csrf import csrf_exempt
from chat_server.models import ChatUser, ChatMessage
from website.utils import render_to_json

logger = logging.getLogger()


# Create your views here.
@csrf_exempt
@login_required
def connect(request):
    logger.info("{} connected".format(request.user.username))
    try:
        token = ChatUser.objects.get(user=request.user.id).token
    except Exception:
        return
    logger.info("Connect, token {}".format(token))


@csrf_exempt
@login_required
def disconnect(request):
    logger.info("{} disconnected".format(request.user.username))


@csrf_exempt
@login_required
def get_messages(request, start, end):
    messages = _get_messages(start, end)
    return render_to_json(request, {'msgs': messages})


def _get_messages(start, end):
    """Get messages (in reverse chronological order) from start to end,
    0 indexed
    """
    return list(reversed(ChatMessage.objects.order_by('-sent')[start:end]
                .values_list("user__username", "message", "sent")))


def _get_connected_users():
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    five_mins_ago = now - datetime.timedelta(minutes=5)
    return list(ChatUser.objects.filter(
        connected_at__gt=five_mins_ago).values_list("user__username",
                                                    flat=True))


@csrf_exempt
@login_required
def join_chat(request):
    token = channel.create_channel(request.user.username, 24 * 60)
    logger.info("Created token {} for {}".format(token, request.user.username))
    chat_user, created = ChatUser.objects.get_or_create(user=request.user)
    chat_user.token = token
    chat_user.save()
    connected_users = _get_connected_users()
    # channel.send_message(request.user.username,
    #                      '[system] Joined the Slashertraxx chat room.')
    return render_to_json(request, {'token': token,
                                    'msgs': _get_messages(0, 20),
                                    'connected_users': connected_users})


@csrf_exempt
@login_required
def check_in(request):
    try:
        ChatUser.objects.get(user=request.user).save()
    except ChatUser.DoesNotExist:
        pass
    return render_to_json(request, {'connected_users': _get_connected_users()})


@csrf_exempt
@login_required
def leave_chat(request):
    try:
        chat_user = ChatUser.objects.get(user=request.user)
        logger.info("{} left chat".format(chat_user.user.username))
        chat_user.delete()
    except ChatUser.DoesNotExist:
        pass
    return render_to_json(request, {'status': 'ok'})


@csrf_exempt
@login_required
def receive(request):
    logging.info("recieved chat msg from {}".format(request.user.username))
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    msg = json.dumps([request.user.username, request.POST['msg'],
           str(now)])
    for chat_user in ChatUser.objects.all():
        logger.info("Sending {} to {}".format(chat_user.token, msg))
        channel.send_message(chat_user.token, msg)
    chat_message = ChatMessage(user=request.user, message=request.POST['msg'])
    chat_message.save()
    return HttpResponse('OK')
