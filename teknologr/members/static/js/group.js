$(document).ready(function () {
	// Update the selected group type
	add_request_listener({
		element: "#grouptypeform",
		method: "PUT",
		url: element => `/api/groupTypes/${element.data("id")}/`
	});
	// Remove the selected group type
	add_request_listener({
		element: "#deleteGroupType",
		method: "DELETE",
		url: element => `/api/groupTypes/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna grupptyp och alla dess undergrupper?",
		newLocation: "/admin/groups/",
	});

	// Add a subgroup to the list
	add_request_listener({
		element: "#addgroupform",
		method: "POST",
		url: "/api/groups/",
	});
	// Remove a subgroup from the list
	add_request_listener({
		element: ".removeGroup",
		method: "DELETE",
		url: element => `/api/groups/${element.data("id")}/`,
		confirmMessage: "Vill du ta bort denna undergrupp?",
		newLocation: element => `/admin/groups/${element.data("grouptype_id")}`,
	});

	// Edit the selected subgroup
	add_request_listener({
		element: "#editgroupform",
		method: "PUT",
		url: element => `/api/groups/${element.data("id")}/`,
	});
	// Add members to the selected subgroup
	add_request_listener({
		element: "#addgroupmemberform",
		method: "POST",
		url: "/api/multiGroupMembership/",
	});
	// Remove a member from the selected subgroup
	add_request_listener({
		element: ".removeMembership",
		method: "DELETE",
		url: element => `/api/groupMembership/${element.data("id")}/`,
		confirmMessage: "Vill du ta bort detta undergruppsmedlemskap?",
	});

	// Copy the hidden list of emails to the clipboard
	$('#copy2clipboard').click(function(){
		$("#members_email_list").select();
		document.execCommand('copy');
	});
});
