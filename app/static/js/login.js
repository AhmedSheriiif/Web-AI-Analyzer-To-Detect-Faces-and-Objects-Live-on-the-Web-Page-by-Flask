// form
// var email;
// var uname;
// var pass;

$(window).on('hashchange', function () {
    if (location.hash.slice(1) == 'signup') {
      $('.page').addClass('extend');
      $('#login').removeClass('active');
      $('#signup').addClass('active');
    } else {
      $('.page').removeClass('extend');
      $('#login').addClass('active');
      $('#signup').removeClass('active');
    }
  });
  $(window).trigger('hashchange');
  
  function validateLoginForm() {
    var name1 = document.getElementById('logName').value;
    var password1 = document.getElementById('logPassword').value;
    if (name1 == '' || password1 == '') {
      document.getElementById('errorMsg').innerHTML = alert(
        'Please fill the required fields'
      );
    } else if (password1.length < 3) {
      document.getElementById('errorMsg').innerHTML = alert(
        'Your password must include atleast 8 characters'
      );
    } else {
      for (var i = 0; i < dataForm.length; i++) {
        if (
          dataForm[i].signNam == name1 &&
          dataForm[i].signPasswor == password1
        ) {
          window.open('index.html');
        } else {
          document.getElementById('errorMsg').innerHTML = 'data is not found';
        }
      }
    }
  }
  
  var dataForm = [];
  if (localStorage.userName != null) {
    dataForm = JSON.parse(localStorage.userName);
  } else {
    dataForm = [];
  }
  
  function validateSignupForm() {
    let signEmail = document.getElementById('signEmail');
    let signName = document.getElementById('signName');
    let signPassword = document.getElementById('signPassword');
    let newUser = {};
  
    if (
      signEmail.value == '' ||
      signName.value == '' ||
      signPassword.value == ''
    ) {
      document.getElementById('errorMsg').innerHTML = alert(
        'Please fill the required fields'
      );
    } else if (signPassword.value.length < 8) {
      document.getElementById('errorMsg').innerHTML = alert(
        'Your password must include atleast 8 characters'
      );
    } else {
      newUser = {
        signEmai: signEmail.value,
        signNam: signName.value,
        signPasswor: signPassword.value,
      };
      dataForm.push(newUser);
      localStorage.setItem('userName', JSON.stringify(dataForm));
      alert('Successfully signed up');
    }
  }
  
  /* function validateLoginForm() {
    var name = document.getElementById('logName').value;
    var password = document.getElementById('logPassword').value;
    var a = localStorage.getItem('name');
    var b = localStorage.getItem('password');
    if (name == '' || password == '') {
      document.getElementById('errorMsg').innerHTML = alert(
        'Please fill the required fields'
      );
    } else if (password.length < 8) {
      document.getElementById('errorMsg').innerHTML = alert(
        'Your password must include atleast 8 characters'
      );
    } else if (name == a && password == b) {
      window.open('index.html');
    } else {
      alert('data is not found');
    }
  }
   */
  
  /* function validateSignupForm() {
    var dataForm = [];
    var newUser = {
      mail: signEmail.value,
      name: signName.value,
      password: signPassword.value,
    };
    dataForm.push(newUser);
    let mail = document.getElementById('signEmail').value;
    let name = document.getElementById('signName').value;
    let password = document.getElementById('signPassword').value;
  
    if (mail == '' || name == '' || password == '') {
      document.getElementById('errorMsg').innerHTML = alert(
        'Please fill the required fields'
      );
    } else if (password.length < 8) {
      document.getElementById('errorMsg').innerHTML = alert(
        'Your password must include atleast 8 characters'
      );
    } else {
      alert('Successfully signed up');
      email = localStorage.setItem('mail', mail);
      uname = localStorage.setItem('name', name);
      pass = localStorage.setItem('password', password);
    }
    console.log(newUser);
  } */