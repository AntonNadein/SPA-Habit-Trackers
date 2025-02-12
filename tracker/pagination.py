from rest_framework.pagination import PageNumberPagination


class TrackerPagination(PageNumberPagination):
    """Класс настроек пагинации"""

    page_size = 5
