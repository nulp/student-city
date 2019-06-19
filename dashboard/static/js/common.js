$(document).ready(function () {
    $.fn.capitalize = function () {

        //iterate through each of the elements passed in, `$.each()` is faster than `.each()
        $.each(this, function () {

            //split the value of this input by the spaces
            var split = this.value.split(' ');

            //iterate through each of the "words" and capitalize them
            for (var i = 0, len = split.length; i < len; i++) {
                split[i] = split[i].charAt(0).toUpperCase() + split[i].slice(1);
            }

            //re-join the string and set the value of the element
            this.value = split.join(' ');
        });
        return this;
    };

    $('#close-or-back').click(function () {
        var currentUrl = window.location.href;
        window.history.back();
        setTimeout(function () {
            // if location was not changed in 100 ms, then there is no history back
            if (currentUrl === window.location.href) {
                // redirect to site root
                window.close();
            }
        }, 100);
    });

    window.getValuesById = function (select_id, params = {}) {
        $('#' + select_id).each(function () {
            var $select = $(this);

            $select.empty()
                .append('<option selected value="">---------</option>')
            ;

            $.ajax({
                url: $select.attr('data-source'),
                data: params,
            }).then(function (options) {
                options.map(function (option) {
                    var $option = $('<option>');

                    $option
                        .val(option[$select.attr('data-valueKey')])
                        .text(option[$select.attr('data-displayKey')]);

                    $select.append($option);
                });
            });
        });
    }

});


