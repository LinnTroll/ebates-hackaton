$(function () {
    var $tabs_el = $('[data-current-tab]');
    var current_tab = $tabs_el.data('currentTab');
    if (current_tab) {
        var $sel_tab = $('.nav-tabs [data-tab=' + current_tab + ']');
        var round_trip = $('[name=roundTripValue]').val();
        setTimeout(function () {
            $sel_tab.trigger('click');
            if (round_trip != 'true') {
                $('.oneWay_btn').trigger('click');
            }
        }, 10);
    }

    var $search = $('.cityairportsearch');
    $search.autocomplete({
        source: function (request, response) {
            $.getJSON('/api/airports/list/', request, function (data, status, xhr) {
                response(data.map(function (item) {
                    return {
                        label: item.pk + ' - ' + item.fields.name,
                        value: item.pk + ' - ' + item.fields.name,
                        pk: item.pk
                    };
                }));
            });
        },
        minLength: 1,
        select: function (event, data) {
            var $input = $(event.target);
            $input.parent().find('.flight_info').val(data.item.pk);
        },
    });

    var $datepicker = $('.datepicker');
    $datepicker.datepicker({
        dateFormat: 'dd/mm/yy'
    });
});