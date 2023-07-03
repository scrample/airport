function billets(){
    if (document.getElementById("cards_wrapper").style.display == 'none') document.getElementById("cards_wrapper").style.display = 'block';
        else document.getElementById("cards_wrapper").style.display = 'none';
}
function Soldbillets(){
    if (document.getElementById("Sold").style.display == 'none') document.getElementById("Sold").style.display = 'block';
        else document.getElementById("Sold").style.display = 'none';
}
function Client(){
    if (document.getElementById("client").style.display == 'none') document.getElementById("client").style.display = 'block';
        else document.getElementById("client").style.display = 'none';
}
$(document).ready(function() {
    var $elements = $('#cards_wrapper .card');
    $('#findinput').on('keyup input', function() {
        var value = this.value;
        $elements.hide();
        $elements.filter(':contains("' + value + '")').show();
       if (value == '') {$elements.show()} 
    });
});
