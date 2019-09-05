function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}

$(document).ready(function() {
    let explore_btn = $("#explore_btn")
    let file_input = $("#file_input")
    let file_addr_text = $("#file_addr")
    let logout_btn = $("#logoutBtn")

    explore_btn.click(function() {
        file_input.click()
    }) 

    file_input.change(function() {
        file_addr_text.val(file_input.val())
    })

    logout_btn.click(function() {
        window.location.replace("../logout")
    })
})