from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        page_number = self.page.number
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count_objects": self.page.paginator.count,
                "page_number": page_number,
                "results": data,
                "pages": self.page.paginator.get_elided_page_range(
                    page_number, on_each_side=2, on_ends=1
                ),
            }
        )
