// Sidebar ajax search delay timer
var timer;

/**
 * Helper method for calling a function, if it is a function.
 */
const call_if_function = (fn, ...params) => {
	return typeof fn === "function" ? fn(...params) : fn;
}

/**
 * Helper function for adding a listener to an element that does a request.
 *
 * @param {Object} options
 * @param {String} option.element          The element(s) to add the listener to
 * @param {String} option.method           The request method
 * @param {String} option.url              The request url
 * @param {Object} [option.data]           The request data (default: Element.serialize())
 * @param {String} [option.confirmMessage] An optional confirm message
 * @param {String} [option.newLocation]    The url to redirect to after the request is done (default: reload current page)
 *
 * Some of the options also allow a function (e: Element) => T to be passed, if the option value depends on for example data on the specific element. These options are:
 * @param {String | (e: Element) => String} option.url
 * @param {Object | (e: Element) => Object} dption.data
 * @param {String | (e: Element) => String} option.confirmMessage
 * @param {String | (e: Element) => String} option.newLocation
 */
const add_request_listener = ({ selector, method, url, data, confirmMessage, newLocation }) => {
	// Get the element(s) to attach the listener to
	$(selector).each((_, domElement) => {
		// Deduce what to listen for based on the element tag
		const type = domElement.tagName.toLowerCase() === "form" ? "submit" : "click";

		const e = $(domElement);
		// Add a listener to the element
		e.on(type, event => {
			event.preventDefault();

			const msg = call_if_function(confirmMessage, e);
			if (msg && !confirm(msg)) return;

			// Do the request
			const request = $.ajax({
				method,
				url: call_if_function(url, e),
				data: data ? call_if_function(data, e) : e.serialize(),
			});

			// Add listeners to the request
			request.done(msg => {
				if (newLocation) window.location = call_if_function(newLocation, e, msg);
				else location.reload();
			});
			// XXX: The error message is not very helpful for the user, so should probably change this to something else
			request.fail((jqHXR, textStatus) => {
				alert(`Request failed (${textStatus}): ${jqHXR.responseText}`);
			});
		});
	});
}

/**
 * Extend the functionality of the AutoCompleteSelectMultipleField from django-ajax-selects by also allowing new members to be created simultaneously. This is how it's done:
 * 1. Add click-listener to a button
 * 2. When clicked, the name is taken from the member search box
 * 3. The name is appended to the hidden input and appended to the list
 * 4. A button for removing the name is also created
 * 5. When the form is submitted, the api endpoint handles splitting the hidden input and creating new members
 *
 * Additional listeners are created to enable/disable the create and submit buttons.
 *
 * Note that a certain layout of the elements is assumed.
 */
const add_ajax_multiselect_extension = ({ selector_button, selector_input, selector_submit }) => {
	const create_member_button = $(selector_button);
	const submit_button = $(selector_submit);
	const input = $(selector_input);

	// Return if not all needed elements are found
	if (!create_member_button.length || !submit_button.length || !input.length) return;

	// Assume the hidden input and the deck comes directly after the normal input element
	const hidden_input = input.next();
	const deck = hidden_input.next();

	// Listen on input to enable/disable create button
	input.on("input", e => {
		const value = e.target.value;
		create_member_button.prop("disabled", !value || !value.trim().includes(" "));
	});

	// Listen for changes in the list of members to enable/disable submit button
	const observer = new MutationObserver(() => {
		input.trigger("input");
		submit_button.prop("disabled", deck.children().length == 0);
	});
	observer.observe(deck.get(0), { childList: true });

	// Handle creating new members
	create_member_button.click(e => {
		e.preventDefault();

		const name = input.val().trim();
		if (!name || !name.includes(" ") || name.includes("|") || name.includes("$")) return;
		input.val("");

		// Add name to hidden (real) input
		const substring = `$${name}|`;
		hidden_input.val(hidden_input.val() + substring);

		// Keep track of the amount of names added by storing the counter on the form
		const data = input.closest("form").data();
		data.counter = (data.counter || 0) + 1;

		// Add name to list
		const div = $("<div>", {
			html: `<b>Ny:</b> ${name}`,
		}).appendTo(deck);

		// Create button for removing the name from the list
		$("<span>", {
			class: "ui-icon ui-icon-trash",
			text: "X",
			click: () => {
				const value = hidden_input.val();
				const i = value.indexOf(substring);
				hidden_input.val(value.slice(0, i) + value.slice(i + substring.length));
				data.counter--;
				div.remove();
			},
		}).prependTo(div);
	});
}

const confirmMessageCreateMembers = e => {
	const newMembers = e.data("counter");
	return newMembers && `Du håller på att skapa ${newMembers === 1 ? "1 ny medlem" : `${newMembers} nya medlemmar`}. Fortsätt?`;
}

$(document).ready(function () {
	const element_to_api_path = element => {
		switch(element.data("active")) {
			case "members": return "members";
			case "groups": return "groupTypes";
			case "functionaries": return "functionaryTypes";
			case "decorations": return "decorations";
		}
	}

	add_request_listener({
		selector: "#new-mgtftd-form",
		method: "POST",
		url: element => `/api/${element_to_api_path(element)}/`,
		newLocation: (element, msg) => `/admin/${element.data("active")}/${msg.id}/`,
	});

	$('#side-search').keyup(function(event) {
		var active = $(this).data('active');
		var filter = $(this).val().toLowerCase();

		if (active === 'members') {
			timer && clearTimeout(timer);
			timer = setTimeout(function(){
				$.ajax({
					// XXX: Why ')'???
					url: "/ajax_select/ajax_lookup/member)?term=" + filter,
					method: "GET",
				}).done(function(data) {
					$("#side-objects").empty();
					$.each(data, function(i, item) {
						var a = '<a class="list-group-item" href="/admin/members/'+ item.pk +'/">'+ item.value +'</a>'
						$("#side-objects").append(a);
					});
				});
			}, 300);

		} else {
			$("#side-objects a").each(function(index){
				if($(this).text().toLowerCase().indexOf(filter) > -1) {
					$(this).css('display', '');
				} else {
					$(this).css('display', 'none');
				}
			});
		}
	});

	/**
	 * Populate "create new xyz" modal form with the current search box value.
	 */
	$("#side-new").click(() => {
		const search = $("#side-search");
		const value = search.val();
		switch (search.data("active")) {
			case "members": {
				const names = value.split(" ").filter(s => s).map(s => s[0].toUpperCase() + s.slice(1));
				if (names.length === 1) {
					return $("#mmodal_given_names").val(names.join(" "));
				}
				const last = names.splice(names.length - 1, 1);
				$("#mmodal_given_names").val(names.join(" "));
				$("#mmodal_surname").val(last);
			} break;
			case "decorations": $("#dmodal_name").val(value); break;
			case "groups": $("#gtmodal_name").val(value); break;
			case "functionaries": $("#ftmodal_name").val(value); break;
		}
	});

});
