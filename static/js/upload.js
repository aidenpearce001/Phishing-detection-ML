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
