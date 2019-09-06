$("#signupBtn").click(function() {
    window.location.replace("../signup/?name=" + $("#username").val())
})

$("#logoutbtn").click(function() {
    window.location.replace("../logout/")
})