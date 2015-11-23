"use strict";
function bulk_price_row() {
    var id = (new Date).getTime();
    var row =  '<tr class="bulk-price">' +
               '<td class="number">' +
               '<input type="hidden" name="price_id" value="' + id + '" />' +
               '<input type="text" class="number" name="amount-' + id + '" value="0" />' +
               '</td>' +
               '<td class="number">' +
               '<input type="text" class="price-absolute price-absolute-' + id + ' right" name="price_absolute-' + id + '" value="0" />' +
               '</td>' +
               '<td class="number">' +
               '<input type="text" class="price-percentual price-percentual-' + id + ' right " name="price_percentual-' + id + '" value="0" /> %' +
               '</td>' +
               '<td class="right">' +
               '<a href="" class="add-bulk-price-button"><img src="/static/lfs/icons/add.png" alt="Add"></a> ' +
               '<a href="" class="delete-bulk-price-button"><img src="/static/lfs/icons/delete.png" alt="Add"></a>' +
               '</td>' +
               '</tr>';
    return row;
};

function calculate_absolute_prices(new_price) {
    $(".price-absolute").each(function(index, item) {
        if (!$(item).hasClass("first")) {
            var id = $(item).attr("name").split("-")[1];
            var percent = $(".price-percentual-" + id).val();
            console.log(new_price, percent);
            var price = ((new_price / 100) * percent).toFixed(1);
            $(".price-absolute-" + id).val(price);
        }
    });
};

function calculate_percentual_price(price_absolute) {
    var absolute = price_absolute.val();
    var base = $(".price-absolute.first").val();
    var id = price_absolute.attr("name").split("-")[1];
    var price = ((absolute / base) * 100).toFixed(2);
    $(".price-percentual-" + id).val(price)

};

function calculate_absolute_price(price_percentual) {
    var percent = price_percentual.val();
    var base = $(".price-absolute.first").val();
    var id = price_percentual.attr("name").split("-")[1];
    var price = ((base / 100) * percent).toFixed(1);
    $(".price-absolute-" + id).val(price)
};


$(function() {
    $(document).on('click', '.delete-bulk-price-button', function() {
        $(this).parents("tr.bulk-price:first").remove();
        return false;
    });

    $(document).on("click", ".add-bulk-price-button", function() {
        var row = $(this).parents("tr.bulk-price");
        row.after(bulk_price_row());
        return false;
    });

    $(document).on("click", ".delete-bulk-price-button", function() {
        $(this).parents("tr.bulk-price").remove();
        return false;
    });

    $(document).on("change", ".price-percentual", function() {
        calculate_absolute_price($(this));
    });

    $(document).on("change", ".price-absolute", function() {
        calculate_percentual_price($(this));
    });

    $(document).on("change", ".price-absolute.first", function() {
        calculate_absolute_prices($(this).val());
    });

});
