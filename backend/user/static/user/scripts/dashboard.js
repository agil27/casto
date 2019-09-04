$(document).ready(function() {
    let explore_btn = $("#explore_btn")
    let file_input = $("#file_input")
    let file_addr_text = $("#file_addr")
    explore_btn.click(function() {
        file_input.click()
    }) 
    file_input.change(function() {
        file_addr_text.val(file_input.val())
    })
})