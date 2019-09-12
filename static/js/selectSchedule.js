$(function(){
    $('#prev').click(function (e) {
        let actual = $('.formato-actual');
        let update = actual.prev();
        if(update.hasClass('formato')){
            actual.hide();
            actual.removeClass('formato-actual');
            update.show();
            update.addClass('formato-actual');
            let selectorActual= $('.actual');
            selectorActual.removeClass("actual active");
            selectorActual.prev().addClass("actual active");
            }
        });

    $('#next').click(function (e) {
        let actual = $('.formato-actual');
        let update = actual.next();
        if(update.hasClass('formato')){
            actual.hide();
            actual.removeClass('formato-actual');
            update.show();
            update.addClass('formato-actual');
            let selectorActual= $('.actual');
            selectorActual.removeClass("actual active");
            selectorActual.next().addClass("actual active");
            }
        });

    $('.selectorFormato').click(function (e) {
        let actual = $(this);
        let num = actual.index();
        $('.formato').removeClass('formato-actual').hide();
        let formatoActual= $('.formato').eq(num-1);
        formatoActual.addClass('formato-actual');
        formatoActual.show();
        $('.selectorFormato').removeClass("active actual");
        actual.addClass("active actual");
        });

    $('#print').click(function(){
            let printContents = $('.formato-actual').html();
            let originalContents = document.body.innerHTML;
            document.body.innerHTML = printContents;
            window.print();
            document.body.innerHTML = originalContents;
    });
});

$( window ).on( "load", function(){
    $('.formato').first().addClass('formato-actual');
    $('.formato-actual').show();
    $('.selectorFormato').first().addClass('active actual');
} );
