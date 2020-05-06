var ide = document.querySelector('.ide');
var innerIde = document.getElementById('inner-ide');
var main = document.getElementById('main');
var stdClass = ide.className;

ide.style.left = document.documentElement.clientWidth + 'px';
ide.style.width = document.documentElement.clientWidth / 2 + 'px';
ide.style.height = document.documentElement.clientHeight + 'px';
innerIde.style.height = document.documentElement.clientHeight - 100 + 'px';

window.addEventListener('scroll', function(){
    ide.style.top = window.pageYOffset + 'px';
});

window.addEventListener('resize', function(){
    ide.style.height = document.documentElement.clientHeight + 'px';
    ide.style.width = document.documentElement.clientWidth / 2 + 'px';
    innerIde.style.height = document.documentElement.clientHeight - 100 + 'px';
    if (ide.className.includes('ide-open')) {
        ide.style.left = document.documentElement.clientWidth / 2 + 'px';
        main.style.maxHeight = document.documentElement.clientHeight - 86 + 'px';
        //main.style.width = document.documentElement.clientWidth / 2 + 'px';
    }else{
        ide.style.left = document.documentElement.clientWidth + 'px';
    }
});

function openIDE(){
    ide.style.transition = 'left 0s';
    toggleMainIDE();
    ide.style.transition = 'left 0.5s';
}

function toggleMainIDE(){
    var offset = 0
    if (ide.className.includes('ide-open')) {
        offset = main.scrollTop;
        document.documentElement.style.overflowY = 'visible';
        ide.className = stdClass;
        ide.style.left = document.documentElement.clientWidth + 'px';
        main.style.width = '100%';
        main.style.maxHeight = 'none';
        main.style.overflow = 'hidden';
        window.scrollBy(0, offset);
    }else{
        offset = window.pageYOffset;
        window.scrollBy(0, -window.pageYOffset);
        document.documentElement.style.overflowY = 'hidden';
        ide.className = stdClass + ' ide-open';
        ide.style.left = document.documentElement.clientWidth / 2 + 'px';
        ide.style.height = document.documentElement.clientHeight + 'px';
        main.style.width = '50%';
        main.style.maxHeight = document.documentElement.clientHeight - 86 + 'px';
        main.style.overflow = 'auto';
        main.scrollTop = offset;
        //main.style.float = 'left';
        //main.style.width = document.documentElement.clientWidth / 2 + 'px';
    }
}