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

// Fechas / agenda
// Agregá una fecha por entrada. "date" en formato YYYY-MM-DD (si el día
// todavía no está confirmado, usá el 01 del mes y agregá day: 'TBA').
// "url" es opcional (link a entradas, evento de Instagram, etc).
const DATES = [
  { date: '2026-03-21', event: 'Warmup Fernando Ferreyra', venue: 'Rosario, Argentina' },
  { date: '2026-06-13', event: 'Warmup Agustín Ficarra', venue: 'Rosario, Argentina' },
  { date: '2026-07-30', event: 'Open to clase FEUR', venue: 'Rosario, Argentina' },
  { date: '2026-09-04', event: 'Closing Fashion Sunset', venue: 'Rosario, Argentina' },
  { date: '2026-09-26', event: 'Open a Marcelo Vasami', venue: 'Rosario, Argentina' },
  { date: '2026-10-01', day: 'TBA', event: 'Sunset', venue: 'A confirmar' },
  { date: '2026-11-01', day: 'TBA', event: 'Victoria', venue: 'A confirmar' },
];

const MONTHS_ES = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'];

function renderDates() {
  const list = document.getElementById('datesList');
  const empty = document.getElementById('datesEmpty');
  if (!list) return;

  if (DATES.length === 0) {
    empty.hidden = false;
    return;
  }

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Para fechas con día "TBA" comparamos contra el último día del mes,
  // así se mantienen como próximas durante todo el mes en curso.
  const compareDate = (d) => {
    const base = new Date(d.date + 'T00:00:00');
    if (d.day) return new Date(base.getFullYear(), base.getMonth() + 1, 0);
    return base;
  };

  const sorted = [...DATES].sort((a, b) => compareDate(a) - compareDate(b));
  const firstUpcomingIndex = sorted.findIndex(d => compareDate(d) >= today);

  list.innerHTML = sorted.map((d, i) => {
    const dateObj = new Date(d.date + 'T00:00:00');
    const isPast = compareDate(d) < today;
    const isNext = i === firstUpcomingIndex;
    const day = d.day || dateObj.getDate();
    const month = MONTHS_ES[dateObj.getMonth()];

    const inner = `
      <span class="date-date">${day} ${month}</span>
      <span class="date-info">
        <span class="date-event">${d.event}</span>
        <span class="date-venue">${d.venue}</span>
      </span>
      ${isNext ? '<span class="date-badge">Próxima fecha</span>' : ''}
    `;

    const classes = ['date-item', isPast ? 'is-past' : '', isNext ? 'is-next' : ''].filter(Boolean).join(' ');

    return d.url
      ? `<li class="${classes}"><a href="${d.url}" target="_blank" rel="noopener">${inner}</a></li>`
      : `<li class="${classes}">${inner}</li>`;
  }).join('');
}
renderDates();

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
