const themeToggle = document.querySelector("#theme-toggle");
const stroke = document.querySelectorAll(".stroke")
const svgItem = document.querySelectorAll(".svg-item")
const body = document.body;

themeToggle.addEventListener('click', function(){
if (themeToggle.getAttribute('src') == 'Assets/Light.svg') {
  themeToggle.setAttribute('src','Assets/Dark.svg') 
  body.classList.replace('light','dark');
}
else if (themeToggle.getAttribute('src') == 'Assets/Dark.svg'){
  themeToggle.setAttribute('src','Assets/Light.svg')
  body.classList.replace('dark','light');
}
})

svgItem.addEventListener('click', function(){
  stroke.setAttribute('stroke','white');
})



