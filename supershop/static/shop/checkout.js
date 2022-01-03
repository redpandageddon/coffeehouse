if($('input').is('#id_address')) {
    document.getElementById('id_address').placeholder = 'Адрес';
    document.getElementById('id_order_date').placeholder = 'Дата получения заказа';
    $('#id_order_date').wrap('<div class = "date-rec"></div>');
    $('#id_order_date').attr('type', 'text');
    $('#id_order_date').on('click', function() {
        $('#id_order_date').attr('type', 'date');
    });
}