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
  $('#confirm_password').keyup(validatePassword);
  $('#ldap_password').change(validatePassword)

  // Create an LDAP account for the selected user
  add_request_listener({
    selector: "#add-ldap-form",
    method: "POST",
    url: element => `/api/accounts/ldap/${element.data('id')}/`,
  });
  // Delete the LDAP account for the selected user
  add_request_listener({
    selector: "#delete-ldap-button",
    method: "DELETE",
    url: element => `/api/accounts/ldap/${element.data('id')}/`,
    confirmMessage: "Vill du ta bort detta LDAP konto?",
  });
  // Change the LDAP password for the selected user
  add_request_listener({
    selector: "#change-ldappw-form",
    method: "POST",
    url: element => `/api/accounts/ldap/change_pw/${element.data('id')}/`,
  });

  // Create a BILL account for the selected memeber
  add_request_listener({
    selector: "#add-bill-button",
    method: "POST",
    url: element => `/api/accounts/bill/${element.data('id')}/`,
    data: element => ({ "member_id": element.data('id') }),
  });
  // Delete the BILL account for the selected memeber
  add_request_listener({
    selector: "#delete-bill-button",
    method: "DELETE",
    url: element => `/api/accounts/bill/${element.data('id')}/`,
    confirmMessage: "Vill du ta bort detta BILL konto?",
  });
});
