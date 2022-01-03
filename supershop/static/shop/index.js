let mouse_target = document.getElementById('logo');
let navbar = document.getElementById('navbar');

let show = false;

mouse_target.addEventListener('click', e => {

    show = !show;
    
    if(show){
        navbar.style.display = 'flex';
        console.log('visible');
    }
    else{
        navbar.style.display = 'none';
        console.log('hidden');
    }
});