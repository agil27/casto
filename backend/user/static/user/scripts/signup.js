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
        $.post("../signup/", data, function(res) {
            if (res.status) {
                window.location.replace("../login/");
            }
        })
    }
}

$(document).ready(function() {
    let signup_btn = $("#btnSignup")
    signup_btn.click(onSignupClicked)
})