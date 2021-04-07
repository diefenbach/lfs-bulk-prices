"use strict";

let BP = {};

function bulk_price_row() {
    let id = (new Date).getTime();

    let vals = [];
    $(".bulk-price input.amount").each(function(index, item) {
        vals.push($(item).val().replace(",", "."));
    });
    let max = Math.max.apply(null, vals) + 1;

    let row =  '<tr class="bulk-price">' +
               '<td class="number">' +
               '<input type="hidden" name="price_id" value="' + id + '" />' +
               '<input type="text" class="number amount" name="amount-' + id + '" value="' + max + '" /> ' + BP.price_unit +
               '</td>' +
               '<td class="number">' +
               '<input type="text" class="price-absolute price-absolute-' + id + ' right" name="price_absolute-' + id + '" value="0,0" /> ' + BP.currency +
               '</td>' +
               '<td class="number">' +
               '<input type="text" class="price-percentual price-percentual-' + id + ' right " name="price_percentual-' + id + '" value="0,0" /> %' +
               '</td>' +
               '<td class="right">' +
               '<a href="" class="delete-bulk-price-button"><img src="/static/lfs/icons/delete.png" alt="Add"></a>' +
               '</td>' +
               '</tr>';
    return row;
}

function calculate_absolute_prices(basePrice) {
    $(".price-absolute").each(function(index, item) {
        if (!$(item).hasClass("first")) {
            let id = $(item).attr("name").split("-")[1];
            let percent = $(".price-percentual-" + id).val().replace(",", ".");
            let price = ((basePrice / 100) * percent).toFixed(2).replace(".", ",");
            $(".price-absolute-" + id).val(price);
        }
    });
}

function calculate_percentual_price(priceAbsolute) {
    let absolute = +priceAbsolute.val().replace(',', '.');
    let base = $(".price-absolute.first").val().replace(",", ".");
    let id = priceAbsolute.attr("name").split("-")[1];
    let price = ((absolute / base) * 100).toFixed(2).replace(".", ",");
    $(".price-percentual-" + id).val(price)

}

function calculate_absolute_price(price_percentual) {
    let percent = +price_percentual.val().replace(',', '.');
    let base = $(".price-absolute.first").val().replace(",", ".");
    let id = price_percentual.attr("name").split("-")[1];
    let price = ((base / 100) * percent).toFixed(2).replace(".", ",");
    $(".price-absolute-" + id).val(price)
}


$(function() {
    $(document).on('click', '.delete-bulk-price-button', function() {
        $(this).parents("tr.bulk-price:first").remove();
        return false;
    });

    $(document).on("click", ".add-bulk-price-button", function() {
        let row = $("tr.bulk-price").last();
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
        let firstPrice = $(this).val().replace(',', '.')
        calculate_absolute_prices(+firstPrice);
    });

});
