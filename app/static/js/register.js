var fullname=document.getElementById("name")
var user=document.getElementById("username")
var user1=document.getElementById("user")
var email=document.getElementById("email")

var phone=document.getElementById("phone")

var pass1=document.getElementById("pass1")
var pass2=document.getElementById("pass2")

var radio1=document.getElementById("dot-1")
var radio2=document.getElementById("dot-2")
var radio3=document.getElementById("dot-3")

var submitbtn1=document.getElementById("submitbtn")


// paragraph errors
var errorname=document.getElementById("nameerr")
var erroruser=document.getElementById("usererr")
var erroruser1=document.getElementById("usererr1")
var erroremail=document.getElementById("emailerr")
var errorphone=document.getElementById("phoneerr")
var errorpass1=document.getElementById("pass1err")
var errorpass2=document.getElementById("pass2err")
var errorgender=document.getElementById("gendererr")



var subname="false"
var subuser="false"
var subuser10="false"
var subemail="false"
var subphone="false"
var subpass1="false"
var subpass2="false"

// fullname regex
// ===========================================================

fullname.addEventListener("blur",function(){
    this.style.border="2px solid red"


    var namereg=/^[a-zA-Z]{4,16}$/i
    var namevalid=namereg.test(fullname.value)

    if(!namevalid){
        errorname.style.display="block";
        errorname.style.color="red";

        errorname.innerHTML="name should be beteen 4 and 16 char"
        this.focus()
    }else{

       
        errorname.style.color="green";
        this.style.border="2px solid green"

        errorname.innerHTML="valid name"
        errorname.style.display="block";
        subname="true"
    }

})

// =================================================================
// username regex
user.addEventListener("blur",function(){
    this.style.border="2px solid red"


    var userreg1=/^[a-zA-Z]{6,20}$/i
    var uservalid1=userreg1.test(this.value)

    if(!uservalid1){
        erroruser1.style.display="block";
        erroruser1.style.color="red";

        erroruser1.innerHTML="user-name should be beteen 6 and 20 char"
        this.focus()
    }else{

       
        erroruser1.style.color="green";
        this.style.border="2px solid green"

        erroruser1.innerHTML="valid user-name"
        erroruser1.style.display="block";
        subuser10="true"
        
    }
})

// ===============================================================
// last name regex
user1.addEventListener("blur",function(){
    this.style.border="2px solid red"


    var userreg=/^[a-zA-Z]{4,14}$/i
    var uservalid=userreg.test(this.value)

    if(!uservalid){
        erroruser.style.display="block";
        erroruser.style.color="red";

        erroruser.innerHTML="last-name should be beteen 4 and 14 char"
        this.focus()
    }else{

       
        erroruser.style.color="green";
        this.style.border="2px solid green"

        erroruser.innerHTML="valid user-name"
        erroruser.style.display="block";
        subuser="true"
        
    }
})



// =================================================================
// email regex
email.addEventListener("blur",function(){
    this.style.border="2px solid red"


    var emailreg=/^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,6}$/
    var emailvalid=emailreg.test(this.value)

    if(!emailvalid){
        erroremail.style.display="block";
        erroremail.style.color="red";

        erroremail.innerHTML="email should be like abc12@someth.com"
        this.focus()
    }else{

       
        erroremail.style.color="green";
        this.style.border="2px solid green"

        erroremail.innerHTML="valid email"
        erroremail.style.display="block";
        subemail="true"
    }
})

// =================================================================
// phone regex
// phone.addEventListener("blur",function(){
//     this.style.border="2px solid red"


//     var phonereg=/^(010|011|012|015)\d{8}$/
//     var phonevalid=phonereg.test(this.value)

//     if(!phonevalid){
//         errorphone.style.display="block";
//         errorphone.style.color="red";

//         errorphone.innerHTML="phone should start with 01 and be 11 char"
//         this.focus()
//     }else{

       
//         errorphone.style.color="green";
//         this.style.border="2px solid green"

//         errorphone.innerHTML="valid number"
//         errorphone.style.display="block";
//         subphone="true"
//     }
// })

// =================================================================
// pass1 regex

function passcheck(e){
    e.target.style.border="2px solid red"
    var pass1reg=/[a-zA-Z0-9._-]{5,20}/
    var pass1valid=pass1reg.test(e.target.value)

    if(!pass1valid){
        errorpass1.style.display="block";
        errorpass1.style.color="red";

        errorpass1.innerHTML="password should be between 5 and 20"
        this.focus()
    }else{

       
        errorpass1.style.color="green";
        this.style.border="2px solid green"

        errorpass1.innerHTML="valid password"
        errorpass1.style.display="block";
        subpass1="true"
    }

}
// ==========================================================

pass1.addEventListener("blur",function(){
    this.style.border="2px solid red"


    var pass1reg=/[a-zA-Z0-9._-]{5,20}/
    var pass1valid=pass1reg.test(this.value)

    if(!pass1valid){
        errorpass1.style.display="block";
        errorpass1.style.color="red";

        errorpass1.innerHTML="password should be between 5 and 20"
        this.focus()
    }else{

       
        errorpass1.style.color="green";
        this.style.border="2px solid green"

        errorpass1.innerHTML="valid password"
        errorpass1.style.display="block";
        subpass1="true"
    }
})
// =================================================================
// confirm pass 
pass2.addEventListener("blur",function(){
    this.style.border="2px solid red"


   

    if(pass1.value != pass2.value || pass2.value.length == 0){
        errorpass2.style.display="block";
        errorpass2.style.color="red";

        errorpass2.innerHTML="password is not identical"
        // this.focus()
    }else{

       
        errorpass2.style.color="green";
        this.style.border="2px solid green"

        errorpass2.innerHTML="confirmed password"
        errorpass2.style.display="block";
        subpass2="true"
    }
})
// =================================================================
// validate for file input
var fileInput=document.getElementById("file")
var errfile=document.getElementById("fileerr")
var filesel=false
fileInput.addEventListener("change",function(){

    if(fileInput.value == ""){
    errfile.style.display="block";
    errfile.style.color="red";
    errfile.innerHTML="you must select a profile pic. "
    }else{
    errfile.style.color="green"
    errfile.innerHTML="selected"
    errfile.style.display="block"
    filesel=true
    }

})













// ================================================================
// var check1="false"
// window.addEventListener("load",function(){

// if(radio1.checked != "true" && radio2.checked != "true" && radio3.checked != "true"){
//     errorgender.style.display="block"
//     errorgender.style.color="red"
//     errorgender.innerHTML="please select gender"

// }else{
//     errorgender.style.display="none"
//     check1="true"
// }


// })

// ================================================================
var errorsubmit=document.getElementById("submiterror")
// submit btn





submitbtn1.addEventListener("click",function(e){
    if(subname == "false" || filesel == false || subuser == "false" || subuser10 == "false" || subemail == "false" || subpass1 == "false" || subpass2 == "false"){
        
        errorsubmit.style.display="block"
        errorsubmit.style.color="red"
        errorsubmit.innerHTML="please fill the required input"

        // errorgender.style.display="block"
        // errorgender.style.color="red"

        if(filesel == false){
            errfile.style.display="block";
            errfile.style.color="red";
            errfile.innerHTML="you must select a profile pic. "

        }

        e.preventDefault()
       
        

    }



})