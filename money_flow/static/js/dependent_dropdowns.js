/**
 * Скрипт для обработки зависимых выпадающих списков
 */
$(document).ready(function() {
    // Обработка изменения типа для фильтрации категорий
    $('#id_type').change(function() {
        var typeId = $(this).val();
        if (typeId) {
            $.ajax({
                url: "/cash_flow/ajax/categories/",
                data: {
                    'type_id': typeId
                },
                dataType: 'json',
                success: function(data) {
                    $('#id_category').html('<option value="">---------</option>');
                    $('#id_subcategory').html('<option value="">---------</option>');
                    $.each(data, function(key, value) {
                        $('#id_category').append('<option value="' + value.id + '">' + value.name + '</option>');
                    });
                }
            });
        } else {
            $('#id_category').html('<option value="">---------</option>');
            $('#id_subcategory').html('<option value="">---------</option>');
        }
    });

    // Обработка изменения категории для фильтрации подкатегорий
    $('#id_category').change(function() {
        var categoryId = $(this).val();
        if (categoryId) {
            $.ajax({
                url: "/cash_flow/ajax/subcategories/",
                data: {
                    'category_id': categoryId
                },
                dataType: 'json',
                success: function(data) {
                    $('#id_subcategory').html('<option value="">---------</option>');
                    $.each(data, function(key, value) {
                        $('#id_subcategory').append('<option value="' + value.id + '">' + value.name + '</option>');
                    });
                }
            });
        } else {
            $('#id_subcategory').html('<option value="">---------</option>');
        }
    });
});