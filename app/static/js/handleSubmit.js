var fileInput=document.getElementById("file")
var mysubmit1=document.getElementById("mysubmit1")

// cpuinput.addEventListener("change",function(){
//     if(cpuinput.checked == true ){
//         fileInput.disabled = false
//     }else{
//         fileInput.disabled = true
    
//     }
// })
// gpuinput.addEventListener("change",function(){
//     if(gpuinput.checked == true ){
//         fileInput.disabled = false
//     }else{
//         fileInput.disabled = true
    
//     }
// })



fileInput.addEventListener("change",function(){

    if(fileInput.value == ""){

        mysubmit1.disabled = true
    }else{
        mysubmit1.disabled = false

    }

})




