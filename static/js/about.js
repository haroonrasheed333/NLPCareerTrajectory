$(document).ready(function () {

  $('#logo-img-about').click(function() {
        sessionStorage.removeItem('response');
        sessionStorage.removeItem('university');
        sessionStorage.removeItem('tree_json');
        console.log("hhh");
        location.href = location.origin + '/';
    });
});