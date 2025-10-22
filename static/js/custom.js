// tiny helper to emulate route navigation
function go(path) {
    // placeholder: in a real site you'd use router or server routes
    if (path.startsWith('/')) {
        window.location.href = path;
    }
}

// Handle "Get Started" logic
function getStarted() {
    const isAuth = false; // change this dynamically when backend ready
    if (isAuth) {
        go('/patient');
    } else {
        go('/register');
    }
}

// Mobile menu toggle
const burger = document.getElementById('burger');
const navLinks = document.getElementById('navLinks');

function toggleMenu() {
    navLinks.classList.toggle('show');
}

// Navbar shrink on scroll
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

// Reveal on scroll animation
const reveals = document.querySelectorAll('.reveal');

function revealOnScroll() {
    reveals.forEach(r => {
        const top = r.getBoundingClientRect().top;
        if (top < window.innerHeight - 80) {
            r.classList.add('show');
        }
    });
}

// Attach event listener and trigger on load
window.addEventListener('scroll', revealOnScroll);
document.addEventListener('DOMContentLoaded', revealOnScroll);
