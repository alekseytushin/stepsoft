var imagesLeft = document.querySelectorAll('.img-content-left');
var imagesRight = document.querySelectorAll('.img-content-right');

var rectLeft = [];
var rectRight = [];

imagesRight.forEach(el => rectRight.push(el.getBoundingClientRect()));
imagesLeft.forEach(el => rectLeft.push(el.getBoundingClientRect()));

window.addEventListener('scroll', function(){
    for (var i = 0; i < imagesLeft.length; i++) {
        if (document.documentElement.clientHeight * 6 / 7 >= (rectRight[i].y - window.pageYOffset)) {
            imagesRight[i].className = 'img-content-right img-transform-right';
        }
    }
});

window.addEventListener('scroll', function(){
    for (var i = 0; i < imagesLeft.length; i++) {
        if (document.documentElement.clientHeight * 6 / 7 >= (rectLeft[i].y - window.pageYOffset)) {
            imagesLeft[i].className = 'img-content-left img-transform-left';
        }
    }
});