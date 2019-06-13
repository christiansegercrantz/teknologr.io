$(document).ready(function() {

    $('#id_degree_programme_options').change(function() {
        console.log('hello');
        if (this.value === 'extra') {
            $('#unknown_degree').show();
            $('#unknown_degree input').val('');
        } else {
            $('#unknown_degree').hide();
            $('#unknown_degree input').val(this.value);
        }
    });

});
