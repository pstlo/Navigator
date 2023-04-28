// Navigator page backend

// Switch between pages
function switchPage(page) {
    var homePage = document.getElementById("home");
    var downloadsPage = document.getElementById("downloads");
    var supportPage = document.getElementById("support");

    if (page === "home") {
        homePage.style.display = "flex";
		homePage.style.flexDirection = "column";
        downloadsPage.style.display = "none";
        supportPage.style.display = "none";
    } else if (page === "downloads") {
        homePage.style.display = "none";
        downloadsPage.style.display = "flex";
		downloadsPage.style.display = "column";
        supportPage.style.display = "none";
    } else if (page === "support") {
        homePage.style.display = "none";
        downloadsPage.style.display = "none";
        supportPage.style.display = "flex";
		supportPage.style.flexDirection = "column";
    }
}

// Animate

var bouncingIcon = document.getElementById("bouncingIcon");
var posX = 0;
var posY = 0;
var dirX = Math.random() * 2 - 1;
var dirY = Math.random() * 2 - 1;
var speed = 5;

function moveImage() {
	posX += dirX * speed;
	posY += dirY * speed;
	bouncingIcon.style.left = posX + "px";
	bouncingIcon.style.top = posY + "px";

	if (posX + bouncingIcon.width/2 > window.innerWidth/2 || posX + bouncingIcon.width/2 <= window.innerWidth/-2) {dirX *= -1;}
	if (posY + (1.5*bouncingIcon.height) > window.innerHeight || posY + (1.5*bouncingIcon.height) < 0) {dirY *= -1;}
}


function moveDiag() {
  const images = [
    'Assets/Obstacles/Meteors/meteor.png',
    'Assets/Obstacles/Meteors/bluem.png',
	'Assets/Obstacles/Meteors/lightbm.png',
	'Assets/Obstacles/Meteors/redm.png',
	'Assets/Obstacles/Meteors/orangem.png',
	'Assets/Obstacles/Meteors/whitem.png'
  ];
  let imageIndex = 0;

  let dPosX = window.innerWidth;
  let dPosY = 0;
  let dDirX = -1;
  let dDirY = 1;
  const diagIcon = document.createElement('img');
  diagIcon.src = images[imageIndex];
  diagIcon.style.position = 'absolute';
  document.body.appendChild(diagIcon);

  function animate() {
    dPosX += dDirX * 5;
    dPosY += dDirY * 5;
    diagIcon.style.left = dPosX + "px";
    diagIcon.style.top = dPosY + "px";

    if (dPosX + diagIcon.width <= 0 || dPosY + diagIcon.height >= window.innerHeight) {
      dPosX = window.innerWidth;
      dPosY = 0;
      imageIndex = (imageIndex + 1) % images.length;
      diagIcon.src = images[imageIndex];
    }

    requestAnimationFrame(animate);
  }

  animate();
}

setInterval(moveImage, 5);
moveDiag();