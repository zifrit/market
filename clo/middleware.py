from django.utils.functional import SimpleLazyObject


class UserGroupsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user_groups_name = SimpleLazyObject(
            lambda: get_user_groups(request.user)
        )
        response = self.get_response(request)
        return response


def get_user_groups(user):
    if user.is_authenticated:
        return list(user.groups.values_list("name", flat=True))
    return []
