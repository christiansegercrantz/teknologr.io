var changed = false;

$(document).ready(function() {

	$("#addmembertypeform").submit(function(event){
		var data = $(this).serialize();
		var request = $.ajax({
			url: "/api/memberTypes/",
			method: "POST",
			data: data
		});

		request.done(function() {
			location.reload();
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});

		event.preventDefault();
	});

	$("#deletemember").click(function(){
		if(confirm("Vill du radera denna medlem?")) {
			var id = $(this).data('id');
			var request = $.ajax({
				url: "/api/members/" + id + "/",
				method: "DELETE",
			});
 
			request.done(function() { 
				window.location = "/admin/members/"; 
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});
		}
	});

	$('[data-toggle="tooltip"]').tooltip({
		placement : 'top'
	});

	$('.removeMemberType').click(function(){
		if(confirm("Vill du radera denna medlemstyp?")) {
			var id = $(this).data('id');
			var request = $.ajax({
				url: "/api/memberTypes/" + id + "/",
				method: "DELETE",
			});

			request.done(function() {
				location.reload();
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});	
		}
	});

	$('.editMemberType').click(function(){
		var id = $(this).data('id');
		$("#editMemberTypeModal .modal-body").load("/admin/membertype/" + id + "/form/", function() {
			$("#editmembertypeform").submit(function(event){
				var data = $(this).serialize();
				var request = $.ajax({
					url: "/api/memberTypes/" + id + "/",
					method: "PUT",
					data: data
				});

				request.done(function() {
					location.reload();
				});

				request.fail(function( jqHXR, textStatus ){
					alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
				});
				event.preventDefault();
			});
			$('#editMemberTypeModal').modal();
		});
	});

	$('#adddecorationform').submit(function(event){
		var data = $(this).serialize();
		var request = $.ajax({
			url: "/api/decorationOwnership/",
			method: "POST",
			data: data
		});

		request.done(function() {
			location.reload();
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});

		event.preventDefault();
	});

	$('#addfunctionaryform').submit(function(event){
		var data = $(this).serialize();
		var request = $.ajax({
			url: "/api/functionaries/",
			method: "POST",
			data: data
		});

		request.done(function() {
			location.reload();
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});

		event.preventDefault();
	});

	$('#addgroupform').submit(function(event){
		var data = $(this).serialize();
		var request = $.ajax({
			url: "/api/groupMembership/",
			method: "POST",
			data: data
		});

		request.done(function() {
			location.reload();
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed (" + textStatus + ") " + jqHXR.responseText );
		});

		event.preventDefault();
	});

	$('.removeFunctionary').click(function(){
		if(confirm("Vill du radera denna post?")) {
			var id = $(this).data('id');
			var request = $.ajax({
				url: "/api/functionaries/" + id + "/",
				method: "DELETE",
			});

			request.done(function() {
				location.reload();
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});	
		}
	});

	$('.removeGroup').click(function(){
		if(confirm("Vill du radera detta gruppmedlemskap?")) {
			var id = $(this).data('id');
			var request = $.ajax({
				url: "/api/groupMembership/" + id + "/",
				method: "DELETE",
			});

			request.done(function() {
				location.reload();
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});	
		}
	});

	$('#memberform').change(function(){
		changed = true;
	});

	$('#memberform').submit(function(){
		changed = false;
	});
});


$(window).on('beforeunload', function(){
	if(changed) {
		return "Changes not saved";
	}
});