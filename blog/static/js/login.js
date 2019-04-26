$(function () {
    // 获取输入框，监听失去焦点状态
    $("[name=uname]").blur(function () {
        if($(this).val().length == 0 || $(this).val() == " "){
            $(this).siblings("span").html("用户名不能为空").css("color","red")
        }
    })
})