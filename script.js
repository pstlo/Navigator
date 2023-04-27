// Navigator page backend

// Switch between pages
function switchPage(page) {
    var homePage = document.getElementById("home");
    var downloadsPage = document.getElementById("downloads");
    var supportPage = document.getElementById("support");

    if (page === "home") {
        homePage.style.display = "block";
        downloadsPage.style.display = "none";
        supportPage.style.display = "none";
    } else if (page === "downloads") {
        homePage.style.display = "none";
        downloadsPage.style.display = "block";
        supportPage.style.display = "none";
    } else if (page === "support") {
        homePage.style.display = "none";
        downloadsPage.style.display = "none";
        supportPage.style.display = "block";
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