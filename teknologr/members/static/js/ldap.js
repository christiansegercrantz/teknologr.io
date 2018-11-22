function validatePassword(){
  var password = $('#ldap_password');
  var confirm = $('#confirm_password');
  if(password.val() != confirm.val()) {
    confirm[0].setCustomValidity("Lösenorden är olika");
    confirm.addClass('is-invalid');
  } else if(confirm.val().length <= 0) {
    confirm.removeClass('is-invalid is-valid');
  } else {
    confirm[0].setCustomValidity('');
    confirm.removeClass('is-invalid').addClass('is-valid');
  }
}

$(document).ready(function() {
  $('#addldapform').submit(function(event){
    event.preventDefault();
    var data = $(this).serialize();
    var id = $(this).data('id')
    var request = $.ajax({
      url: "/api/accounts/ldap/" + id + "/",
      method: "POST",
      data: data
    });

    request.done(function() {
      location.reload();
    });

    request.fail(function(jqHXR, textStatus ) {
      alert( "Request failed (" + textStatus + "): " + jqHXR.responseText );
    });
  });

  $('#changeldappwform').submit(function(event){
    event.preventDefault();
    var data = $(this).serialize();
    var id = $(this).data('id')
    var request = $.ajax({
      url: "/api/accounts/ldap/change_pw/" + id + "/",
      method: "POST",
      data: data
    });

    request.done(function() {
      location.reload();
    });

    request.fail(function(jqHXR, textStatus ) {
      alert( "Request failed (" + textStatus + "): " + jqHXR.responseText );
    });
  });

  $('#confirm_password').keyup(validatePassword);
  $('#ldap_password').change(validatePassword)

  $('#delldap').click(function() {
    if(confirm("Vill du ta bort detta LDAP konto?")){
      var id = $(this).data('id');
      var request = $.ajax({
        url: "/api/accounts/ldap/" + id + "/",
        method: "DELETE",
      })

      request.done(function() {
        location.reload();
      });

      request.fail(function(jqHXR, textStatus ) {
        alert( "Request failed (" + textStatus + "): " + jqHXR.responseText );
      });
    }
  });

  $('#addbill').click(function() {
    var id = $(this).data('id');
    var request = $.ajax({
      url: "/api/accounts/bill/" + id + "/",
      method: "POST",
      data: {"member_id": id}
    })

    request.done(function() {
      location.reload();
    });

    request.fail(function(jqHXR, textStatus ) {
      alert( "Request failed (" + textStatus + "): " + jqHXR.responseText );
      });
  });

  $('#delbill').click(function() {
    if(confirm("Vill du ta bort detta BILL konto?")){
      var id = $(this).data('id');
      var request = $.ajax({
        url: "/api/accounts/bill/" + id + "/",
        method: "DELETE",
      })

      request.done(function() {
        location.reload();
      });

      request.fail(function(jqHXR, textStatus ) {
        alert( "Request failed (" + textStatus + "): " + jqHXR.responseText );
      });
    }
  });
});
