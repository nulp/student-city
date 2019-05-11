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
});