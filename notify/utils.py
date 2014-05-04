from notify.models import Notification


def notify_users(user_ids, text, link, type, level):
        notifications = []
        for user in user_ids:
            notifications.append(Notification(user_id=user, text=text,
                                              type=type,
                                              link=link,
                                              level=level))
        Notification.objects.bulk_create(notifications)