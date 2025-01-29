from accounts.models import User


def user_exists(**kwargs):
    return User.objects.filter(**kwargs).exists()


def get_user(**kwargs):
    return User.objects.get(**kwargs)
