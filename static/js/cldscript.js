// function mysubmit() {
//     $.ajax({
//         type: "POST",
//         url: '/survey',
//         data: $("#form").serialize(), 
//         processData: false,
//         dataType: 'json',
//         success: function(data) {
//             console.log('ok');
//         },
//         error: function(data) {
//             console.log('error');
//             alert(data);
//             location.reload();  
//         }
//         });
// }; 

$(function(){
	$('button').click(function(){
        alert(1);
		var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();
		$.ajax({
			url: '/signUpUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});

// $("#submit").on('click', function(){
//     $.ajax({
//         type: "POST",
//         url: '/survey',
//         data: $("#form").serialize(), 
//         processData: false,
//         dataType: 'json',
//         success: function(data)
//         {
//             console.log(data); 
//         }
//     });
// });

// $("#linksubmit").submit(function(e) {
//     alert(1);
//     e.preventDefault(); // avoid to execute the actual submit of the form.

//     var form = $(this);
//     var url = form.attr('action');
    
//     $.ajax({
//            type: "POST",
//            url: url,
//            data: form.serialize(), // serializes the form's elements.
//            success: function(data)
//            {
//                alert(data); // show response from the php script.
//            }
//          });

    
// });

