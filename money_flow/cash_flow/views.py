from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic.base import ContextMixin
from typing import Optional, List

from .models import CashFlow, Status, Type, Category, Subcategory
from .forms import (
    CashFlowForm, StatusForm,
    TypeForm, CategoryForm,
    SubcategoryForm
)


class MessageMixin:
    """
    Миксин для добавления сообщений пользователю после выполнения действий.
    Упрощает добавление единообразных сообщений в представлениях.
    """
    success_message: Optional[str] = None

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if self.success_message:
            messages.success(request, self.success_message)
        return response


class FilterMixin(ContextMixin):
    """
    Миксин для добавления фильтров в представления списков.
    Упрощает обработку параметров фильтрации.
    """
    filter_fields: List[str] = []

    def get_queryset(self):
        """
        Применяет фильтры к базовому queryset на основе GET-параметров.
        Если параметр находится в filter_fields и присутствует в GET-запросе,
        применяет соответствующий фильтр к queryset.
        """
        queryset = super().get_queryset()

        for field in self.filter_fields:
            value = self.request.GET.get(field)
            if value:
                filter_kwargs = {field: value}
                queryset = queryset.filter(**filter_kwargs)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавляет параметры фильтрации в контекст шаблона.
        """
        context = super().get_context_data(**kwargs)

        filters = {}
        for field in self.filter_fields:
            filters[field] = self.request.GET.get(field, '')

        context['filters'] = filters
        return context


class CashFlowListView(FilterMixin, ListView):
    """
    Представление для отображения списка записей о движении денежных средств.
    Поддерживает фильтрацию по датам, статусу, типу, категории и подкатегории.
    """
    model = CashFlow
    template_name = 'cash_flow/cashflow_list.html'
    context_object_name = 'cashflows'
    paginate_by = 10
    filter_fields = ['status', 'type', 'category', 'subcategory']

    def get_queryset(self):
        """
        Расширяет базовую фильтрацию, добавляя поддержку диапазонов дат,
        которые не могут быть обработаны стандартным способом в FilterMixin.
        """
        queryset = super().get_queryset()

        # Фильтрация по диапазону дат
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            queryset = queryset.filter(date_created__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_created__lte=end_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем списки для выпадающих меню фильтров
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()

        # Добавляем параметры дат в контекст, т.к. они обрабатываются отдельно
        filters = context.get('filters', {})
        filters.update({
            'start_date': self.request.GET.get('start_date', ''),
            'end_date': self.request.GET.get('end_date', ''),
        })
        context['filters'] = filters

        return context


class CashFlowCreateView(MessageMixin, CreateView):
    """Представление для создания новой записи о движении денежных средств."""
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cash_flow/cashflow_form.html'
    success_url = reverse_lazy('cashflow_list')
    success_message = 'Запись успешно создана.'


class CashFlowUpdateView(MessageMixin, UpdateView):
    """Представление для редактирования записи о движении денежных средств."""
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cash_flow/cashflow_form.html'
    success_url = reverse_lazy('cashflow_list')
    success_message = 'Запись успешно обновлена.'


class CashFlowDeleteView(MessageMixin, DeleteView):
    """Представление для удаления записи о движении денежных средств."""
    model = CashFlow
    template_name = 'cash_flow/cashflow_confirm_delete.html'
    success_url = reverse_lazy('cashflow_list')
    success_message = 'Запись успешно удалена.'


class StatusListView(ListView):
    """Представление для отображения списка статусов."""
    model = Status
    template_name = 'cash_flow/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(MessageMixin, CreateView):
    """Представление для создания нового статуса."""
    model = Status
    form_class = StatusForm
    template_name = 'cash_flow/status_form.html'
    success_url = reverse_lazy('status_list')
    success_message = 'Статус успешно создан.'


class StatusUpdateView(MessageMixin, UpdateView):
    """Представление для редактирования статуса."""
    model = Status
    form_class = StatusForm
    template_name = 'cash_flow/status_form.html'
    success_url = reverse_lazy('status_list')
    success_message = 'Статус успешно обновлен.'


class StatusDeleteView(MessageMixin, DeleteView):
    """Представление для удаления статуса."""
    model = Status
    template_name = 'cash_flow/status_confirm_delete.html'
    success_url = reverse_lazy('status_list')
    success_message = 'Статус успешно удален.'


class TypeListView(ListView):
    """Представление для отображения списка типов."""
    model = Type
    template_name = 'cash_flow/type_list.html'
    context_object_name = 'types'


class TypeCreateView(MessageMixin, CreateView):
    """Представление для создания нового типа."""
    model = Type
    form_class = TypeForm
    template_name = 'cash_flow/type_form.html'
    success_url = reverse_lazy('type_list')
    success_message = 'Тип успешно создан.'


class TypeUpdateView(MessageMixin, UpdateView):
    """Представление для редактирования типа."""
    model = Type
    form_class = TypeForm
    template_name = 'cash_flow/type_form.html'
    success_url = reverse_lazy('type_list')
    success_message = 'Тип успешно обновлен.'


class TypeDeleteView(MessageMixin, DeleteView):
    """Представление для удаления типа."""
    model = Type
    template_name = 'cash_flow/type_confirm_delete.html'
    success_url = reverse_lazy('type_list')
    success_message = 'Тип успешно удален.'


class CategoryListView(ListView):
    """Представление для отображения списка категорий."""
    model = Category
    template_name = 'cash_flow/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """Оптимизация запроса с использованием select_related."""
        return Category.objects.select_related('type').all()


class CategoryCreateView(MessageMixin, CreateView):
    """Представление для создания новой категории."""
    model = Category
    form_class = CategoryForm
    template_name = 'cash_flow/category_form.html'
    success_url = reverse_lazy('category_list')
    success_message = 'Категория успешно создана.'


class CategoryUpdateView(MessageMixin, UpdateView):
    """Представление для редактирования категории."""
    model = Category
    form_class = CategoryForm
    template_name = 'cash_flow/category_form.html'
    success_url = reverse_lazy('category_list')
    success_message = 'Категория успешно обновлена.'


class CategoryDeleteView(MessageMixin, DeleteView):
    """Представление для удаления категории."""
    model = Category
    template_name = 'cash_flow/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    success_message = 'Категория успешно удалена.'


class SubcategoryListView(ListView):
    """Представление для отображения списка подкатегорий."""
    model = Subcategory
    template_name = 'cash_flow/subcategory_list.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        return Subcategory.objects.select_related(
            'category', 'category__type'
        ).all()


class SubcategoryCreateView(MessageMixin, CreateView):
    """Представление для создания новой подкатегории."""
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'cash_flow/subcategory_form.html'
    success_url = reverse_lazy('subcategory_list')
    success_message = 'Подкатегория успешно создана.'


class SubcategoryUpdateView(MessageMixin, UpdateView):
    """Представление для редактирования подкатегории."""
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'cash_flow/subcategory_form.html'
    success_url = reverse_lazy('subcategory_list')
    success_message = 'Подкатегория успешно обновлена.'


class SubcategoryDeleteView(MessageMixin, DeleteView):
    """Представление для удаления подкатегории."""
    model = Subcategory
    template_name = 'cash_flow/subcategory_confirm_delete.html'
    success_url = reverse_lazy('subcategory_list')
    success_message = 'Подкатегория успешно удалена.'


# AJAX представления для зависимых выпадающих списков
def get_categories_by_type(request):
    """
    Возвращает категории, связанные с выбранным типом.

    Используется для динамического обновления выпадающего списка категорий
    при изменении типа в формах.
    """
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)


def get_subcategories_by_category(request):
    """
    Возвращает подкатегории, связанные с выбранной категорией.

    Используется для динамического обновления выпадающего списка подкатегорий
    при изменении категории в формах.
    """
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(
        category_id=category_id
    ).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)


def index(request):
    return redirect('cashflow_list')
