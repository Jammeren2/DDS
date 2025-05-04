from django.db import models
from django.core.validators import MinValueValidator


class Status(models.Model):
    """Модель для хранения статусов движения денежных средств."""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название"
    )

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Type(models.Model):
    """Модель для хранения типов движения денежных средств."""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название"
    )

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для хранения категорий движения денежных средств."""
    name = models.CharField(max_length=100, verbose_name="Название")
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name="Тип"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
        unique_together = ['name', 'type']

    def __str__(self):
        return f"{self.name} ({self.type})"


class Subcategory(models.Model):
    """Модель для хранения подкатегорий движения денежных средств."""
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['name']
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} ({self.category})"


class CashFlow(models.Model):
    """Модель для хранения записей о движении денежных средств."""
    date_created = models.DateField(verbose_name="Дата создания")
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name="Статус"
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        verbose_name="Тип"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Сумма (руб.)"
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий"
    )

    class Meta:
        verbose_name = "Движение денежных средств"
        verbose_name_plural = "Движение денежных средств"
        ordering = ['-date_created']

    def __str__(self):
        return (
            f"{self.date_created} - {self.type}"
            f" - {self.category} - {self.amount} руб."
        )
