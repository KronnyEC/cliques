from notify.models import Notification
from website.utils import render_to_json


def get_notifications(request):
    notifications = Notification(user=request.user).values_list(
        'text', 'type', 'method', 'created_at', flat=True)
    return render_to_json(request, {'notifications': notifications})
