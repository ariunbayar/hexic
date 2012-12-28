$(function(){
    $('.close').click(function(){
        var parent_class = $(this).attr('dismiss');
        $(this).parent("." + parent_class).remove();
    });
})
