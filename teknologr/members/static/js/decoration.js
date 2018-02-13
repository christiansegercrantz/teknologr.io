$(document).ready(function() {
	
	$("#decorationform").submit(function(event){
		var id = $(this).data('id');	
		var request = $.ajax({
			url: "/api/decorations/" + id + "/",
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


	$("#deleteDecoration").click(function(){
		if(confirm("Vill du radera denna betygelse?")) {
			var id = $(this).data('id');
			var request = $.ajax({
				url: "/api/decorations/" + id + "/",
				method: "DELETE",
			});
 
			request.done(function() { 
				window.location = "/admin/decorations/";
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});
		}
	});

	$("#adddecorationform").submit(function(event){
		var request = $.ajax({
			url: "/api/decorationOwnership/",
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

	$(".removeDecoration").click(function(){
		if(confirm("Vill du radera detta betygelseinnehav?")) {
			var id = $(this).data('id');
			var decorationid = $(this).data("decoration_id");
			var request = $.ajax({
				url: "/api/decorationOwnership/" + id + "/",
				method: "DELETE",
			});

			request.done(function() { 
				window.location = "/admin/decorations/" + decorationid + "/"; 
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});
		}
	});
});