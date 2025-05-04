from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Status, Type, Category, Subcategory, CashFlow
from .serializers import (
    StatusSerializer, TypeSerializer,
    CategorySerializer, SubcategorySerializer,
    CashFlowSerializer
)


class StatusViewSet(viewsets.ModelViewSet):
    """
    API для управления статусами.

    Поддерживает стандартные CRUD-операции:
    - GET /api/statuses/ - получить список статусов
    - POST /api/statuses/ - создать новый статус
    - GET /api/statuses/{id}/ - получить статус по ID
    - PUT /api/statuses/{id}/ - обновить статус
    - DELETE /api/statuses/{id}/ - удалить статус
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


class TypeViewSet(viewsets.ModelViewSet):
    """
    API для управления типами движения денежных средств.

    Поддерживает стандартные CRUD-операции:
    - GET /api/types/ - получить список типов
    - POST /api/types/ - создать новый тип
    - GET /api/types/{id}/ - получить тип по ID
    - PUT /api/types/{id}/ - обновить тип
    - DELETE /api/types/{id}/ - удалить тип
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API для управления категориями.

    Поддерживает стандартные CRUD-операции и фильтрацию по типу.
    """
    queryset = Category.objects.select_related('type').all()
    serializer_class = CategorySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['type']
    search_fields = ['name']
    ordering_fields = ['name', 'type__name']


class SubcategoryViewSet(viewsets.ModelViewSet):
    """
    API для управления подкатегориями.

    Поддерживает стандартные CRUD-операции и фильтрацию по категории.
    """
    queryset = Subcategory.objects.select_related(
        'category', 'category__type'
    ).all()
    serializer_class = SubcategorySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['category', 'category__type']
    search_fields = ['name']
    ordering_fields = ['name', 'category__name']


class CashFlowViewSet(viewsets.ModelViewSet):
    """
    API для управления движением денежных средств.

    Поддерживает стандартные CRUD-операции и расширенную фильтрацию.
    """
    queryset = CashFlow.objects.select_related(
        'status', 'type', 'category', 'subcategory'
    ).all()
    serializer_class = CashFlowSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = [
        'date_created', 'status', 'type',
        'category', 'subcategory'
    ]
    search_fields = ['comment']
    ordering_fields = [
        'date_created', 'status__name', 'type__name',
        'category__name', 'subcategory__name', 'amount'
    ]
