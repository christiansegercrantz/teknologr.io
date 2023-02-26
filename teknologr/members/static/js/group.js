$(document).ready(function () {
	// Update the selected group type
	add_request_listener({
		selector: "#edit-gt-form",
		method: "PUT",
		url: element => `/api/groupTypes/${element.data("id")}/`
	});
	// Remove the selected group type
	add_request_listener({
		selector: "#delete-gt-button",
		method: "DELETE",
		url: element => `/api/groupTypes/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna grupptyp och alla dess undergrupper?",
		newLocation: "/admin/groups/",
	});

	// Add a group to the list
	add_request_listener({
		selector: "#add-g-form",
		method: "POST",
		url: "/api/groups/",
	});
	// Remove a group from the list
	add_request_listener({
		selector: ".delete-g-button",
		method: "DELETE",
		url: element => `/api/groups/${element.data("id")}/`,
		confirmMessage: "Vill du ta bort denna undergrupp?",
		newLocation: element => `/admin/groups/${element.data("grouptype_id")}`,
	});

	// Edit the selected group
	add_request_listener({
		selector: "#edit-g-form",
		method: "PUT",
		url: element => `/api/groups/${element.data("id")}/`,
	});
	// Add members to the selected group
	add_request_listener({
		selector: "#add-gm-form",
		method: "POST",
		url: "/api/multiGroupMembership/",
		confirmMessage: confirmMessageCreateMembers,
	});
	// Remove a member from the selected group
	add_request_listener({
		selector: ".delete-gm-button",
		method: "DELETE",
		url: element => `/api/groupMembership/${element.data("id")}/`,
		confirmMessage: "Vill du ta bort detta undergruppsmedlemskap?",
	});

	// Copy the hidden list of emails to the clipboard
	$('#copy2clipboard').click(function(){
		$("#members_email_list").select();
		document.execCommand('copy');
	});

	add_ajax_multiselect_extension({
		selector_button: "#gmform-create-member",
		selector_input: "#gmform_member_text",
	});
});
