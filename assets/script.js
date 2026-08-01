(() => {
  document.documentElement.classList.add('js');

  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointerQuery = window.matchMedia('(pointer: fine)');
  const header = document.querySelector('.site-header');
  const menuButton = document.querySelector('.menu-toggle');
  const mobilePanel = document.querySelector('.mobile-panel');
  const navLinks = [...document.querySelectorAll('[data-nav-link]')];

  const setHeaderState = () => {
    header?.classList.toggle('is-scrolled', window.scrollY > 18);
  };

  const closeMenu = () => {
    if (!menuButton || !mobilePanel) return;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Otwórz menu');
    mobilePanel.hidden = true;
    document.body.style.overflow = '';
  };

  menuButton?.addEventListener('click', () => {
    const nextState = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(nextState));
    menuButton.setAttribute('aria-label', nextState ? 'Zamknij menu' : 'Otwórz menu');
    mobilePanel.hidden = !nextState;
    document.body.style.overflow = nextState ? 'hidden' : '';
    if (nextState) mobilePanel.querySelector('a')?.focus();
  });

  navLinks.forEach((link) => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeMenu();
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 820) closeMenu();
  });
  window.addEventListener('scroll', setHeaderState, { passive: true });
  setHeaderState();

  const sections = [...document.querySelectorAll('main section[id]')];
  if ('IntersectionObserver' in window) {
    const navigationObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navLinks.forEach((link) => {
          const active = link.getAttribute('href') === `#${entry.target.id}`;
          if (active) link.setAttribute('aria-current', 'page');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-35% 0px -55% 0px', threshold: 0 });
    sections.forEach((section) => navigationObserver.observe(section));
  }

  const revealElements = [...document.querySelectorAll('.reveal')];
  if (motionQuery.matches || !('IntersectionObserver' in window)) {
    revealElements.forEach((element) => element.classList.add('is-visible'));
  } else {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    revealElements.forEach((element) => revealObserver.observe(element));
  }

  const counters = [...document.querySelectorAll('[data-counter]')];
  const setCounterFinalValue = (element) => {
    const target = Number(element.dataset.counter || 0);
    const suffix = element.dataset.suffix || '';
    element.textContent = `${target}${suffix}`;
  };

  if (motionQuery.matches || !('IntersectionObserver' in window)) {
    counters.forEach(setCounterFinalValue);
  } else {
    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const element = entry.target;
        const target = Number(element.dataset.counter || 0);
        const suffix = element.dataset.suffix || '';
        const start = performance.now();
        const duration = 950;

        const tick = (now) => {
          const progress = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          element.textContent = `${Math.round(target * eased)}${suffix}`;
          if (progress < 1) requestAnimationFrame(tick);
        };

        requestAnimationFrame(tick);
        observer.unobserve(element);
      });
    }, { threshold: 0.6 });
    counters.forEach((counter) => counterObserver.observe(counter));
  }

  const heroVisual = document.querySelector('.hero-visual');
  const resetHeroPointer = () => {
    heroVisual?.style.setProperty('--pointer-x', '0px');
    heroVisual?.style.setProperty('--pointer-y', '0px');
  };

  if (heroVisual && !motionQuery.matches && finePointerQuery.matches) {
    heroVisual.addEventListener('pointermove', (event) => {
      const rect = heroVisual.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width - 0.5) * 14;
      const y = ((event.clientY - rect.top) / rect.height - 0.5) * 10;
      heroVisual.style.setProperty('--pointer-x', `${x.toFixed(2)}px`);
      heroVisual.style.setProperty('--pointer-y', `${y.toFixed(2)}px`);
    });
    heroVisual.addEventListener('pointerleave', resetHeroPointer);
  }

  const track = document.querySelector('.carousel-track');
  const carousel = document.querySelector('.carousel');
  const slides = [...document.querySelectorAll('.project-card')];
  const previousButton = document.querySelector('[data-carousel="prev"]');
  const nextButton = document.querySelector('[data-carousel="next"]');
  const dots = [...document.querySelectorAll('[data-slide]')];
  let currentSlide = 0;
  let autoPlayTimer;
  let pointerStartX = null;

  const showSlide = (index, focus = false) => {
    if (!track || slides.length === 0) return;
    currentSlide = (index + slides.length) % slides.length;
    track.style.transform = `translateX(-${currentSlide * 100}%)`;
    slides.forEach((slide, slideIndex) => {
      const isCurrent = slideIndex === currentSlide;
      slide.setAttribute('aria-hidden', String(!isCurrent));
      slide.tabIndex = isCurrent ? 0 : -1;
    });
    dots.forEach((dot, dotIndex) => {
      dot.setAttribute('aria-current', String(dotIndex === currentSlide));
    });
    if (focus) slides[currentSlide].focus({ preventScroll: true });
  };

  const stopAutoPlay = () => clearInterval(autoPlayTimer);
  const startAutoPlay = () => {
    stopAutoPlay();
    if (motionQuery.matches || document.hidden || slides.length < 2) return;
    autoPlayTimer = setInterval(() => showSlide(currentSlide + 1), 6500);
  };

  previousButton?.addEventListener('click', () => {
    showSlide(currentSlide - 1);
    startAutoPlay();
  });
  nextButton?.addEventListener('click', () => {
    showSlide(currentSlide + 1);
    startAutoPlay();
  });
  dots.forEach((dot) => dot.addEventListener('click', () => {
    showSlide(Number(dot.dataset.slide));
    startAutoPlay();
  }));

  carousel?.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      showSlide(currentSlide - 1, true);
      startAutoPlay();
    }
    if (event.key === 'ArrowRight') {
      event.preventDefault();
      showSlide(currentSlide + 1, true);
      startAutoPlay();
    }
  });
  carousel?.addEventListener('pointerdown', (event) => {
    pointerStartX = event.clientX;
    stopAutoPlay();
  });
  carousel?.addEventListener('pointerup', (event) => {
    if (pointerStartX === null) return;
    const distance = event.clientX - pointerStartX;
    if (Math.abs(distance) > 45) showSlide(currentSlide + (distance < 0 ? 1 : -1));
    pointerStartX = null;
    startAutoPlay();
  });
  carousel?.addEventListener('pointercancel', () => {
    pointerStartX = null;
    startAutoPlay();
  });
  carousel?.addEventListener('mouseenter', stopAutoPlay);
  carousel?.addEventListener('mouseleave', startAutoPlay);
  carousel?.addEventListener('focusin', stopAutoPlay);
  carousel?.addEventListener('focusout', startAutoPlay);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stopAutoPlay();
    else startAutoPlay();
  });

  showSlide(0);
  startAutoPlay();

  document.querySelectorAll('.faq-question').forEach((button) => {
    button.addEventListener('click', () => {
      const answerId = button.getAttribute('aria-controls');
      const answer = answerId ? document.getElementById(answerId) : null;
      const isOpen = button.getAttribute('aria-expanded') === 'true';

      document.querySelectorAll('.faq-question[aria-expanded="true"]').forEach((openButton) => {
        if (openButton === button) return;
        openButton.setAttribute('aria-expanded', 'false');
        const openAnswerId = openButton.getAttribute('aria-controls');
        const openAnswer = openAnswerId ? document.getElementById(openAnswerId) : null;
        if (openAnswer) openAnswer.hidden = true;
      });

      button.setAttribute('aria-expanded', String(!isOpen));
      if (answer) answer.hidden = isOpen;
    });
  });

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
