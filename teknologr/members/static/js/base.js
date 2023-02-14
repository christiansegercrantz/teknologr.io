// Sidebar ajax search delay timer
var timer;

/**
 * Extend the functionality of the AutoCompleteSelectMultipleField from django-ajax-selects by also allowing new members to be created simultaneously. This is how it's done:
 * 1. Add click-listener to a button
 * 2. When clicked, the name is taken from the member search box
 * 3. The name is appended to the hidden input and appended to the list
 * 4. A button for removing the name is also created
 * 5. When the form is submitted, the api endpoint handles splitting the hidden input and creating new members
 */
const add_ajax_multiselect_extension = ({ selector_button, selector_input, selector_hidden_input, selector_deck }) => {
	$(selector_button).click(e => {
		e.preventDefault();

		const input = $(selector_input);
		const name = input.val().trim();
		if (!name || !name.includes(" ") || name.includes("|") || name.includes("$")) return;
		input.val("");

		const hidden_input = $(selector_hidden_input);

		// Add name to hidden (real) input
		const substring = `$${name}|`;
		hidden_input.val(hidden_input.val() + substring);

		// Keep track of the amount of names added
		const data = hidden_input.data();
		data.counter = (data.counter || 0) + 1;

		// Add name to list
		const div = $("<div>", {
			html: `<b>Ny:</b> ${name}`,
		}).appendTo(selector_deck);

		// Create button for removing the name from the list
		$("<span>", {
			class: "ui-icon ui-icon-trash",
			text: "X",
			click: () => {
				const value = hidden_input.val();
				const i = value.indexOf(substring);
				hidden_input.val(value.slice(0, i) + value.slice(i + substring.length));
				hidden_input.data().counter--;
				div.remove();
			},
		}).prependTo(div);
	});
}

$(document).ready(function() {
	$("#newform").submit(function(event){
		var active = $(this).data('active');
		switch(active) {
			case 'members':
				var apipath = 'members'
				break;
			case 'groups':
				var apipath = 'groupTypes'
				break;
			case 'functionaries':
				var apipath = 'functionaryTypes'
				break;
			case 'decorations':
				var apipath = 'decorations'
				break;
		}


		var request = $.ajax({
			url: "/api/" + apipath + "/",
			method: 'POST',
			data: $(this).serialize()
		});

		request.done(function(msg) {
			window.location = "/admin/"+ active +"/" + msg.id + "/";
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});

		event.preventDefault();
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

	/**
	 * Populate "create new xyz" modal form with the current search box value.
	 */
	$("#side-new").click(() => {
		const search = $("#side-search");
		const value = search.val();
		switch (search.data("active")) {
			case "members": {
				const names = value.split(" ").filter(s => s);
				const last = names.splice(names.length - 1, 1);
				$("#mmodal_given_names").val(names.join(" "));
				$("#mmodal_surname").val(last);
			} break;
			case "decorations": $("#dform_name").val(value); break;
			case "groups": $("#gtform_name").val(value); break;
			case "functionaries": $("#ftform_name").val(value); break;
		}
	});

    $('#choose-multiple-applicants').submit(function(event) {
        const data = $(this).serialize();
        const request = $.ajax({
            url: '/api/multiApplicantSubmission/',
            method: 'POST',
            data: data,
        });

        request.done(function() {
            window.location = '/admin/applicants/';
        });

        request.fail(function(jqHXR, textStatus) {
            alert('Request failed: ' + textStatus + ': ' + jqHXR.responseText);
        });

        event.preventDefault();
    });

});
