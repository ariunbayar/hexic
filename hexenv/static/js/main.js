$(document).ready(function(){
    $('#language-select a').click(function(){
        var lang = $(this).attr('lang');
        $('#language-submit input:[name=language]').val(lang);
        $('#language-submit').submit();
        return false;
    });

});
