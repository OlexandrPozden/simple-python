function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};

token = getCookie('token');

let navBar = document.getElementById('nav');

let firstElement = document.createElement('li');
let secondElement = document.createElement('li');
firstElement.style="float:right";
secondElement.style="float:right";
if(token!=""){
  console.log(token);
  payload = parseJwt(token);
  console.log(payload);

  var username = payload.username;
  if (username!=""){
    let userProfile = document.createElement('a');
    userProfile.href = "/user/"+username;
    userProfile.innerHTML = username;
    userProfile.style = "color:#B2EB1C";
    firstElement.appendChild(userProfile);
    let logOut = document.createElement('a');
    logOut.href = "/logout";
    logOut.innerHTML = "log out";
    secondElement.appendChild(logOut);   
  }
}
else{
  let loginOption = document.createElement('a');
  loginOption.href = "/login";
  loginOption.innerHTML = "log in";
  let signupOption = document.createElement('a');
  signupOption.innerHTML = "sign up";
  signupOption.href = "/signup";
  firstElement.appendChild(loginOption);
  secondElement.appendChild(signupOption);
}

navBar.appendChild(secondElement);
navBar.appendChild(firstElement);

