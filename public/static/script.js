function navDropdown() {
  var x = document.getElementById("nav");
  var home = document.getElementById("home");
  if (x.className === "navbar") {
    x.className += " responsive";
    home.className += " blur";
  } else {
    x.className = "navbar";
    home.className = "home";
  }
}
