document.querySelectorAll('.cta-btn, .cta-outline').forEach(btn => {
    btn.addEventListener('click', function () {
        showToast('Funcția nu este activă în demo.');
    });
});

function showToast(msg) {
    let toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('toast-hide');
        toast.addEventListener('transitionend', () => toast.remove());
    }, 1500);
}

document.querySelectorAll('.main-nav a, .footer-links a').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        link.classList.add('nav-active');
        setTimeout(() => link.classList.remove('nav-active'), 500);
    });
});

document.querySelectorAll('.hero-gallery img').forEach(img => {
    img.addEventListener('mouseenter', () => img.classList.add('img-hover'));
    img.addEventListener('mouseleave', () => img.classList.remove('img-hover'));
});

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('section-visible');
        }
    });
}, { threshold: 0.15 });

document.querySelectorAll('section').forEach(section => observer.observe(section));

const sections = document.querySelectorAll('section');
let isScrolling = false;
let currentIndex = 0;

function scrollToSection(index) {
    if (index < 0 || index >= sections.length) return;
    isScrolling = true;
    sections[index].scrollIntoView({ behavior: 'smooth' });
    currentIndex = index;
    setTimeout(() => { isScrolling = false; }, 700);
}

window.addEventListener('wheel', (e) => {
    if (isScrolling) return;
    if (e.deltaY > 0) {
        scrollToSection(currentIndex + 1);
    } else {
        scrollToSection(currentIndex - 1);
    }
});

let touchStartY = 0;
window.addEventListener('touchstart', (e) => {
    touchStartY = e.touches[0].clientY;
});

window.addEventListener('touchend', (e) => {
    const touchEndY = e.changedTouches[0].clientY;
    if (isScrolling) return;
    if (touchStartY - touchEndY > 50) scrollToSection(currentIndex + 1);
    if (touchEndY - touchStartY > 50) scrollToSection(currentIndex - 1);
});
