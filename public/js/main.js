// Header background on scroll
const header = document.getElementById('siteHeader');
const onScroll = () => {
  if (window.scrollY > 40) header.classList.add('scrolled');
  else header.classList.remove('scrolled');
};
window.addEventListener('scroll', onScroll);
onScroll();

// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const mainNav = document.getElementById('mainNav');
navToggle.addEventListener('click', () => {
  const isOpen = mainNav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', isOpen);
});
mainNav.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => mainNav.classList.remove('open'));
});

// YouTube facade: load iframe on click
document.querySelectorAll('.video-card').forEach(card => {
  const thumb = card.querySelector('.video-thumb');
  thumb.addEventListener('click', () => {
    const id = card.dataset.id;
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube.com/embed/${id}?autoplay=1`;
    iframe.title = 'YouTube video player';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;
    thumb.replaceWith(iframe);
  }, { once: true });
});

// Contact form -> mailto
const form = document.getElementById('contactForm');
form.addEventListener('submit', (e) => {
  e.preventDefault();
  const data = new FormData(form);
  const nombre = data.get('nombre');
  const email = data.get('email');
  const evento = data.get('evento');
  const mensaje = data.get('mensaje');

  const subject = encodeURIComponent(`Consulta desde la web — ${nombre}`);
  const body = encodeURIComponent(
    `Nombre: ${nombre}\nEmail: ${email}\nEvento / Fecha: ${evento}\n\nMensaje:\n${mensaje}`
  );
  window.location.href = `mailto:Jonatan.sc2726@gmail.com?subject=${subject}&body=${body}`;
});
