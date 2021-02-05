// form validation checks is passwords match
// in the future it is possible to make more complex validation
// but for now there is no reason


let password1 = document.getElementById('password1');
let password2 = document.getElementById('password2');
let error = document.getElementById('error');
let form = document.getElementById('form');

form.addEventListener('submit', (e) => {
    let errors = [];
    if (password1.value !== password2.value) {
        errors.push("passwords do not match!");
        password2.style.color = 'rgb(247, 67, 67)'
        password1.style.color = 'rgb(247, 67, 67)'
    }
    if (errors.length > 0) {
        e.preventDefault();
        error.innerHTML = errors.join(',');
    }
});