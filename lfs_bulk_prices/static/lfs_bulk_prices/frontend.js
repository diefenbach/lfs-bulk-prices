document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('keyup', function(event) {
        if (event.target.matches('.product input[name=quantity]')) {
            var url = event.target.getAttribute('bulk_prices_update_url');
            var amount = event.target.value;
            
            fetch(url + '?amount=' + encodeURIComponent(amount))
                .then(response => response.json())
                .then(data => {
                    document.querySelectorAll('.standard-price-value').forEach(element => {
                        element.innerHTML = data['standard_price'];
                    });
                    document.querySelectorAll('.base-price .money').forEach(element => {
                        element.innerHTML = data['base_price'];
                    });
                });
        }
    });
});
