var changed = false;

$(document).ready(function() {

	// Buttons for adding items to the selected member
	// XXX: Could probably be combined
	add_request_listener({
		selector: "#add-do-form",
		method: "POST",
		url: "/api/decorationOwnership/",
	});
	add_request_listener({
		selector: "#add-f-form",
		method: "POST",
		url: "/api/functionaries/",
	});
	add_request_listener({
		selector: "#add-gm-form",
		method: "POST",
		url: "/api/groupMembership/",
	});
	add_request_listener({
		selector: "#add-mt-form",
		method: "POST",
		url: "/api/memberTypes/",
	});

	// Buttons for deleting individual items from the selected member
	// XXX: Could probably be combined
	add_request_listener({
		selector: ".delete-do-button",
		method: "DELETE",
		url: element => `/api/decorationOwnership/${element.data("id")}/`,
		confirmMessage: "Vill du radera detta betygelseinnehav?",
	});
	add_request_listener({
		selector: ".delete-f-button",
		url: element => `/api/functionaries/${element.data("id")}/`,
		method: "DELETE",
		confirmMessage: "Vill du radera detta postinnehav?",
	});
	add_request_listener({
		selector: ".delete-gm-button",
		method: "DELETE",
		url: element => `/api/groupMembership/${element.data("id")}/`,
		confirmMessage: "Vill du radera detta gruppmedlemskap?",
	});
	add_request_listener({
		selector: ".delete-mt-button",
		method: "DELETE",
		url: element => `/api/memberTypes/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna medlemstyp?",
	});

	// Delete the selected member
	add_request_listener({
		selector: "#delete-m-button",
		method: "DELETE",
		url: element => `/api/members/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna medlem?",
		newLocation: "/admin/members/",
	});

	$('.edit-mt-button').click(function(){
		const id = $(this).data("id");
		$("#edit-mt-modal .modal-body").load("/admin/membertype/" + id + "/form/", function () {
			add_request_listener({
				selector: "#edit-mt-form",
				method: "PUT",
				url: `/api/memberTypes/${id}/`,
			});

			$('#edit-mt-modal').modal();
		});
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