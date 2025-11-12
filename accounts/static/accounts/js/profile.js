// Hover efect 3D Saved
const savedCards = document.querySelectorAll(".saved-card");
savedCards.forEach((card, i) => {
  card.style.zIndex = i;
  card.addEventListener("mouseenter", () => {
    card.style.transform = "rotateY(0deg) scale(1.05)";
  });
  card.addEventListener("mouseleave", () => {
    card.style.transform = "rotateY(25deg)";
  });
});

// Click pe imagine -> deschidere în modal
const albums = document.querySelectorAll(".album img");
const modal = document.getElementById("image-modal");
const modalImg = document.getElementById("modal-img");
const closeModal = document.querySelector(".close");

albums.forEach((img) => {
  img.addEventListener("click", () => {
    modal.style.display = "flex";
    modalImg.src = img.src;
  });
});

closeModal.addEventListener("click", () => {
  modal.style.display = "none";
});

window.addEventListener("click", (e) => {
  if (e.target === modal) modal.style.display = "none";
});
