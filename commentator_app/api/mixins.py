from rest_framework.pagination import PageNumberPagination


class PaginationMixin(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 25

    def __init__(self, *args, **kwargs):
        super(PaginationMixin, self).__init__(*args, **kwargs)
