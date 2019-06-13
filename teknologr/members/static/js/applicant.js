$(document).ready(function() {

    $('#id_degree_programme_options').change(function() {
        console.log('hello');
        if (this.value === 'extra') {
            $('#unknown_degree').show();
            $('#id_degree_programme').val('');
        } else {
            $('#unknown_degree').hide();
            $('#id_degree_programme').val(this.value);
        }
    });

});
