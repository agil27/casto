function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
}

$(document).ready(function () {
    let explore_btn = $("#explore_btn")
    let upload_btn = $("#upload_btn")
    let file_input = $("#file_input")
    let file_addr = $("#file_addr")
    let web_addr = $("#web_addr")
    let logout_btn = $("#logoutBtn")
    let delete_btns = $(".delete-btn")
    let delete_all_btn = $("#delete-all-btn")

    $("#function_block").hide()

    logout_btn.click(function () {
        window.location.replace("../../logout/")
    })

    delete_btns.each(function () {
        this.onclick = function () {
            console.log(this)
            let operation_id = this.id
            $.post(
                "../delete/",
                {"ids": [operation_id]},
                function (res) {
                    window.location.replace("../dashboard/")
                }
            )
        }
    })

    delete_all_btn.click(function () {
        let ids = []
        let checkboxes = $(".checkbox")
        checkboxes.each(function () {
            if (this.checked && this.id !== "checkall") {
                ids.push(this.id.substring(11))
            }
        })
        $.post(
            "../delete/",
            {"ids": ids},
            function (res) {
                window.location.replace("../dashboard/")
            }
        )
    })

    $("#checkall").click(function () {
        $(".checkbox").prop("checked", this.checked)
    })


    $("#query-btn").click(function() {
        date1 = $("#date1").val()
        date2 = $("#date2").val()
        console.log(date1, date2)
        if (date1.length > 0 && date2.length > 0) {
            href_path = "../dashboard/?range=yes"
            href_time1 = "&start=" + date1
            href_time2 = "&end=" + date2
            window.location.replace(href_path + href_time1 + href_time2)
        }
    })

    if (GetQueryString("range") === "yes") {
        $("#timequery").addClass("active")
        $("#allrecord").removeClass("active")
    }
})