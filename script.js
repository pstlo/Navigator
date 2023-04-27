// Navigator page backend

// Toggle between pages
function switchPage() {
	var currentPage = document.getElementById("home")
	var downloadsPage = document.getElementById("downloads")
	if (currentPage.style.display === "none")
	{
		currentPage.style.display = "block";
		downloadsPage.style.display = "none";
	}
	else
	{
		currentPage.style.display = "none";
		downloadsPage.style.display = "block";
	}
}

// Animate
var img = document.getElementById("img");
var x = 0;
var direction = 1;
var speed = 5;

function moveImage() {
	x += direction * speed;
	img.style.left = x + "px";

	if (x >= window.innerWidth/2 || x <= window.innerWidth/-2) {
		direction *= -1;
	}
}

setInterval(moveImage, 10);