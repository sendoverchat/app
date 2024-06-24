document.getElementById("openNav").addEventListener("click", () => {
    if(document.querySelector(".div-burger-menu-container").style.display == "none"){
        document.querySelector(".div-burger-menu-container").style.display = "flex";
    }else{
        document.querySelector(".div-burger-menu-container").style.display = "none";
    } 
});