let burger = document.getElementById("burger")
let menu = document.getElementById("mobile_menu")
burger.addEventListener("click", function(){
	if(menu.style.display === "none"){
		menu.style.display = "flex";
	}
	else {
		menu.style.display = "none";
	}
});
	
