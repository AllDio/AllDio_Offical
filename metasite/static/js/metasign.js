$('.invite').on("change keyup paste",
    function () {
        if ($(this).val().length > 8) {
            if ($(this).val().indexOf('-') > 0) {
                if ($(this).val()) {
                    $('.icon-invite').addClass("next");
                } else {
                    $('.icon-invite').removeClass("next");
                }
            } else {
                $('.icon-invite').removeClass("next");
            }
        } else {
            $('.icon-invite').removeClass("next");
        }
    }
);


$('.email').on("change keyup paste",
    function () {
        if ($(this).val().indexOf('@') > 0) {
            if ($(this).val().indexOf('.') > 0) {
                if ($(this).val()) {
                    $('.icon-paper-plane').addClass("next");
                } else {
                    $('.icon-paper-plane').removeClass("next");
                }
            } else {
                $('.icon-paper-plane').removeClass("next");
            }
        } else {
            $('.icon-paper-plane').removeClass("next");
        }
    }
);

// $('.next-button.email').click(
//     function () {
//         console.log("Something");
//         $('.email-section').addClass("fold-up");
//         $('.code-section').removeClass("folded");
//     }
// );


$('.code').on("change keyup paste",
    function () {
        if ($(this).val()) {
            $('.icon-qrcode').addClass("next");
        } else {
            $('.icon-qrcode').removeClass("next");
        }
    }
);

// $('.next-button.code').click(
//     function () {
//         console.log("Something");
//         $('.code-section').addClass("fold-up");
//         $('.password-section').removeClass("folded");
//     }
// );


$('.password').on("change keyup paste",
    function () {
        if ($(this).val()) {
            $('.icon-lock').addClass("next");
        } else {
            $('.icon-lock').removeClass("next");
        }
    }
);

$('.next-button.password').click(
    function () {
        console.log("Something");
        $('.password-section').addClass("fold-up");
        $('.repeat-password-section').removeClass("folded");
    }
);


$('.repeat-password').on("change keyup paste",
    function () {
        if ($(this).val()) {
            $('.icon-repeat-lock').addClass("next");
        } else {
            $('.icon-repeat-lock').removeClass("next");
        }
    }
);

// $('.next-button.repeat-password').click(
//     function () {
//         console.log("Something");
//         $('.repeat-password-section').addClass("fold-up");
//         $('.signsuccess').css("marginTop", 0);
//     }
// );

$('.next-button').hover(
    function () {
        $(this).css('cursor', 'pointer');
    }
);

$('.username').on("change keyup paste",
    function () {
        if ($(this).val().indexOf('@') > 0) {
            if ($(this).val().indexOf('.') > 0) {
                if ($(this).val()) {
                    $('.icon-username').addClass("next");
                } else {
                    $('.icon-username').removeClass("next");
                }
            } else {
                $('.icon-username').removeClass("next");
            }
        } else {
            $('.icon-username').removeClass("next");
        }
    }
);

$('.next-button.username').click(
    function () {
        console.log("Something");
         $('#loginpassword').removeAttr('disabled', 'disabled');
        $('.username-section').addClass("fold-up");
        $('.loginpassword-section').removeClass("folded");

    }
);


$('.loginpassword').on("change keyup paste",
    function () {
        if ($(this).val()) {
            $('.icon-loginpassword').addClass("next");
        } else {
            $('.icon-loginpassword').removeClass("next");
        }
    }
);

// $('.next-button.loginpassword').click(
//     function () {
//         console.log("Something");
//         $('.loginpassword-section').addClass("fold-up");
//         $('.logsuccess').css("marginTop", 0);
//     }
// );


$('.resetusername').on("change keyup paste",
    function () {
        if ($(this).val().indexOf('@') > 0) {
            if ($(this).val().indexOf('.') > 0) {
                if ($(this).val()) {
                    $('.icon-resetusername').addClass("next");
                } else {
                    $('.icon-resetusername').removeClass("next");
                }
            } else {
                $('.icon-resetusername').removeClass("next");
            }
        } else {
            $('.icon-resetusername').removeClass("next");
        }
    }
);

// $('.next-button.resetusername').click(
//     function () {
//         console.log("Something");
//         $('.resetusername-section').addClass("fold-up");
//         $('.resetemailcode-section').removeClass("folded");
//     }
// );

$('.resetemailcode').on("change keyup paste",
    function () {
        if ($(this).val()) {
            $('.icon-resetemailcode').addClass("next");
        } else {
            $('.icon-resetemailcode').removeClass("next");
        }
    }
);

// $('.next-button.resetemailcode').click(
//     function () {
//         console.log("Something");
//         $('.resetemailcode-section').addClass("fold-up");
//         $('.resetloginpassword-section').removeClass("folded");
//     }
// );


$('.resetloginpassword').on("change keyup paste",
    function () {
        if ($(this).val()) {
            $('.icon-resetloginpassword').addClass("next");
        } else {
            $('.icon-resetloginpassword').removeClass("next");
        }
    }
);

$('.next-button.resetloginpassword').click(
    function () {
        console.log("Something");
        $('.resetloginpassword-section').addClass("fold-up");
        $('.resetconfirmpassword-section').removeClass("folded");
    }
);

$('.resetconfirmpassword').on("change keyup paste",
    function () {
        if ($(this).val()) {
            $('.icon-resetconfirmpassword').addClass("next");
        } else {
            $('.icon-resetconfirmpassword').removeClass("next");
        }
    }
);

// $('.next-button.resetconfirmpassword').click(
//     function () {
//         console.log("Something");
//         $('.resetconfirmpassword-section').addClass("fold-up");
//         $('.resetsuccess').css("marginTop", 0);
//     }
// );