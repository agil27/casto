function onSignupClicked() {
    console.log("Signup Button Clicked")
    let name = $("#username")
    let pwd = $("#password")
    if (length(username) == 0 || length(password) == 0) {
        return
    }
    else {
        let data = {
            username: name,
            password: pwd
        }
        $.post("../dashboard/", data, function(res) {
            console.log(res)
        })
    }
}

$(document).ready(function() {
    let signup_btn = $("#btnSignup")
    signup_btn.click(onSignupClicked)
})