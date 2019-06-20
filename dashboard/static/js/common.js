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


    window.PopupCenter = function (url, title, w, h) {
        // Fixes dual-screen position                         Most browsers      Firefox
        var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : window.screenX;
        var dualScreenTop = window.screenTop != undefined ? window.screenTop : window.screenY;

        var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
        var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

        var systemZoom = width / window.screen.availWidth;
        var left = (width - w) / 2 / systemZoom + dualScreenLeft
        var top = (height - h) / 2 / systemZoom + dualScreenTop
        var newWindow = window.open(url, title, 'scrollbars=yes, width=' + w / systemZoom + ', height=' + h / systemZoom + ', top=' + top + ', left=' + left);

        // Puts focus on the newWindow
        if (window.focus) newWindow.focus();
        return newWindow;
    };


    window.listenNcapitalize = function (field) {
        $(field).on('keyup', function () {
            $(this).capitalize();
        }).capitalize();
    };

    window.listenFormSubmit = function (formId) {

        var answerFields = ['id_old_address', 'id_registered_period'];

        $(formId).submit(function (event) {
            var form = this;
            event.preventDefault();
            var msg_text = "Незаповнені поля:\n";
            var cnt = 0;
            $('input').each(function () {
                if (answerFields.includes(this.id) && $(this).val() === '') {
                    cnt += 1;
                    var empty_field = $('label[for="' + this.id + '"]').html().replace(':', '');
                    msg_text += ' - ' + empty_field + '\n';
                }
            });

            if (cnt && confirm(msg_text)) {
                form.submit();
            }

        });
    };

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


