// js
$(document).ready(function() {
    // da
    $.ajax({
        url:'/sale/profit/',
        dataType: 'json',
        success: function(data) {
            $('#profit').html(data.html);
        }
    })
});