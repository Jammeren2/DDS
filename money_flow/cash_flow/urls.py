from django.urls import path
from . import views


# Функция для создания стандартного набора CRUD URL-шаблонов
def crud_patterns(prefix, view_class_prefix, name_prefix):
    """
    Создает стандартный набор URL-шаблонов для CRUD операций.

    Args:
        prefix: Префикс URL (например, 'status/')
        view_class_prefix: Префикс класса представления (например, 'Status')
        name_prefix: Префикс имени URL-шаблона (например, 'status')

    Returns:
        Список URL-шаблонов для указанного ресурса
    """
    return [
        path(
            f'{prefix}',
            getattr(views, f'{view_class_prefix}ListView').as_view(),
            name=f'{name_prefix}_list'
        ),
        path(
            f'{prefix}create/', 
            getattr(views, f'{view_class_prefix}CreateView').as_view(),
            name=f'{name_prefix}_create'
        ),
        path(
            f'{prefix}<int:pk>/update/',
            getattr(views, f'{view_class_prefix}UpdateView').as_view(),
            name=f'{name_prefix}_update'
        ),
        path(
            f'{prefix}<int:pk>/delete/',
            getattr(views, f'{view_class_prefix}DeleteView').as_view(),
            name=f'{name_prefix}_delete'
        ),
    ]


urlpatterns = [
    path('', views.index, name='index'),
]

# Добавляем URL-шаблоны для каждого ресурса
urlpatterns.extend(crud_patterns('cashflow/', 'CashFlow', 'cashflow'))
urlpatterns.extend(crud_patterns('status/', 'Status', 'status'))
urlpatterns.extend(crud_patterns('type/', 'Type', 'type'))
urlpatterns.extend(crud_patterns('category/', 'Category', 'category'))
urlpatterns.extend(crud_patterns('subcategory/', 'Subcategory', 'subcategory'))

# AJAX URL-шаблоны
urlpatterns.extend([
    path(
        'ajax/categories/',
        views.get_categories_by_type,
        name='ajax_categories'
    ),
    path(
        'ajax/subcategories/',
        views.get_subcategories_by_category,
        name='ajax_subcategories'
    ),
])
