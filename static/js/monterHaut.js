// Back to top button
const backToTopBtn = document.getElementById("backToTop");

window.addEventListener("scroll", () => {
  if (window.pageYOffset > 300) {
    backToTopBtn.classList.add("visible");
  } else {
    backToTopBtn.classList.remove("visible");
  }
});

document.getElementById("backToTop").addEventListener("click", function (e) {
  e.preventDefault(); // empêche le # de sauter brutalement
  window.scrollTo({
    top: 0,
    behavior: "smooth" // défilement en douceur
  });
});
