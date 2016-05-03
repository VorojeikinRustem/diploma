$(document).ready(function () {

    $('[data-shop="size"]:first-child > input[type="radio"]').click() 
    $('[data-slider="img"]').click(function () {
    $(this).toggleClass('img-full');
    });


    // order_status_form
    $('[data-order="order_id"]').on('input',function(){
        if ($('[data-order="phone"]').val() != '') {
            $('[data-order="btn"]').prop("disabled", false);
        }
    });
    $('[data-order="phone"]').on('input',function(){
        if ($('[data-order="order_id"]').val() != '') {
            $('[data-order="btn"]').prop("disabled", false);
        }
    });

});