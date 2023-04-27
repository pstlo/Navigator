function switchPage() {
	var currentPage = document.getElementById("home")
	var downloadsPage = document.getElementById("downloads")
	if (currentPage.style.display === "none") {
		currentPage.style.display = "block";
		downloadsPage.style.display = "none";
	}
	else {
		currentPage.style.display = "none";
		downloadsPage.style.display = "block";
	}
}