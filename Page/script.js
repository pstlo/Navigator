// Navigator page functions


// Spaceship animation
var bouncingIcon = document.getElementById("bouncingIcon");
var posX = 0;
var posX = window.innerWidth / 2;
var posY = window.innerHeight/2;
var dirX = Math.random() * 2 - 1;
var dirY = Math.random() * 2 - 1;
var speed = 2;

bouncingIcon.style.transform = "rotate(-90deg)";

function moveImage() {
	posX += dirX * speed;
	posY += dirY * speed;
	bouncingIcon.style.left = posX + "px";
	bouncingIcon.style.top = posY + "px";

	var angle = Math.atan2(dirY, dirX) * 180 / Math.PI;
	bouncingIcon.style.transform = "rotate(" + (angle +90) + "deg)";

	if (posX < 0) {
		posX = 0;
		dirX *= -1;
	}

	if (50 +posX > window.innerWidth) {
		posX = window.innerWidth-50;
		dirX *= -1;
	}

	if (posY < 0) {
		posY = 0;
		dirY *= -1;
	}

	if (50 + posY > window.innerHeight) {
		posY = window.innerHeight-50;
		dirY *= -1;
	}

}


// Meteor shower animation
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

  const parentContainer = document.createElement('div');
  parentContainer.style.position = 'fixed';
  parentContainer.style.width = '100%';
  parentContainer.style.height = '100%';
  document.body.appendChild(parentContainer);

  const icons = [];
  for (let i = 0; i < numIcons; i++) {
    const diagIcon = document.createElement('img');
    let dPosX = window.innerWidth;
    let dPosY = window.innerHeight*0.25+0.25;
    let dDirX = Math.random() * -1;
    let dDirY = Math.random()/2;
    let dSpeed = Math.random() * 5 + 2;
	let dSize = 100/dSpeed;

	diagIcon.src = selectRandomImage();
    diagIcon.style.position = 'absolute';

	diagIcon.style.height = dSize+'px';
	diagIcon.style.width = dSize+'px';


    parentContainer.appendChild(diagIcon);

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

			if (icon.posX < 0 || icon.posY > window.innerHeight) {
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
moveDiag(30);