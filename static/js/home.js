$(function(){
    $(document).on('change', '.list', function (e) {
        var selector = $(this).parents('.item').find('.number');
        var numSecciones = $("option:selected",this).attr('secc');
        selector.empty();
        selector.append($('<option></option>').attr('value',0).text("todas"));
        for(i=1;i<= numSecciones;i++){
            selector.append($('<option></option>').attr('value',i).text(i));
        }
        e.preventDefault();
    });

    $("#add").click(function(e){      
        $('#courses').prepend($('#template').html());
        $('.item').length > 2 ? $('#courses .delete').show() : $('#courses .delete').hide();
        $('.item').length > 8 ? $('#add').fadeOut() : $('#add').fadeIn();
        updateList();
        e.preventDefault();
        return false;
    });

    $('#career').change(function(){
        $('#template .course [major!="grl"]').addClass('hide');
        $('#template .course [major~="' + $(this).val() +'"]').removeClass('hide');
        $("#schedule").removeClass('hide');
        $('#courses').empty().prepend($('#template').html());
        $('#courses .course').attr("name",'course_0');
        $('#courses .number').attr("name",'number_0');
        $('#courses .delete').hide();
    });

    $(document).on('click', '.delete', function (e) {
        $(this).parents('.item').remove();
        $('.item').length > 2 ? $('#courses .delete').show() : $('#courses .delete').hide();
        $('.item').length > 8 ? $('#add').fadeOut() : $('#add').fadeIn();
        updateList();
        e.preventDefault();
    });
});


function updateList() {
    let i=0;
    $('#courses .course').each(function(){
        $(this).attr("name",'course_'+i)
        i++;
    });
    i=0;
    $('#courses .number').each(function(){
        $(this).attr("name", 'number_'+i)
        i++;
    });
}