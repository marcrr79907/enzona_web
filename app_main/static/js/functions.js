function messaje_error(obj) {
    var html = '<ul>';
    $.each(obj, function (key, value) {
        html += '<li>' + key + ': ' + value + '</li>';
    });
    html += '</ul>';
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}