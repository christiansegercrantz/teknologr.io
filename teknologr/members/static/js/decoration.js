$(document).ready(function () {
	// Update the decoration type
	add_request_listener({
		element: "#decorationform",
		method: "PUT",
		url: element => `/api/decorations/${element.data("id")}/`,
	});
	// Delete the decoration type
	add_request_listener({
		element: "#deleteDecoration",
		method: "DELETE",
		url: element => `/api/decorations/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna hedersbetygelse?",
		newLocation: "/admin/decorations/",
	});

	// Add a person to the list
	add_request_listener({
		element: "#adddecorationform",
		method: "POST",
		url: "/api/multiDecorationOwnership/",
	});
	// Delete a person from the list
	add_request_listener({
		element: ".removeDecoration",
		method: "DELETE",
		url: element => `/api/decorationOwnership/${element.data("id")}/`,
		confirmMessage: "Vill du radera detta hedersbetygelseinnehav?",
	});
});