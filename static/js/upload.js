var _validFileExtensions = [".csv"];    

"use strict";
let sleep = (time) => new Promise(resolve => setTimeout(resolve, time));
let upload = document.querySelector(".upload");
let uploadBtn = document.querySelector(".upload__button");
uploadBtn.addEventListener("click", async () => {
    upload.classList.add("uploading");
    await sleep(3000);
    upload.classList.add("uploaded");
    await sleep(2000);
    upload.classList.remove("uploading");
    upload.classList.add("uploaded-after");
    await sleep(1000);
    upload.className = "upload";
});
document.addEventListener('click', function (event) {
    if (!event.target.matches('.click-me'))
        return;
    console.log(event.target);
    document.getElementById("file").click();
}, false);

// var input = document.getElementById( 'file-upload' );

document.getElementById("file-upload").addEventListener("change", showFileName );

function showFileName( event ) {
  
  // the change event gives us the input it occurred in 
  var input = event.srcElement;
  
  var fileName = input.files[0].name;

  console.log(fileName)
  document.getElementById("filename").innerHTML = fileName
  
}

$(function() {
    $('#upload').click(function() {
    event.preventDefault();
    let form_data = new FormData($('#uploadform')[0]);
    // console.log($('#uploadform')[0]);
    form_data.append("file", $('input[type=file]')[0].files[0])

    console.log(form_data);
    $.ajax({
        type : "POST",
        url : "/comparison",
        contentType: false,
        cache: false,
        processData: false,
        data: form_data,
        success: function(data) {
            // alert(val);
            console.log(data);
        }
    })
    })
});