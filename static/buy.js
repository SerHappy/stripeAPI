var button = document.getElementById("clickMe");

button.addEventListener("click", function () {
  /**
   * When the customer clicks on the button, redirect
   * them to Checkout.
   */

  var stripe = Stripe("pk_test_TYooMQauvdEDq54NiTphI7jx");

  var my_string = $("#url").attr("data-url");
  var url = document.location.origin + my_string;

  const request = new Request(url);

  fetch(request)
    .then(function (response) {
      return response.json();
    })
    .then(function (session) {
      return stripe.redirectToCheckout({ sessionId: session.session_id });
    })
    .then(function (result) {
      if (result.error) {
        alert(result.error.message);
      }
    });
});
