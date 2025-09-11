"use strict";

// Global namespace set by template
window.BP = window.BP || {};

function qs(selector, root) {
    return (root || document).querySelector(selector);
}
function qsa(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
}
function closest(el, selector) {
    return el && (el.closest ? el.closest(selector) : null);
}

function decimalCommaToDot(s) {
    return String(s || "").replace(",", ".");
}
function decimalDotToComma(n) {
    return String(n).replace(".", ",");
}

function newRowId() {
    return String(new Date().getTime());
}

function updateTierNumbers() {
    var cards = qsa(".bulk-price-card");
    cards.forEach(function (card, index) {
        // Skip the first card (base price)
        if (index === 0) return;

        var header = qs(".card-header h6", card);
        if (header) {
            var icon = qs("i", header);
            if (icon) {
                header.innerHTML = '<i class="bi bi-tag-fill me-2"></i>Price Tier ' + (index + 1);
            }
        }
    });
}

function updateAddButtons() {
    var cards = qsa(".bulk-price-card");
    var headers = qsa(".bulk-price-card .card-header");

    // Remove all add buttons first
    qsa(".add-bulk-price-button").forEach(function (btn) {
        if (!btn.closest("#bulk-prices-content > .d-flex > .btn")) {
            btn.remove();
        }
    });

    // Add add button to the last card only
    if (cards.length > 0) {
        var lastCard = cards[cards.length - 1];
        var lastHeader = qs(".card-header", lastCard);
        var buttonContainer = qs(".d-flex", lastHeader);

        if (buttonContainer && !qs(".add-bulk-price-button", buttonContainer)) {
            var addBtn = document.createElement("button");
            addBtn.type = "button";
            addBtn.className = "btn btn-sm btn-outline-primary add-bulk-price-button";
            addBtn.title = "Add new price tier";
            addBtn.innerHTML = '<i class="bi bi-plus-circle"></i>';
            buttonContainer.insertBefore(addBtn, buttonContainer.firstChild);
        }
    }
}

function bulk_price_card() {
    var id = newRowId();
    var vals = [];
    qsa(".bulk-price-card input.amount").forEach(function (item) {
        vals.push(decimalCommaToDot(item.value));
    });
    var max = 1;
    if (vals.length) {
        try {
            max = Math.max.apply(null, vals.map(parseFloat)) + 1;
        } catch (e) {
            max = 1;
        }
    }

    var cardCount = qsa(".bulk-price-card").length;
    var tierNumber = cardCount + 1;

    var card = '' +
        '<div class="bulk-price-card card mb-3">' +
        '  <div class="card-header d-flex justify-content-between align-items-center">' +
        '    <h6 class="mb-0">' +
        '      <i class="bi bi-tag-fill me-2"></i>Price Tier ' + tierNumber +
        '    </h6>' +
        '    <div class="d-flex gap-2">' +
        '      <button type="button" class="btn btn-sm btn-outline-danger delete-bulk-price-button" title="Remove this price tier">' +
        '        <i class="bi bi-trash"></i>' +
        '      </button>' +
        '    </div>' +
        '  </div>' +
        '  <div class="card-body">' +
        '    <input type="hidden" name="price_id" value="' + id + '" />' +
        '    <div class="row g-3">' +
        '      <div class="col-md-4">' +
        '        <label class="form-label fw-semibold">Minimum Quantity</label>' +
        '        <div class="input-group">' +
        '          <input type="text" class="form-control number amount" name="amount-' + id + '" value="' + decimalDotToComma(max.toFixed ? max.toFixed(1) : max) + '" />' +
        '          <span class="input-group-text">' + (BP.price_unit || "") + '</span>' +
        '        </div>' +
        '      </div>' +
        '      <div class="col-md-4">' +
        '        <label class="form-label fw-semibold">Price per Unit</label>' +
        '        <div class="input-group">' +
        '          <input type="text" class="form-control price-absolute price-absolute-' + id + ' number" name="price_absolute-' + id + '" value="0,0" />' +
        '          <span class="input-group-text">' + (BP.currency || "") + '</span>' +
        '        </div>' +
        '      </div>' +
        '      <div class="col-md-4">' +
        '        <label class="form-label fw-semibold">Discount</label>' +
        '        <div class="input-group">' +
        '          <input type="text" class="form-control price-percentual price-percentual-' + id + ' number" name="price_percentual-' + id + '" value="0,0" />' +
        '          <span class="input-group-text">%</span>' +
        '        </div>' +
        '      </div>' +
        '    </div>' +
        '  </div>' +
        '</div>';
    return card;
}

function calculate_absolute_prices(basePrice) {
    qsa(".price-absolute").forEach(function (item) {
        if (!item.classList.contains("first")) {
            var id = (item.getAttribute("name") || "").split("-")[1];
            var percentEl = qs(".price-percentual-" + id);
            if (!percentEl) return;
            var percent = parseFloat(decimalCommaToDot(percentEl.value)) || 0;
            var price = ((basePrice / 100) * percent).toFixed(2);
            item.value = decimalDotToComma(price);
        }
    });
}

function calculate_percentual_price(input) {
    var absolute = parseFloat(decimalCommaToDot(input.value)) || 0;
    var baseEl = qs(".price-absolute.first");
    if (!baseEl) return;
    var base = parseFloat(decimalCommaToDot(baseEl.value)) || 1;
    var id = (input.getAttribute("name") || "").split("-")[1];
    var price = ((absolute / base) * 100).toFixed(2);
    var target = qs(".price-percentual-" + id);
    if (target) target.value = decimalDotToComma(price);
}

function calculate_absolute_price(input) {
    var percent = parseFloat(decimalCommaToDot(input.value)) || 0;
    var baseEl = qs(".price-absolute.first");
    if (!baseEl) return;
    var base = parseFloat(decimalCommaToDot(baseEl.value)) || 0;
    var id = (input.getAttribute("name") || "").split("-")[1];
    var price = ((base / 100) * percent).toFixed(2);
    var target = qs(".price-absolute-" + id);
    if (target) target.value = decimalDotToComma(price);
}

document.addEventListener("click", function (e) {
    var delBtn = closest(e.target, ".delete-bulk-price-button");
    if (delBtn) {
        e.preventDefault();
        var card = closest(delBtn, ".bulk-price-card");
        if (card) {
            card.remove();
            updateTierNumbers();
            updateAddButtons();
        }
        return;
    }
    var addBtn = closest(e.target, ".add-bulk-price-button");
    if (addBtn) {
        e.preventDefault();
        var html = bulk_price_card();
        var container = qs("#bulk-prices-container");
        if (container) {
            container.insertAdjacentHTML("beforeend", html);
            updateAddButtons();
        }
        return;
    }
});

document.addEventListener("change", function (e) {
    var target = e.target;
    if (target.matches(".price-percentual")) {
        calculate_absolute_price(target);
        return;
    }
    if (target.matches(".price-absolute")) {
        calculate_percentual_price(target);
        return;
    }
});

document.addEventListener("input", function (e) {
    var target = e.target;
    if (target.matches(".price-absolute.first")) {
        var firstPrice = parseFloat(decimalCommaToDot(target.value)) || 0;
        calculate_absolute_prices(firstPrice);
    }
});
