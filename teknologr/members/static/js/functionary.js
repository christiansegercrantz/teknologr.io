$(document).ready(function () {
	// Update the selected functionary type
	add_request_listener({
		selector: "#edit-ft-form",
		method: "PUT",
		url: element => `/api/functionaryTypes/${element.data("id")}/`,
	});
	// Remove the selected functionary type
	add_request_listener({
		selector: "#delete-ft-button",
		method: "DELETE",
		url: element => `/api/functionaryTypes/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna funktionärstyp?",
		newLocation: "/admin/functionaries/",
	});

	// Add a person to the list
	add_request_listener({
		selector: "#add-f-form",
		method: "POST",
		url: `/api/multiFunctionary/`,
		confirmMessage: confirmMessageCreateMembers,
	});
	// Remove a person from the list
	add_request_listener({
		selector: ".delete-f-button",
		method: "DELETE",
		url: element => `/api/functionaries/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna funktionär?",
	});

	add_ajax_multiselect_extension({
		selector_button: "#fform-create-member",
		selector_input: "#fform_member_text",
	});
});
