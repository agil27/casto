function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}

$(document).ready(function() {
    let explore_btn = $("#explore_btn")
    let upload_btn = $("#upload_btn")
    let file_input = $("#file_input")
    let file_addr = $("#file_addr")
    let web_addr = $("#web_addr")
    let logout_btn = $("#logoutBtn")
    let detect_btn = $("#detect_btn")
    let gender_btn = $("#gender_btn")

    $("#function_block").hide()

    explore_btn.click(function() {
        file_input.click()
    }) 

    file_input.change(function() {
        file_addr.val(file_input.val())
        let formData = new FormData();
        formData.append("image", file_input[0].files[0]);
        $.ajax({
            url: "../operation/upload/",
            type:'post',
            data: formData,
            contentType: false,
            processData: false,
            success: function(res){
                console.log(res)
                if (res.addr) {
                    $("#preview").attr("src", "../static/" + res.addr)
                    upload_btn.attr("disabled", true)
                    file_addr.attr("disabled", true)
                    explore_btn.attr("disabled", true)
                    file_addr.attr("disabled", true)
                    $("#file_desc").text("本地图片已经上传")
                    $("#web_desc").text("已禁用网络上传")
                    $("#status").text("图片已经上传，请选择您的服务")
                    $("#function_block").show()
                }           
                else if (res.error) {
                    $("#file_desc").text("本地图片上传失败，请重新选择")
                }    
            }
        })
    })

    upload_btn.click(function() {
        let file_web = web_addr.val()
        console.log(file_web)
        $.post(
            "../operation/upload/", 
            {"url": file_web},
            function(res) {
                console.log(res)
                if (res.addr) {
                    $("#preview").attr("src", "../static/" + res.addr)
                    upload_btn.attr("disabled", true)
                    file_addr.attr("disabled", true)
                    explore_btn.attr("disabled", true)
                    file_addr.attr("disabled", true)
                    $("#file_desc").text("已禁用本地上传")
                    $("#web_desc").text("网络图片已上传")
                    $("#status").text("图片已经上传，请选择您的服务")
                    $("#function_block").show()
                }
                else if (res.error) {
                    $("#web_desc").text("网络图片上传失败，请换一张")
                }
            }
        )
    })

    detect_btn.click(function() {

    })

    gender_btn.click(function() {

    })
    
    logout_btn.click(function() {
        window.location.replace("../logout")
    })
})