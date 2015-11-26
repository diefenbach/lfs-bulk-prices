"use strict";

$(function() {
    $(".product input[name=quantity]").on("change", function() {
        var url = $(this).attr("bulk_prices_update_url");
        var amount = $(this).val();
        $.get(url, {"amount": amount}, function(data) {
            $(".standard-price-value").html(data["standard_price"]);
            $(".base-price .money").html(data["base_price"]);
        });
    });
});
