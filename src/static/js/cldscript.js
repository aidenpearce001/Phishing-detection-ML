$(document).ready(function(){
    $("#submit").on('click', function(){
        $.ajax({
            type: "POST",
            url: '/',
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
        $('#reportModal').modal('hide');
        $.ajax({
            type: "POST",
            url: '/feedback',
            data: {
                title : document.getElementById("slct").value,
                content : document.getElementById("comment_text").value
            },
            success: function(data)
            {
                console.log('success'); 
                swal({
                    title: "Send Feedback success",
                    text: "Thanks for your feedback",
                    icon: "success",
                });
            },
            error: function(data)
            {
                console.log("error");
            }
        })
    });
});