$(document).ready(function () {
    // Make login card visible with animation
    $('.fade-in').addClass('visible');

    // Icon animations on hover
    $('.logo-icon').hover(
        function () {
            $(this).addClass('rotate');
        },
        function () {
            $(this).removeClass('rotate');
        }
    );

    // Input focus animations
    $('.form-control').focus(function () {
        $(this).parent().find('i').addClass('pulse');
    }).blur(function () {
        $(this).parent().find('i').removeClass('pulse');
    });

    // Button click animation and AJAX login
    $('.btn-login').click(function (e) {
        e.preventDefault();

        const username = $('#username').val();
        const role = 'user'; // or fetch from a dropdown

        $.ajax({
            url: '/auth/login',
            method: 'POST',
            data: {
                username: username,
                role: role
            },
            success: function (response) {
                console.log(response);
                if (response.isSuccess) {
                    window.location.href = response.url;
                } else {
                    alert(response.message);
                }
            },
            error: function (xhr) {
                alert('Login failed: ' + xhr.responseJSON?.message || 'Unknown error');
            }
        });
    });


    // Add CSS for ripple effect
    $('<style>')
        .prop('type', 'text/css')
        .html(`
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `)
        .appendTo('head');
});
