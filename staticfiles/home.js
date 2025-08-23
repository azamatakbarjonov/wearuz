const menuToggle = document.getElementById('menu-toggle');
const navMenu = document.getElementById('nav-menu');
const header = document.getElementById('header');
const cards = document.querySelectorAll('.card');

let lastScrollY = 0;

menuToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});

window.addEventListener('scroll', () => {
    if (window.scrollY > lastScrollY && window.scrollY > 50) {
        header.classList.add('hidden');
    } else {
        header.classList.remove('hidden');
    }
    lastScrollY = window.scrollY;

    cards.forEach(card => {
        const cardTop = card.getBoundingClientRect().top;
        if (cardTop < window.innerHeight - 100) {
            card.classList.add('show');
        }
    });
});

const trendContainer = document.getElementById('trend-container');
let scrollStep = trendContainer.querySelector('.trend-item').offsetWidth + 20;
let scrollPos = 0;

setInterval(() => {
    scrollPos += scrollStep;

    if (scrollPos >= trendContainer.scrollWidth - trendContainer.clientWidth) {
        scrollPos = 0;
    }

    trendContainer.scrollTo({
        left: scrollPos,
        behavior: 'smooth'
    });
}, 2000);

const trendItems = document.querySelectorAll('.trend-item');

window.addEventListener('scroll', () => {
    trendItems.forEach(item => {
        const top = item.getBoundingClientRect().top;
        if (top < window.innerHeight - 50) {
            item.classList.add('show');
        }
    });
});
