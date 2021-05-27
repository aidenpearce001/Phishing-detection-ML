function searchToggle(obj, evt){
    var container = $(obj).closest('.search-wrapper');
        var x = document.getElementById("searchTxt").value;
        if(!container.hasClass('active')){
            container.addClass('active');
            evt.preventDefault();
        }
        else if(container.hasClass('active') && $(obj).closest('.input-holder').length == 0){
            container.removeClass('active');
            // clear input
            container.find('.search-input').val('');
        }
}

$(document).ready(function(){
    $("#submit").on('click', function(){
        $.ajax({
            type: "POST",
            url: '/survey',
            data: $("#form").serialize(), 
            processData: false,
            dataType: 'json',
            success: function(data)
            {
                console.log(data); 
            }
        });
    });
});

$("#linksubmit").submit(function(e) {
    alert(1);
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    
    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
               alert(data); // show response from the php script.
           }
         });

    
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();   
});