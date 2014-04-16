from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from google.appengine.api import channel
import logging
from django.views.decorators.csrf import csrf_exempt
from chat_server.models import ChatUser, ChatMessage
from django.core.serializers.json import DjangoJSONEncoder

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
    # channel.send_message(request.user.username, '[system] Connected! Welcome to the prototype '
    #                             'chat system.')

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
    return list(ChatMessage.objects.order_by('-sent')[start:end]
                .values_list('user__username', 'message', 'sent'))


@csrf_exempt
@login_required
def join_chat(request):
    token = channel.create_channel(request.user.username, 24*60)
    logger.info("Created token {} for {}".format(token, request.user.username))
    chat_user, created = ChatUser.objects.get_or_create(user=request.user)
    chat_user.token = token
    chat_user.save()
    # channel.send_message(request.user.username,
    #                      '[system] Joined the Slashertraxx chat room.')
    return render_to_json(request, {'token': token,
                                    'msgs': _get_messages(0, 20)})


@csrf_exempt
@login_required
def receive(request):
    logging.info("recieved chat msg from {}".format(request.user.username))
    for chat_user in ChatUser.objects.all():
        msg = "{}: {}".format(request.user.username, request.POST['msg'])
        logger.info("Sending {} to {}".format(chat_user.token, msg))
        channel.send_message(chat_user.token, msg)
    chat_message = ChatMessage(user=request.user, message=request.POST['msg'])
    chat_message.save()
    return HttpResponse('OK')


def render_to_json(request, data):
    # msgs = {}
    # messages_list = messages.get_messages(request)
    # count = 0
    # for message in messages_list:
    #     msgs[count] = {'message': message.message, 'level': message.level}
    #     count += 1
    # data['messages'] = msgs
    return HttpResponse(
        json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder),
        content_type=request.is_ajax() and "application/json" or "text/html"
    )