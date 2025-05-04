from rest_framework import serializers
from .models import Status, Type, Category, Subcategory, CashFlow


class StatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Status.
    Преобразует объекты Status в JSON и обратно.
    """
    class Meta:
        model = Status
        fields = ['id', 'name']


class TypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Type.
    Преобразует объекты Type в JSON и обратно.
    """
    class Meta:
        model = Type
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    Включает информацию о связанном типе.
    """
    type_name = serializers.StringRelatedField(source='type', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'type_name']


class SubcategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Subcategory.
    Включает информацию о связанной категории.
    """
    category_name = serializers.StringRelatedField(
        source='category',
        read_only=True
    )

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category', 'category_name']


class CashFlowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CashFlow.
    Включает информацию о связанных объектах и допускает вложенное создание.
    """
    status_name = serializers.StringRelatedField(
        source='status', read_only=True
    )
    type_name = serializers.StringRelatedField(source='type', read_only=True)
    category_name = serializers.StringRelatedField(
        source='category',
        read_only=True
    )
    subcategory_name = serializers.StringRelatedField(
        source='subcategory',
        read_only=True
    )

    class Meta:
        model = CashFlow
        fields = [
            'id', 'date_created', 'status', 'status_name',
            'type', 'type_name', 'category', 'category_name',
            'subcategory', 'subcategory_name', 'amount', 'comment'
        ]
