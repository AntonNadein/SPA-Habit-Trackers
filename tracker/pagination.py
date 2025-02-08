from rest_framework.pagination import PageNumberPagination


class TrackerPagination(PageNumberPagination):
    page_size = 5
