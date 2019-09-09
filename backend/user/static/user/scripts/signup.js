function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
}

function onSignupClicked() {
    console.log("Signup Button Clicked")
    let name = $("#username").val()
    let pwd = $("#password").val()
    console.log(name, pwd)
    if (name.length === 0 || pwd.length === 0) {
        return
    }
    else {
        let data = {
            username: name,
            password: pwd
        }
        console.log(data)
        $.post("../signup/", data, function (res) {
            if (res.status == 'True') {
                window.location.replace("../login/");
            } else {
                $("#authInfo").text(res.error)
            }
        })
    }
}

$(document).ready(function () {
    let signup_btn = $("#btnSignup")
    signup_btn.click(onSignupClicked)
    $("#username").val(GetQueryString("name"))
})