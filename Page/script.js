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

/// Bounce animation
var bouncingIcon = document.getElementById("bouncingIcon");
var posX = 0;
var posY = 0;
var dirX = Math.random() * 2 - 1;
var dirY = Math.random() * 2 - 1;
var speed = 5;

// Set the image to face upright by default
bouncingIcon.style.transform = "rotate(-90deg)";

function moveImage() {
	posX += dirX * speed;
	posY += dirY * speed;
	bouncingIcon.style.left = posX + "px";
	bouncingIcon.style.top = posY + "px";

	// Calculate angle of rotation based on direction of movement
	var angle = Math.atan2(dirY, dirX) * 180 / Math.PI;
	bouncingIcon.style.transform = "rotate(" + (angle +90) + "deg)";

	// Bounce off walls
	if (posX + bouncingIcon.width/2 > window.innerWidth/2 || posX + bouncingIcon.width/2 <= window.innerWidth/-2) {dirX *= -1;}
	if (posY + (1.5*bouncingIcon.height) > window.innerHeight || posY + (1.5*bouncingIcon.height) < 0) {dirY *= -1;}
}

function moveDiag(numIcons) {
  const images = [
    'Assets/Obstacles/Meteors/bluem.png',
    'Assets/Obstacles/Meteors/lightbm.png',
    'Assets/Obstacles/Meteors/redm.png',
    'Assets/Obstacles/Meteors/orangem.png',
    'Assets/Obstacles/Meteors/whitem.png',
	'Assets/Obstacles/Meteors/yellowm.png',
	'Assets/Obstacles/Meteors/greenm.png',
	'Assets/Obstacles/Meteors/dgreenm.png',
  ];

	function selectRandomImage() {
		const randomNum = Math.random();
		if (randomNum < 0.9) {
			return 'Assets/Obstacles/Meteors/meteor.png';
		} 
		else {
			const index = Math.floor(Math.random() * (images.length - 1) + 1);
			return images[index];
		}
	}

  // Create a new parent container element
  const parentContainer = document.createElement('div');
  parentContainer.style.position = 'fixed';
  parentContainer.style.width = '100%';
  parentContainer.style.height = '100%';
  document.body.appendChild(parentContainer);

  const icons = [];
  for (let i = 0; i < numIcons; i++) {
    const diagIcon = document.createElement('img');
    diagIcon.src = selectRandomImage();
    diagIcon.style.position = 'absolute';
    parentContainer.appendChild(diagIcon);

    let dPosX = window.innerWidth;
    let dPosY = 0
    let dDirX = Math.random() * -1;
    let dDirY = Math.random()/2;
    let dSpeed = Math.random() * 5 + 5;

    icons.push({
      element: diagIcon,
      posX: dPosX,
      posY: dPosY,
      dirX: dDirX,
      dirY: dDirY,
      speed: dSpeed
    });
  }

	function animate() {
		icons.forEach(icon => {
			icon.posX += icon.dirX * icon.speed;
			icon.posY += icon.dirY * icon.speed;
			icon.element.style.left = icon.posX + "px";
			icon.element.style.top = icon.posY + "px";

			if (icon.posX < 0 || icon.posY > 1.5*window.innerHeight) {
				icon.posX = window.innerWidth;
				icon.posY = Math.random() * window.innerHeight;
				icon.element.src = selectRandomImage();
			}
		});
		requestAnimationFrame(animate);
	}
	animate();
}

setInterval(moveImage, 5);
moveDiag(20);