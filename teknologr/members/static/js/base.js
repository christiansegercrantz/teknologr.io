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
 * @param {String | (e: Element) => String} option.newLocation
 */
const add_request_listener = options => {
	const { element, method, url, data, confirmMessage, newLocation } = options;
	const ELEMENT = $(element);

	let TYPE = ELEMENT.get(0)?.tagName.toLowerCase() === "form" ? "submit" : "click";

	// Add a listener to the element(s)
	ELEMENT.on(TYPE, event => {
		event.preventDefault();

		if (confirmMessage && !confirm(confirmMessage)) return;

		// Do the request
		const request = $.ajax({
			method,
			url: call_if_function(url, ELEMENT),
			data: data ? call_if_function(data, ELEMENT) : ELEMENT.serialize(),
		});

		// Add listeners to the request
		request.done(msg => {
			if (newLocation) window.location = call_if_function(newLocation, ELEMENT, msg);
			else location.reload();
		});
		request.fail((jqHXR, textStatus) => {
			alert(`Request failed (${textStatus}): ${jqHXR.responseText}`);
		});
	});
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
		element: "#newform",
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
					url: "/admin/ajax_select/ajax_lookup/member?term=" + filter,
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
});
