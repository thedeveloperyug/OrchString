(() => {
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const progress = document.getElementById('progress');
  const menu = document.querySelector('.menu-toggle');
  const navigation = document.getElementById('main-nav');

  if (menu && navigation) {
    const closeMenu = () => {
      navigation.classList.remove('open');
      menu.setAttribute('aria-expanded', 'false');
    };
    menu.addEventListener('click', () => {
      const open = navigation.classList.toggle('open');
      menu.setAttribute('aria-expanded', String(open));
    });
    navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') closeMenu();
    });
  }

  const reveals = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        reveals.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(element => reveals.observe(element));

  let scrollFrame = 0;
  const updateProgress = () => {
    scrollFrame = 0;
    if (progress) {
      const height = Math.max(1, document.documentElement.scrollHeight - innerHeight);
      progress.style.width = Math.min(100, scrollY / height * 100) + '%';
    }
  };
  addEventListener('scroll', () => {
    if (!scrollFrame) scrollFrame = requestAnimationFrame(updateProgress);
  }, { passive: true });
  updateProgress();

  document.querySelectorAll('.tilt-card,.person-card').forEach(card => {
    card.addEventListener('pointermove', event => {
      if (motion.matches || innerWidth < 900) return;
      const rect = card.getBoundingClientRect();
      const x = ((event.clientY - rect.top) / rect.height - 0.5) * -5;
      const y = ((event.clientX - rect.left) / rect.width - 0.5) * 7;
      card.style.transform = 'perspective(900px) rotateX(' + x + 'deg) rotateY(' + y + 'deg) translateY(-5px)';
    }, { passive: true });
    card.addEventListener('pointerleave', () => { card.style.transform = ''; });
  });

  const scene = document.querySelector('.neural-scene');
  if (!scene) return;

  const svg = scene.querySelector('.neural-network');
  const linksGroup = svg.querySelector('.neural-links');
  const nodesGroup = svg.querySelector('.neural-nodes');
  const signalsGroup = svg.querySelector('.neural-signals');
  const namespace = 'http://www.w3.org/2000/svg';
  const makeElement = (tag, parent) => {
    const element = document.createElementNS(namespace, tag);
    parent.appendChild(element);
    return element;
  };

  const phones = matchMedia('(max-width: 767px), (max-width: 980px) and (max-height: 500px) and (pointer: coarse)');
  const center = { x: 320, y: 300 };
  const nodes = Array.from(nodesGroup.querySelectorAll('.connector-node'), (element, index) => ({
    element,
    x: Number(element.dataset.x),
    y: Number(element.dataset.y),
    tailX: Number(element.dataset.tailX),
    tailY: Number(element.dataset.tailY),
    link: linksGroup.querySelector('[data-link="' + index + '"]'),
    trail: svg.querySelector('[data-trail="' + index + '"]')
  }));

  // Each illustrated business connector has an independent open strand.
  // Soft cubic curves carry every signal inward to the same console hub.
  const signals = nodes.flatMap((node, index) => Array.from({ length: 2 }, (_, pulse) => {
    const halo = makeElement('circle', signalsGroup);
    const dot = makeElement('circle', signalsGroup);
    halo.setAttribute('class', 'neural-signal-halo');
    halo.setAttribute('r', '7');
    dot.setAttribute('class', 'neural-signal-dot');
    dot.setAttribute('r', '2.7');
    return { node, offset: index * 0.173 + pulse * 0.5, halo, dot };
  }));
  const coordinate = point => point.x.toFixed(2) + ',' + point.y.toFixed(2);
  const draw = time => {
    nodes.forEach((node, index) => {
      const wave = Math.sin(time * 0.8 + index * 1.4);
      node.point = {
        x: node.x + Math.sin(time * 0.65 + index * 1.7) * 7,
        y: node.y + Math.cos(time * 0.72 + index * 1.3) * 8
      };
      const dx = center.x - node.point.x;
      const dy = center.y - node.point.y;
      node.control1 = {
        x: node.point.x + dx * 0.38 + wave * 19,
        y: node.point.y + dy * 0.2 + Math.cos(time * 0.7 + index) * 23
      };
      node.control2 = {
        x: node.point.x + dx * 0.72 - wave * 17,
        y: node.point.y + dy * 0.83 - Math.cos(time * 0.75 + index) * 16
      };
      node.element.setAttribute('transform', 'translate(' + coordinate(node.point) + ')');
      node.link.setAttribute('d', 'M' + coordinate(node.point) + ' C' +
        coordinate(node.control1) + ' ' + coordinate(node.control2) + ' ' + coordinate(center));
      node.trail.setAttribute('d', 'M' + node.tailX + ',' + node.tailY + ' C' +
        (node.tailX + (node.point.x - node.tailX) * 0.4).toFixed(2) + ',' + (node.tailY + wave * 22).toFixed(2) +
        ' ' + (node.point.x + wave * 24).toFixed(2) + ',' + (node.point.y - 18).toFixed(2) +
        ' ' + coordinate(node.point));
    });

    signals.forEach(signal => {
      const phase = (time * 0.16 + signal.offset) % 1;
      const inverse = 1 - phase;
      const { point, control1, control2 } = signal.node;
      const x = inverse ** 3 * point.x + 3 * inverse ** 2 * phase * control1.x +
        3 * inverse * phase ** 2 * control2.x + phase ** 3 * center.x;
      const y = inverse ** 3 * point.y + 3 * inverse ** 2 * phase * control1.y +
        3 * inverse * phase ** 2 * control2.y + phase ** 3 * center.y;
      const opacity = Math.min(1, phase * 5) * Math.min(1, (1 - phase) * 5);
      [signal.halo, signal.dot].forEach(element => {
        element.setAttribute('cx', x.toFixed(2));
        element.setAttribute('cy', y.toFixed(2));
        element.setAttribute('opacity', opacity.toFixed(2));
      });
    });
  };

  let visible = false;
  let frame = 0;
  let lastTime = 0;
  let elapsed = 0;
  const animate = timestamp => {
    frame = 0;
    if (timestamp - lastTime >= 1000 / 30) {
      elapsed += lastTime ? Math.min(timestamp - lastTime, 64) / 1000 : 0;
      lastTime = timestamp;
      draw(elapsed);
    }
    frame = requestAnimationFrame(animate);
  };
  const updateAnimation = () => {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    lastTime = 0;
    if (phones.matches) {
      return;
    } else if (motion.matches) {
      draw(0);
    } else if (visible && !document.hidden) {
      frame = requestAnimationFrame(animate);
    }
  };
  draw(0);
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    updateAnimation();
  }, { threshold: 0 }).observe(scene);
  document.addEventListener('visibilitychange', updateAnimation);
  motion.addEventListener('change', updateAnimation);
  phones.addEventListener('change', updateAnimation);
})();
