const themeToggle = document.querySelector("#theme-toggle");
const stroke = document.querySelectorAll(".stroke")
const svgItem = document.querySelectorAll(".svg-item")
const body = document.body;

// themeToggle.addEventListener('click', function(){
// if (themeToggle.getAttribute('src') == 'Assets/Light.svg') {
//   themeToggle.setAttribute('src','Assets/Dark.svg') 
//   body.classList.replace('light','dark');
// }
// else if (themeToggle.getAttribute('src') == 'Assets/Dark.svg'){
//   themeToggle.setAttribute('src','Assets/Light.svg')
//   body.classList.replace('dark','light');
// }
// })

function toggleTheme(){
  if (themeToggle.getAttribute('src') == 'Assets/Light.svg') {
    themeToggle.setAttribute('src','Assets/Dark.svg') 
    body.classList.replace('light','dark');
    darkObjs();
  }
  else if (themeToggle.getAttribute('src') == 'Assets/Dark.svg'){
    themeToggle.setAttribute('src','Assets/Light.svg')
    body.classList.replace('dark','light');
  }
  }

// addLayer = Document.querySelector('.add-layer');
// addStrFil = addLayer.getElementByID('#add-lay');
// addGlyph = addLayer.querySelector('#add-glyph');

// function darkObjs(){
// addStrFil.setAttribute('stroke', '#F6F9FF');
// addStrFil.setAttribute('fill', '#1B385A');
// addGlyph.setAttribute('fill', '#F6F9FF');
// }

// svgItem.addEventListener('click', function(){
//   stroke.setAttribute('stroke','white');
// })


  
 

