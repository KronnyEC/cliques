from notify.models import Notification
from website.models import UserProfile


def notify_users(user_ids, from_user, text, link, type, level):
        notifications = []
        for user in user_ids:
            notifications.append(Notification(user_id=user,
                                              from_user=from_user,
                                              text=text,
                                              type=type,
                                              link=link,
                                              level=level))
        Notification.objects.bulk_create(notifications)


def find_pings(text, sending_user, notification_type, level='info'):
    # Look for highlights
    usernames = UserProfile.objects.all().values('username')
    for username in usernames:
        if username.lower() in text.lower():
            # Don't notify self
            if sending_user.username == username:
                continue
            # Notify the user they've been pinged
            user = UserProfile.objects.get(username=username)
            Notification(text="{}: {}".format(username, text),
                         user=user,
                         type=notification_type,
                         level=level).save()