$(document).ready(function () {
    $('.show').click(function (e) {
        e.preventDefault();
        var that = this;
        $.ajax({
            url: '/users/1/show',
            method: 'GET',
            success: function (data) {
                console.log(data);
                $(that).parent().append(`<div>${data.email}</div>`);
            },
            error: function () {

            }
        })
    })
});