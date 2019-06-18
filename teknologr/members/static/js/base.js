// Sidebar ajax search delay timer
var timer;

$(document).ready(function() {
	$("#newform").submit(function(event){
		var active = $(this).data('active');
		switch(active) {
			case 'members':
				var apipath = 'members'
				break;
			case 'groups':
				var apipath = 'groupTypes'
				break;
			case 'functionaries':
				var apipath = 'functionaryTypes'
				break;
			case 'decorations':
				var apipath = 'decorations'
				break;
		}


		var request = $.ajax({
			url: "/api/" + apipath + "/",
			method: 'POST',
			data: $(this).serialize()
		});

		request.done(function(msg) {
			window.location = "/admin/"+ active +"/" + msg.id + "/";
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});

		event.preventDefault();
	});

	$('#side-search').keyup(function(event) {
		var active = $(this).data('active');
		var filter = $(this).val().toLowerCase();

		if (active === 'members') {
			timer && clearTimeout(timer);
			timer = setTimeout(function(){
				$.ajax({
					url: "/admin/ajax_select/ajax_lookup/member?term=" + filter,
					method: "GET",
				}).done(function(data) {
					$("#side-objects").empty();
					$.each(data, function(i, item) {
						var a = '<a class="list-group-item" href="/admin/members/'+ item.pk +'/">'+ item.value +'</a>'
						$("#side-objects").append(a);
					});
				});
			}, 300);

		} else {
			$("#side-objects a").each(function(index){
				if($(this).text().toLowerCase().indexOf(filter) > -1) {
					$(this).css('display', '');
				} else {
					$(this).css('display', 'none');
				}
			});
		}
	});

    $('#choose-multiple-applicants').submit(function(event) {
        const data = $(this).serialize();
        const request = $.ajax({
            url: '/api/multiApplicantSubmission/',
            method: 'POST',
            data: data,
        });

        request.done(function() {
            window.location = '/admin/applicants/';
        });

        request.fail(function(jqHXR, textStatus) {
            alert('Request failed: ' + textStatus + ': ' + jqHXR.responseText);
        });

        event.preventDefault();
    });

});
