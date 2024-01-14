from users.models import Subscription


def get_is_subscribed(self, obj):
    request = self.context.get('request')
    if request is None or request.user.is_anonymous:
        return False
    return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()
