/* Some browsers (e.g. desktop Safari) does not have built-in datepickers (e.g. Firefox).
 * Thus we check first if the browser supports this, in case not we inject jQuery UI into the DOM.
 * This enables a jQuery datepicker.
 */

var datefield = document.createElement('input');
datefield.setAttribute('type', 'date');

if (datefield.type != 'date') {
    const jQueryUIurl = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1';
    document.write(`<link href="${jQueryUIurl}/themes/base/jquery-ui.css" rel="stylesheet" type="text/css" />\n`)
    document.write(`<script src="${jQueryUIurl}/jquery-ui.min.js"><\/script>\n`)
}

$(document).ready(function() {
    // There is no default option for setting readonly a field with django-bootstrap4
    $('#id_mother_tongue').prop('readonly', true);

    // Set tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Set the datepicker on birth date, in case input type of date is not supported
    if (datefield.type != 'date') {
        const currentYear = new Date().getFullYear();

        $('#id_birth_date').datepicker({
            changeMonth: true,
            changeYear: true,
            yearRange: `1930:${currentYear}`,
        });
    }
});

$('#id_degree_programme_options').change(function() {
    if (this.value === 'extra') {
        $('#unknown_degree').show();
        $('#unknown_degree input').val('');
    } else {
        $('#unknown_degree').hide();
        $('#unknown_degree input').val(this.value);
    }
});

$('input:radio[name="language"]').change(function() {
    if ($(this).is(':checked')) {
        if ($(this).val() == 'extra') {
            $('#id_mother_tongue').prop('readonly', false);
            $('#id_mother_tongue').val('');
        } else {
            $('#id_mother_tongue').prop('readonly', true);
            $('#id_mother_tongue').val(this.value);
        }
    }
});
