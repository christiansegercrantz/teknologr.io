$(document).ready(function () {
	// Update the decoration type
	add_request_listener({
		selector: "#decorationform",
		method: "PUT",
		url: element => `/api/decorations/${element.data("id")}/`,
	});
	// Delete the decoration type
	add_request_listener({
		selector: "#deleteDecoration",
		method: "DELETE",
		url: element => `/api/decorations/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna hedersbetygelse?",
		newLocation: "/admin/decorations/",
	});

	// Add a person to the list
	add_request_listener({
		selector: "#adddecorationform",
		method: "POST",
		url: "/api/multiDecorationOwnership/",
		confirmMessage: confirmMessageCreateMembers,
	});

	// Delete a person from the list
	add_request_listener({
		selector: ".removeDecoration",
		method: "DELETE",
		url: element => `/api/decorationOwnership/${element.data("id")}/`,
		confirmMessage: "Vill du radera detta hedersbetygelseinnehav?",
	});

	add_ajax_multiselect_extension({
		selector_button: "#doform-create-member",
		selector_input: "#doform_member_text",
		selector_hidden_input: "#doform_member",
		selector_deck: "#doform_member_on_deck",
	});
});
