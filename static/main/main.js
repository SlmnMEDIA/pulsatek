// js
$(document).ready(function() {
    $('.ui.dropdown').dropdown();
    
    $('.ui.sidebar').sidebar('toggle');

    // da
    function call_profit() {
        $.ajax({
            url:'/sale/profit/',
            dataType: 'json',
            success: function(data) {
                $('.profit').html(data.html);
            }
        });
        return false;
    };


    $('.bars').click(function() {
        $('.ui.sidebar').sidebar('toggle');
    });


    call_profit();
});