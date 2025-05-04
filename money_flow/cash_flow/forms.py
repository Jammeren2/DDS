from django import forms
from .models import CashFlow, Status, Type, Category, Subcategory
import datetime


class CashFlowForm(forms.ModelForm):
    """
    Форма для создания и редактирования записей о движении денежных средств.
    """

    class Meta:
        model = CashFlow
        fields = [
            'date_created', 'status', 'type',
            'category', 'subcategory',
            'amount', 'comment'
        ]
        widgets = {
            'date_created': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0.01'
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.initial.get('date_created'):
            self.initial['date_created'] = datetime.date.today()

        # Если это новая запись (не редактирование)
        if not self.instance.pk:
            # Устанавливаем пустой queryset для категорий и подкатегорий
            self.fields['category'].queryset = Category.objects.none()
            self.fields['subcategory'].queryset = Subcategory.objects.none()
            
            # Если в данных формы уже есть type_id (например, при повторной отправке формы с ошибкой)
            if 'type' in self.data:
                try:
                    type_id = int(self.data.get('type'))
                    self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
                except (ValueError, TypeError):
                    pass
                    
            # Если в данных формы уже есть category_id
            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
                except (ValueError, TypeError):
                    pass
        else:
            # Для существующей записи
            if self.instance.type:
                self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)
            else:
                self.fields['category'].queryset = Category.objects.none()
                
            if self.instance.category:
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
            else:
                self.fields['subcategory'].queryset = Subcategory.objects.none()


class StatusForm(forms.ModelForm):
    """Форма для создания и редактирования статусов."""

    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TypeForm(forms.ModelForm):
    """Форма для создания и редактирования типов."""

    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    """Форма для создания и редактирования категорий."""

    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }


class SubcategoryForm(forms.ModelForm):
    """Форма для создания и редактирования подкатегорий."""

    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
