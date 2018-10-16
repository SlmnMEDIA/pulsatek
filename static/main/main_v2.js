// js
$(document).ready(function() {
    $('.ui.dropdown').dropdown();
    
    // da
    $.ajax({
        url:'/sale/profit/',
        dataType: 'json',
        success: function(data) {
            $('#profit').html(data.html);
        }
    });

});