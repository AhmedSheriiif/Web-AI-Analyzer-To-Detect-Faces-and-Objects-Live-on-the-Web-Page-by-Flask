
var mysubmit1=document.getElementById("mysubmit1")
var objectinput = document.getElementById("object")
var emotionalinput = document.getElementById("emotional")
var imageinput = document.getElementById("image")
var videoinput = document.getElementById("video")
var camerainput = document.getElementById("camera")
objectinput.addEventListener("change",function(){
    if(objectinput.checked == true ){
        if(imageinput.checked == true || videoinput.checked == true || camerainput.checked == true){
            mysubmit1.disabled = false

        }
    }else{
        mysubmit1.disabled = true
    
    }
})
emotionalinput.addEventListener("change",function(){
    if(emotionalinput.checked == true ){
        if(imageinput.checked == true || videoinput.checked == true || camerainput.checked == true){
            mysubmit1.disabled = false

        }
    }else{
        mysubmit1.disabled = true
    
    }
})

imageinput.addEventListener("change",function(){
    if(imageinput.checked == true ){
        if(objectinput.checked == true || emotionalinput.checked == true ){
            mysubmit1.disabled = false

        }
    }else{
        mysubmit1.disabled = true
    
    }
})
videoinput.addEventListener("change",function(){
    if(videoinput.checked == true ){
        if(objectinput.checked == true || emotionalinput.checked == true ){
            mysubmit1.disabled = false

        }
    }else{
        mysubmit1.disabled = true
    
    }
})
camerainput.addEventListener("change",function(){
    if(camerainput.checked == true ){
        if(objectinput.checked == true || emotionalinput.checked == true ){
            mysubmit1.disabled = false

        }
    }else{
        mysubmit1.disabled = true
    
    }
})









