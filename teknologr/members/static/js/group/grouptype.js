$(document).ready(function() {
	
	$("#grouptypeform").submit(function(event){
		var id = $(this).data('id');	
		var request = $.ajax({
			url: "/api/groupTypes/" + id + "/",
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


	$("#deleteGroupType").click(function(){
		if(confirm("Vill du radera denna grupptyp och alla dess undergrupper?")) {
			var id = $(this).data('id');
			var request = $.ajax({
				url: "/api/groupTypes/" + id + "/",
				method: "DELETE",
			});
 
			request.done(function() { 
				window.location = "/admin/groups/"; 
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});
		}
	});
});