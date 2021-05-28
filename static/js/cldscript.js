$(document).ready(function(){
    $("#submit").on('click', function(){
        $.ajax({
            type: "POST",
            url: '/survey',
            data: $("#form").serialize(), 
            cache: 'false',
            processData: false,
            dataType: 'json',
            success: function(data)
            {
                console.log(data); 
            },
            error: function(data)
            {
                console.log(data); 
                console.log("error");
            }
        })
        .done(function(data) {
            if (data.notsafe) {
                swal({
                    title: data.notsafe,
                    text: "Score :"+data.score,
                    icon: "error",
                    });
                console.log(data);
            }
            if (data.safe){
                swal({
                    title: data.safe,
                    text: "Score :"+data.score,
                    icon: "success",
                    });
            }
        });
        event.preventDefault();
    });
});


$(document).ready(function(){
    $("#feedback").on('click', function(){
        $.ajax({
            type: "POST",
            url: '/feedback',
            data: $("#form").serialize(), 
            cache: 'false',
            processData: false,
            dataType: 'json',
            success: function(data)
            {
                console.log(data); 
            },
            error: function(data)
            {
                console.log(data); 
                console.log("error");
            }
        })
  
    });
});