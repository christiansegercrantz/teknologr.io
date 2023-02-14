$(document).ready(function () {
	// Update the selected group type
	add_request_listener({
		selector: "#grouptypeform",
		method: "PUT",
		url: element => `/api/groupTypes/${element.data("id")}/`
	});
	// Remove the selected group type
	add_request_listener({
		selector: "#deleteGroupType",
		method: "DELETE",
		url: element => `/api/groupTypes/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna grupptyp och alla dess undergrupper?",
		newLocation: "/admin/groups/",
	});

	// Add a subgroup to the list
	add_request_listener({
		selector: "#addgroupform",
		method: "POST",
		url: "/api/groups/",
	});
	// Remove a subgroup from the list
	add_request_listener({
		selector: ".removeGroup",
		method: "DELETE",
		url: element => `/api/groups/${element.data("id")}/`,
		confirmMessage: "Vill du ta bort denna undergrupp?",
		newLocation: element => `/admin/groups/${element.data("grouptype_id")}`,
	});

	// Edit the selected subgroup
	add_request_listener({
		selector: "#editgroupform",
		method: "PUT",
		url: element => `/api/groups/${element.data("id")}/`,
	});
	// Add members to the selected subgroup
	add_request_listener({
		selector: "#addgroupmemberform",
		method: "POST",
		url: "/api/multiGroupMembership/",
		confirmMessage: confirmMessageCreateMembers,
	});
	// Remove a member from the selected subgroup
	add_request_listener({
		selector: ".removeMembership",
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
		selector_hidden_input: "#gmform_member",
		selector_deck: "#gmform_member_on_deck",
	});
});
