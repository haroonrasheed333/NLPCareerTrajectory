$(document).ready(function () {

  $('#logo-img-about').click(function() {
        sessionStorage.removeItem('response');
        console.log("hhh");
        location.href = location.origin + '/';
    });
});