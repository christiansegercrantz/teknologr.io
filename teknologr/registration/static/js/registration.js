$('#id_degree_programme_options').change(function() {
    if (this.value === 'extra') {
        $('#unknown_degree').show();
    } else {
        $('#unknown_degree').hide();
        $('#unknown_degree').val(self.value);
    }
})
