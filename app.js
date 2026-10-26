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

  // A fixed spherical topology keeps every neuron connected while the entire
  // network softly deforms. No random layout changes or third-party libraries.
  const count = 100;
  const goldenAngle = Math.PI * (3 - Math.sqrt(5));
  const nodes = Array.from({ length: count }, (_, index) => {
    const y = 1 - 2 * (index + 0.5) / count;
    const radius = Math.sqrt(1 - y * y);
    const angle = index * goldenAngle;
    const element = makeElement('circle', nodesGroup);
    return { x: Math.cos(angle) * radius, y, z: Math.sin(angle) * radius, element };
  });

  const edges = [];
  const connected = new Set();
  nodes.forEach((node, from) => {
    const neighbors = nodes.map((other, to) => ({
      to,
      distance: Math.hypot(node.x - other.x, node.y - other.y, node.z - other.z)
    })).filter(other => other.to !== from).sort((a, b) => a.distance - b.distance).slice(0, 4);
    neighbors.forEach(({ to }) => {
      const key = Math.min(from, to) + ':' + Math.max(from, to);
      if (connected.has(key)) return;
      connected.add(key);
      edges.push({ from, to, element: makeElement('path', linksGroup) });
    });
  });

  const signals = Array.from({ length: 18 }, (_, index) => ({
    edge: edges[(index * 13) % edges.length],
    offset: index * 0.618,
    halo: makeElement('circle', signalsGroup),
    dot: makeElement('circle', signalsGroup)
  }));
  signals.forEach(signal => {
    signal.halo.setAttribute('class', 'neural-signal-halo');
    signal.halo.setAttribute('r', '8');
    signal.dot.setAttribute('class', 'neural-signal-dot');
    signal.dot.setAttribute('r', '2.8');
  });

  const draw = time => {
    const turn = 0.3 + Math.sin(time * 0.19) * 0.32;
    const cos = Math.cos(turn);
    const sin = Math.sin(turn);
    const points = nodes.map((node, index) => {
      const wave = Math.sin(time * 0.9 + node.y * 3.5 + node.z * 1.8);
      const swell = 1 + 0.055 * Math.sin(time * 0.8 + node.y * 2.2);
      const x = node.x * 182 * swell + wave * 15;
      const y = node.y * 186 / swell + Math.sin(time * 0.95 + node.x * 3) * 12;
      const z = node.z * 178 + Math.cos(time * 0.75 + node.y * 3) * 9;
      const depth = z * cos - x * sin;
      const perspective = 1 + depth / 1000;
      const point = {
        x: 280 + (x * cos + z * sin) * perspective,
        y: 280 + y * perspective,
        depth: Math.max(0, Math.min(1, (depth + 210) / 420))
      };
      node.element.setAttribute('cx', point.x.toFixed(2));
      node.element.setAttribute('cy', point.y.toFixed(2));
      node.element.setAttribute('r', (2 + point.depth * 2.2).toFixed(2));
      node.element.setAttribute('opacity', (0.25 + point.depth * 0.7).toFixed(2));
      // Selected neurons stay hollow, giving the network a lighter appearance.
      node.element.setAttribute('fill', index % 5 === 0 ? '#ffffff' : '#1a73e8');
      return point;
    });

    edges.forEach((edge, index) => {
      const a = points[edge.from];
      const b = points[edge.to];
      const bend = Math.sin(time * 0.85 + index * 0.7) * 0.16;
      edge.control = {
        x: (a.x + b.x) / 2 + (b.y - a.y) * bend,
        y: (a.y + b.y) / 2 - (b.x - a.x) * bend
      };
      edge.element.setAttribute('d', 'M' + a.x.toFixed(2) + ',' + a.y.toFixed(2) +
        ' Q' + edge.control.x.toFixed(2) + ',' + edge.control.y.toFixed(2) +
        ' ' + b.x.toFixed(2) + ',' + b.y.toFixed(2));
      edge.element.setAttribute('opacity', (0.1 + (a.depth + b.depth) * 0.22).toFixed(2));
    });

    signals.forEach(signal => {
      const phase = (time * 0.16 + signal.offset) % 1;
      const inverse = 1 - phase;
      const a = points[signal.edge.from];
      const b = points[signal.edge.to];
      const control = signal.edge.control;
      const x = inverse * inverse * a.x + 2 * inverse * phase * control.x + phase * phase * b.x;
      const y = inverse * inverse * a.y + 2 * inverse * phase * control.y + phase * phase * b.y;
      const opacity = Math.sin(phase * Math.PI) * (0.35 + (a.depth + b.depth) * 0.3);
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
    if (motion.matches) {
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
})();
