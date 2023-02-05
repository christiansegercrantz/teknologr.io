var changed = false;

$(document).ready(function() {

	// Buttons for adding items to the selected member
	// XXX: Could probably be combined
	add_request_listener({
		element: "#adddecorationform",
		method: "POST",
		url: "/api/decorationOwnership/",
	});
	add_request_listener({
		element: "#addfunctionaryform",
		method: "POST",
		url: "/api/functionaries/",
	});
	add_request_listener({
		element: "#addgroupform",
		method: "POST",
		url: "/api/groupMembership/",
	});
	add_request_listener({
		element: "#addmembertypeform",
		method: "POST",
		url: "/api/memberTypes/",
	});

	// Buttons for deleting individual items from the selected member
	// XXX: Could probably be combined
	add_request_listener({
		element: ".removeDecoration",
		method: "DELETE",
		url: element => `/api/decorationOwnership/${element.data("id")}/`,
		confirmMessage: "Vill du radera detta hedersbetygelseinnehav?",
	});
	add_request_listener({
		element: ".removeFunctionary",
		url: element => `/api/functionaries/${element.data("id")}/`,
		method: "DELETE",
		confirmMessage: "Vill du radera denna post?",
	});
	add_request_listener({
		element: ".removeGroup",
		method: "DELETE",
		url: element => `/api/groupMembership/${element.data("id")}/`,
		confirmMessage: "Vill du radera detta gruppmedlemskap?",
	});
	add_request_listener({
		element: ".removeMemberType",
		method: "DELETE",
		url: element => `/api/memberTypes/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna medlemstyp?",
	});

	// Delete the selected member
	add_request_listener({
		element: "#deletemember",
		method: "DELETE",
		url: element => `/api/members/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna medlem?",
		newLocation: "/admin/members/",
	});

	$('.editMemberType').click(function(){
		const id = $(this).data("id");
		$("#editMemberTypeModal .modal-body").load("/admin/membertype/" + id + "/form/", function () {
			add_request_listener({
				element: "#editmembertypeform",
				method: "PUT",
				url: `/api/memberTypes/${id}/`,
			});

			$('#editMemberTypeModal').modal();
		});
	});

	$('[data-toggle="tooltip"]').tooltip({
		placement : 'top'
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