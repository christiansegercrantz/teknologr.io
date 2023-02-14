$(document).ready(function() {

	$("#addgroupmemberform").submit(function(event){
		const newMembers = $("#doform_member").data("counter");
		if (newMembers && !confirm(`Du håller på att skapa ${newMembers === 1 ? "1 ny medlem" : `${newMembers} nya medlemmar`}. Fortsätt?`)) return;

		var data = $(this).serialize();
		var request = $.ajax({
			url: "/api/multiGroupMembership/",
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

	$(".removeMembership").click(function(){
		if(confirm("Vill du ta bort detta gruppmedlemskap?")) {		
			var id = $(this).data('id');	

			var request = $.ajax({
				url: "/api/groupMembership/" + id + "/",
				method: "DELETE"
			})

			request.done(function() {
				location.reload();
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});
		}
	});
	$('#copy2clipboard').click(function(){
		$("#members_email_list").select();
    document.execCommand('copy');
	});

	add_ajax_multiselect_extension({
		selector_button: "#gmform-create-member",
		selector_input: "#gmform_member_text",
		selector_hidden_input: "#gmform_member",
		selector_deck: "#gmform_member_on_deck",
	});
});
