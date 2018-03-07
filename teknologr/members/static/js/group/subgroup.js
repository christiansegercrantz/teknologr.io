$(document).ready(function() {

	$("#addgroupform").submit(function(event){

		var data = $(this).serialize();
	
		var request = $.ajax({
			url: "/api/groups/",
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

	$(".removeGroup").click(function(){
		if(confirm("Vill du ta bort denna grupp?")) {		
			var id = $(this).data('id');
			var grouptype_id = $(this).data('grouptype_id');

			var request = $.ajax({
				url: "/api/groups/" + id + "/",
				method: "DELETE"
			})

			request.done(function() {
				window.location = "/admin/groups/" + grouptype_id + "/"; 
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});
		}
	});

	$("#editgroupform").submit(function(event){
		var id = $(this).data('id');
		var data = $(this).serialize();
		var request = $.ajax({
			url: "/api/groups/" + id + "/",
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
});
