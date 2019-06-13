function setProgrammeChoice() {
    const programmeOptionsSelector = $('#id_degree_programme_options option');
    const programmeOptions = Object.values(programmeOptionsSelector).map(option => option.value);

    const currentProgramme = $('#id_degree_programme').val();
    if (programmeOptions.indexOf(currentProgramme) !== -1) {
        $('#id_degree_programme_options').val(currentProgramme);
    } else {
        $('#id_degree_programme_options').val('extra');
        $('#unknown_degree').show();
    }
}

$(document).ready(function() {

    // Set degree choice based on pre-existing data
    setProgrammeChoice();

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
