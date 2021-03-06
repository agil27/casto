function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}

function onLoginBtnClicked() {
    console.log("Login Button Clicked")
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
        $.post("../login/", data, function(res) {
            console.log(res)
            if (res.status) {
                console.log('replace')
                window.location.replace("../dashboard/")
            } else {
                $("#authInfo").text(res.error)
            }
        })
    }
}

$(document).ready(function() {
    let login_btn = $("#btnLogin")
    login_btn.click(onLoginBtnClicked)
})