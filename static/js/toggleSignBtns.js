const minWidth = 600;

var signin = document.querySelector('.signin-block');
var signup = document.querySelector('.signup-block');
var sign = document.querySelector('.sign-block');

var stdClassSign = sign.className;
var stdClassIn = signin.className;
var stdClassUp = signup.className;

sign.style.left = document.documentElement.clientWidth + 'px';
sign.style.width = document.documentElement.clientWidth + 'px';
sign.style.height = document.documentElement.clientHeight + 'px';

window.addEventListener('scroll', function(){
    sign.style.top = window.pageYOffset + 'px';
});

window.addEventListener('resize', function(){
    sign.style.height = document.documentElement.clientHeight + 'px';
    if (sign.className.includes('sign-open-full')){
        sign.style.left = 0 + 'px';
        sign.style.width = document.documentElement.clientWidth + 'px';
    }else if (sign.className.includes('sign-open')){
        sign.style.left = document.documentElement.clientWidth / 2 + 'px';
        sign.style.width = document.documentElement.clientWidth / 2 + 'px';
    }else{
        sign.style.left = document.documentElement.clientWidth + 'px';
    }

    if (document.documentElement.clientWidth <= minWidth && sign.className.includes('sign-open')) {
        sign.className = stdClassSign + ' sign-open-full';
        sign.style.left = 0 + 'px';
        sign.style.width = document.documentElement.clientWidth + 'px';
    }else if (document.documentElement.clientWidth > minWidth && sign.className.includes('sign-open-full')) {
        sign.className = stdClassSign + ' sign-open';
        sign.style.left = document.documentElement.clientWidth / 2 + 'px';
        sign.style.width = document.documentElement.clientWidth / 2 + 'px';
    }
});

function toggleForm(type){
    if (type === 'auth'){
        toggleTypeForm(signin, stdClassIn, signup, stdClassUp);
    }else if (type === 'reg'){
        toggleTypeForm(signup, stdClassUp, signin, stdClassIn);
    }
}

function openForm(type){
    sign.style.transition = 'left 0s';
    if (type === 'auth'){
        toggleTypeForm(signin, stdClassIn, signup, stdClassUp);
    }else if (type === 'reg'){
        toggleTypeForm(signup, stdClassUp, signin, stdClassIn);
    }
    sign.style.transition = 'left 1s';
}

function toggleTypeForm(elOpen, classOpen, elClose, classClose){
    if (sign.className.includes('sign-open')){
        if (elOpen.className.includes('d-none')){
            elOpen.className = classOpen;
            elClose.className = classClose + ' d-none';
        }else{
            elOpen.className = classOpen + ' d-none';
            elClose.className = classClose + ' d-none';
            sign.className = stdClassSign;
            sign.style.left = document.documentElement.clientWidth + 'px';
        }
    }else{
        if (document.documentElement.clientWidth <= minWidth) {
            sign.className = stdClassSign + ' sign-open-full';
            sign.style.width = document.documentElement.clientWidth + 'px';
            sign.style.left = 0 + 'px';
        }else {
            sign.className = stdClassSign + ' sign-open';
            sign.style.left = document.documentElement.clientWidth / 2 + 'px';
            sign.style.width = document.documentElement.clientWidth / 2 + 'px';
        }
        elOpen.className = classOpen;
        elClose.className = classClose + ' d-none';
    }
}

