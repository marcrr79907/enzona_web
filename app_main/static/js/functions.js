function messaje_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    }
    else {
        html = '<p>' + obj + '</p>'
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

function confirm(params) {
    $.confirm({
        title: 'Confirm!',
        content: params,
        buttons: {
            confirm: function () {
                $.alert('Confirmed!');
            },
            cancel: function () {
                $.alert('Canceled!');
            },
            somethingElse: {
                text: 'Something else',
                btnClass: 'btn-blue',
                keys: ['enter', 'shift'],
                action: function () {
                    $.alert('Something else?');
                }
            }
        }
    });
}

function alert(messaje) {
    Swal.fire({
        title: 'Error!',
        text: messaje,
        icon: 'error'
    });
}