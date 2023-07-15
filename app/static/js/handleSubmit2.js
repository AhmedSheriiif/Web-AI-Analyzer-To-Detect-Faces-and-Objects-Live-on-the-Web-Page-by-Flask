
var videoInput=document.getElementById("video")
var mysubmit1=document.getElementById("mysubmit1")
// var errfile=document.getElementById("errorfile")
// var filesel=false
// var cpuinput = document.getElementById("cpu")
// var gpuinput = document.getElementById("gpu")



videoInput.addEventListener("change",function(){

    if(videoInput.value == ""){
        mysubmit1.disabled = true
    }else{

        mysubmit1.disabled = false

    }

})

