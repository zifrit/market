class UserGroupsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, "user") and request.user.is_authenticated:
            user_groups = list(request.user.groups.values_list("name", flat=True))
            request.user_groups_name = user_groups
        else:
            request.user_groups_name = []

        response = self.get_response(request)
        return response
