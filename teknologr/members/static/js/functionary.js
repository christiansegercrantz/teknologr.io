$(document).ready(function () {
	// Update the selected functionary type
	add_request_listener({
		element: "#functionaryTypeForm",
		method: "PUT",
		url: element => `/api/functionaryTypes/${element.data("id")}/`,
	});
	// Remove the selected functionary type
	add_request_listener({
		element: "#deleteFunctionaryType",
		method: "DELETE",
		url: element => `/api/functionaryTypes/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna funktionärstyp?",
		newLocation: "/admin/functionaries/",
	});

	// Add a person to the list
	add_request_listener({
		element: "#addfunctionaryform",
		method: "POST",
		url: `/api/functionaries/`,
	});
	// Remove a person from the list
	add_request_listener({
		element: ".removeFunctionary",
		method: "DELETE",
		url: element => `/api/functionaries/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna funktionär?",
	});
});