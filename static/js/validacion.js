$('.max').on("keypress",function(){
    var l = $(this).val();
    if (l.length >= 50){

        $(this).val(l.slice(0,50));
        $(this).parent().addClass("has-error");
    }else{
        $(this).parent().removeClass("has-error");
    }

});

$('.numero').on("keyup",function(){
    var l = $(this).val();
    var n = l.length
    if(n >= 5){
        $(this).val(l.slice(0,5));

    }
    else if (isNaN(l)){
        $(this).val(l.slice(0,n-2));
    }

});

$('#myForm').on("submit",function(){
    $('#upload').attr("disabled",true);
});

