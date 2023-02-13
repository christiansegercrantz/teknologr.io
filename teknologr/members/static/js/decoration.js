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
	});
	// Delete a person from the list
	add_request_listener({
		selector: ".removeDecoration",
		method: "DELETE",
		url: element => `/api/decorationOwnership/${element.data("id")}/`,
		confirmMessage: "Vill du radera detta hedersbetygelseinnehav?",
	});
});