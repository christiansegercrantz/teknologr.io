$(document).ready(function () {
	// Update the selected functionary type
	add_request_listener({
		selector: "#functionaryTypeForm",
		method: "PUT",
		url: element => `/api/functionaryTypes/${element.data("id")}/`,
	});
	// Remove the selected functionary type
	add_request_listener({
		selector: "#deleteFunctionaryType",
		method: "DELETE",
		url: element => `/api/functionaryTypes/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna funktionärstyp?",
		newLocation: "/admin/functionaries/",
	});

	// Add a person to the list
	add_request_listener({
		selector: "#addfunctionaryform",
		method: "POST",
		url: `/api/multiFunctionary/`,
		confirmationMessage: () => {
			const newMembers = $("#doform_member").data("counter");
			return newMembers && `Du håller på att skapa ${newMembers === 1 ? "1 ny medlem" : `${newMembers} nya medlemmar`}. Fortsätt?`;
		},
	});
	// Remove a person from the list
	add_request_listener({
		selector: ".removeFunctionary",
		method: "DELETE",
		url: element => `/api/functionaries/${element.data("id")}/`,
		confirmMessage: "Vill du radera denna funktionär?",
	});

	add_ajax_multiselect_extension({
		selector_button: "#fform-create-member",
		selector_input: "#fform_member_text",
		selector_hidden_input: "#fform_member",
		selector_deck: "#fform_member_on_deck",
	});
});
