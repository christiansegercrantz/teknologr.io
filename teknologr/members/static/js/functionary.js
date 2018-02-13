$(document).ready(function() {
	
	$("#functionaryTypeForm").submit(function(event){
		var id = $(this).data('id');	
		var request = $.ajax({
			url: "/api/functionaryTypes/" + id + "/",
			method: 'PUT',
			data: $(this).serialize()
		});

		request.done(function() {
			location.reload();
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});

		event.preventDefault();
	});


	$("#deleteFunctionaryType").click(function(){
		if(confirm("Vill du radera denna funktionärstyp?")) {
			var id = $(this).data('id');
			var request = $.ajax({
				url: "/api/functionaryTypes/" + id + "/",
				method: "DELETE",
			});
 
			request.done(function() { 
				window.location = "/admin/functionaries/"; 
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});
		}
	});

	$("#addfunctionaryform").submit(function(event){
		var request = $.ajax({
			url: "/api/functionaries/",
			method: 'POST',
			data: $(this).serialize()
		});

		request.done(function() {
			location.reload();
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});

		event.preventDefault();
	});

	$(".removeFunctionary").click(function(){
		if(confirm("Vill du radera denna funktionär?")) {
			var id = $(this).data('id');
			var functionaryTypeID = $(this).data("functionarytype_id");
			var request = $.ajax({
				url: "/api/functionaries/" + id + "/",
				method: "DELETE",
			});

			request.done(function() { 
				window.location = "/admin/functionaries/" + functionaryTypeID + "/"; 
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});
		}
	});
});