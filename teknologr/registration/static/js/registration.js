$(document).ready(function() {
    // There is no default option for disabling a field with django-bootstrap4
    $('#id_mother_tongue').prop('disabled', true);

    // Set tooltips
    $('[data-toggle="tooltip"]').tooltip();
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
            $('#id_mother_tongue').prop('disabled', false);
            $('#id_mother_tongue').val('');
        } else {
            $('#id_mother_tongue').prop('disabled', true);
            $('#id_mother_tongue').val(this.value);
        }
    }
});
