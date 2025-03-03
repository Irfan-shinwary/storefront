from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    PAGE_SIZE=10