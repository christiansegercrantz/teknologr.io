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
        if (this.value === 'extra') {
            $('#unknown_degree').show();
            $('#id_degree_programme').val('');
        } else {
            $('#unknown_degree').hide();
            $('#id_degree_programme').val(this.value);
        }
    });

    $('#deleteapplicant').click(function() {
        if (confirm('Vill du radera denna ansökan?')) {
            const id = $(this).data('id');
			const request = $.ajax({
                url: '/api/applicants/' + id + '/',
                method: 'DELETE',
                data: {'applicant_id': id},
            });

            request.done(function() {
                window.location = '/admin/applicants/';
            });

            request.fail(function(jqHXR, textStatus) {
                alert('Request failed: ' + textStatus + ': ' + jqHXR.responseText);
            });
        }
    });

    $('#makemember').click(function() {
        if (confirm('Vill du lägga till denna ansökan i medlemsregistret?')) {
            const id = $(this).data('id');
            const request = $.ajax({
                url: '/api/applicants/makeMember/' + id + '/',
                method: 'POST',
            });

            request.done(function() {
                window.location = '/admin/applicants/';
            });

            request.fail(function(jqHXR, textStatus) {
                alert('Request failed: ' + textStatus + ': ' + jqHXR.responseText);
            });
        }
    });
});
