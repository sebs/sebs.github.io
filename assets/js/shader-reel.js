// Shader reel — the homepage hero panel.
//
// A playlist of fragment shaders painted in the active Carbon theme: every
// colour comes from a --cds-* token read off the page, so the reel follows the
// light/dark toggle like the rest of the UI. The stage tilts toward the pointer
// (CSS 3D, see _sass/site/_hero.scss) and the same pointer offset is handed to
// the shaders as `uMouse`, so the picture shifts with depth inside the frame.
//
// Progressive enhancement: without WebGL 2 nothing here runs and the panel
// stays the static grid. With prefers-reduced-motion the reel starts paused,
// does not tilt and shows each shader as a still frame; play is an opt-in.
(function () {
  'use strict';

  var root = document.querySelector('[data-reel]');
  if (!root) return;
  var canvas = root.querySelector('[data-reel-canvas]');
  var stage = root.querySelector('[data-reel-stage]');
  var gl = canvas.getContext('webgl2', {
    alpha: false,
    antialias: false,
    depth: false,
    powerPreference: 'low-power'
  });
  if (!gl) return;

  var TRACK_SECONDS = 14;
  var WIPE_OUT = 0.45;
  var WIPE_IN = 0.9;

  // ---- Shaders -------------------------------------------------------------
  // Each track supplies `vec3 scene(vec2 uv, vec2 p)`: uv is 0..1 across the
  // canvas, p is centred and aspect-correct (short side = 1). The shared main()
  // composites the wipe transition and a 1/255 dither against banding.

  var PRELUDE = [
    '#version 300 es',
    'precision highp float;',
    'uniform vec2 uRes;',
    'uniform float uTime;',
    'uniform vec2 uMouse;',
    'uniform float uReveal;',
    'uniform vec3 uBg, uLayer, uLine, uAccent, uHi, uAlt;',
    'out vec4 outColor;',
    'float hash12(vec2 p) { vec3 p3 = fract(vec3(p.xyx) * .1031); p3 += dot(p3, p3.yzx + 33.33); return fract((p3.x + p3.y) * p3.z); }',
    'vec2 hash22(vec2 p) { vec3 p3 = fract(vec3(p.xyx) * vec3(.1031, .1030, .0973)); p3 += dot(p3, p3.yzx + 33.33); return fract((p3.xx + p3.yz) * p3.zy); }',
    'float vnoise(vec2 p) {',
    '  vec2 i = floor(p), f = fract(p), u = f * f * (3. - 2. * f);',
    '  return mix(mix(hash12(i), hash12(i + vec2(1, 0)), u.x), mix(hash12(i + vec2(0, 1)), hash12(i + vec2(1, 1)), u.x), u.y);',
    '}',
    'float fbm(vec2 p) {',
    '  float s = 0., a = .5; mat2 r = mat2(.8, .6, -.6, .8);',
    '  for (int i = 0; i < 5; i++) { s += a * vnoise(p); p = r * p * 2.02; a *= .5; }',
    '  return s;',
    '}',
    'float px() { return 1. / min(uRes.x, uRes.y); }',
    ''
  ].join('\n');

  var MAIN = [
    'void main() {',
    '  vec2 uv = gl_FragCoord.xy / uRes;',
    '  vec2 p = (gl_FragCoord.xy - .5 * uRes) / min(uRes.x, uRes.y);',
    '  vec3 c = scene(uv, p);',
    // A slightly slanted wipe with a one-pixel accent leading edge.
    '  float d = uv.x * .85 + (1. - uv.y) * .15;',
    '  float e = uReveal * 1.12 - .06;',
    '  float aa = 1.5 / uRes.x;',
    '  c = mix(uBg, c, smoothstep(e + aa, e - aa, d));',
    '  float edge = (1. - smoothstep(0., 2. * aa, abs(d - e))) * step(.001, uReveal) * step(uReveal, .999);',
    '  c = mix(c, uAccent, edge);',
    '  c += (hash12(gl_FragCoord.xy + fract(uTime) * 97.) - .5) * (3. / 255.);',
    '  outColor = vec4(c, 1.);',
    '}'
  ].join('\n');

  var TRACKS = [
    {
      name: 'topography.glsl',
      sub: 'Warped noise, cut into contours',
      still: 40,
      frag: [
        'vec3 scene(vec2 uv, vec2 p) {',
        '  float t = uTime * .035;',
        '  vec2 q = p * 1.35;',
        // Height-dependent parallax: high ground slides further with the pointer.
        '  float h0 = fbm(q + vec2(t, -t * .6));',
        '  q += uMouse * (.05 + .16 * h0);',
        '  vec2 w = vec2(fbm(q + vec2(1.7, 9.2) + t), fbm(q + vec2(8.3, 2.8) - t));',
        '  float h = fbm(q + 1.1 * w);',
        '  float v = h * 26.;',
        '  float f = fract(v);',
        '  float dist = min(f, 1. - f) / max(fwidth(v), 1e-4);',
        '  float major = step(mod(floor(v + .5), 5.), .5);',
        '  float minor = 1. - smoothstep(.3, 1., dist);',
        '  float maj = (1. - smoothstep(.6, 1.5, dist)) * major;',
        '  vec3 c = mix(uBg, uLayer, smoothstep(.25, .85, h));',
        '  c = mix(c, uLine, minor * .7);',
        '  vec3 ink = mix(uAccent, uHi, smoothstep(.55, .8, h));',
        '  c = mix(c, ink, maj);',
        // A survey line sweeping upward lights the contours it crosses.
        '  float scan = exp(-pow((uv.y - fract(uTime * .045)) * 26., 2.));',
        '  c = mix(c, uAlt, scan * max(minor, maj) * .7);',
        '  c = mix(c, uAccent, smoothstep(.74, .92, h) * .2);',
        '  return mix(c, uBg, smoothstep(.55, 1., length(p)));',
        '}'
      ].join('\n')
    },
    {
      name: 'dependencies.glsl',
      sub: 'Three layers deep, packets in flight',
      still: 12,
      frag: [
        'float seg(vec2 p, vec2 a, vec2 b, out float h) {',
        '  vec2 pa = p - a, ba = b - a;',
        '  h = clamp(dot(pa, ba) / dot(ba, ba), 0., 1.);',
        '  return length(pa - ba * h);',
        '}',
        'vec2 node(vec2 cell, float layer) {',
        '  vec2 r = hash22(cell + layer * 17.31);',
        '  return cell + .5 + .34 * sin(uTime * .3 * (.4 + r) + r * 6.2831);',
        '}',
        'vec3 scene(vec2 uv, vec2 p) {',
        '  vec3 c = uBg;',
        '  for (int L = 0; L < 3; L++) {',
        '    float l = float(L) / 2.;',            // 0 far .. 1 near
        '    float s = mix(10., 4.2, l);',
        '    vec2 pos = (p + uMouse * mix(.03, .16, l)) * s + vec2(uTime * mix(.05, .16, l), 0.) + l * 31.;',
        '    float w = s * px();',
        '    vec2 cell = floor(pos);',
        '    float fade = mix(.35, 1., l);',
        '    vec3 edgeCol = mix(uBg, uLine, fade);',
        '    float edgeA = 0., pulse = 0.;',
        '    for (int j = -1; j <= 1; j++) for (int i = -1; i <= 1; i++) {',
        '      vec2 cid = cell + vec2(i, j);',
        '      vec2 a = node(cid, float(L));',
        '      for (int k = 0; k < 3; k++) {',
        '        vec2 dir = k == 0 ? vec2(1, 0) : (k == 1 ? vec2(0, 1) : vec2(1, 1));',
        '        float r = hash12(cid * 1.7 + dir * 9.1 + float(L));',
        '        if (r < .38) continue;',
        '        float h;',
        '        float d = seg(pos, a, node(cid + dir, float(L)), h);',
        '        edgeA = max(edgeA, 1. - smoothstep(0., w * 1.3, d));',
        '        if (r > .72) {',
        '          float at = fract(uTime * (.22 + .3 * r) + r * 7.);',
        '          pulse = max(pulse, (1. - smoothstep(0., w * 2.6, d)) * smoothstep(.07, 0., abs(h - at)));',
        '        }',
        '      }',
        '    }',
        '    c = mix(c, edgeCol, edgeA);',
        '    c = mix(c, mix(uBg, uAlt, fade), pulse);',
        // Nodes: square, like everything else in Carbon. Some are filled.
        '    for (int j = -1; j <= 1; j++) for (int i = -1; i <= 1; i++) {',
        '      vec2 cid = cell + vec2(i, j);',
        '      vec2 d = abs(pos - node(cid, float(L)));',
        '      float sq = max(d.x, d.y);',
        '      float sz = mix(.045, .07, l);',
        '      float body = 1. - smoothstep(sz - w, sz, sq);',
        '      float hole = 1. - smoothstep(sz - 2.5 * w, sz - 1.5 * w, sq);',
        '      bool solid = hash12(cid + float(L) * 3.3) > .7;',
        '      vec3 ink = mix(uBg, solid ? uAccent : uHi, fade);',
        '      c = mix(c, ink, body);',
        '      if (!solid) c = mix(c, uBg, hole);',
        '    }',
        '  }',
        '  return mix(c, uBg, smoothstep(.6, 1.05, length(p)));',
        '}'
      ].join('\n')
    },
    {
      name: 'signal.glsl',
      sub: '36 ridges, drawn front to back',
      still: 21,
      frag: [
        'vec3 scene(vec2 uv, vec2 p) {',
        '  const int N = 36;',
        '  float horizon = .4;',
        '  float sweep = fract(uTime * .05);',
        '  for (int i = 0; i < N; i++) {',
        '    float fi = float(i) / float(N - 1);',     // 0 front .. 1 back
        '    float z = mix(1., 3.4, fi);',
        '    vec2 off = uMouse * vec2(.22, .1) / z;',
        '    float x = (p.x - off.x) * z;',
        '    float base = horizon - .88 / z + off.y;',
        '    float env = exp(-x * x * 2.6);',
        '    float n = fbm(vec2(x * 2.1, fi * 7. - uTime * .3));',
        '    float ridge = env * (pow(n, 2.2) * 2.2 + .04 * vnoise(vec2(x * 18., fi * 40.)));',
        '    float y = base + .3 * ridge / z;',
        '    float d = p.y - y;',
        '    float w = px() * mix(1.4, .8, fi);',
        '    float ink = 1. - smoothstep(w * .5, w * .5 + px(), abs(d));',
        '    vec3 col = mix(uLine, uAccent, smoothstep(.12, .5, ridge));',
        '    col = mix(col, uAlt, exp(-pow((fi - sweep) * 22., 2.)));',
        '    col = mix(col, uBg, fi * .7);',
        '    if (ink > 0.) return mix(uBg, col, ink);',
        '    if (d < 0.) return uBg;',                   // hidden behind this ridge
        '  }',
        '  return mix(uBg, uAccent, .07 * exp(-abs(p.y - horizon) * 9.));',
        '}'
      ].join('\n')
    },
    {
      name: 'blocks.glsl',
      sub: 'A heightfield, walked cell by cell',
      still: 30,
      frag: [
        'float height(vec2 c) {',
        '  float n = vnoise(c * .16 + vec2(0., uTime * .04));',
        '  float wave = max(0., sin(length(c - vec2(0., uTime * .9 + 8.)) * .45 - uTime * 1.1));',
        '  float h = .25 + 2.3 * n * n + .5 * wave * wave;',
        '  return floor(h * 4.) / 4.;',
        '}',
        'vec3 scene(vec2 uv, vec2 p) {',
        '  vec3 ro = vec3(uMouse.x * 3., 7. + uMouse.y * 2., uTime * .9 - 6.);',
        '  vec3 ta = vec3(0., 0., uTime * .9 + 6.);',
        '  vec3 fw = normalize(ta - ro);',
        '  vec3 rt = normalize(cross(vec3(0, 1, 0), fw));',
        '  vec3 up = cross(fw, rt);',
        '  vec3 rd = normalize(p.x * rt + p.y * up + 1.25 * fw);',
        '  if (rd.y >= -.001) return uBg;',
        // Start where the ray drops below the tallest possible block, then step
        // through the grid one cell at a time (DDA): exact, and cheap.
        '  float t = (ro.y - 3.4) / -rd.y;',
        '  vec3 o = ro + rd * t;',
        '  vec2 cell = floor(o.xz);',
        '  vec2 st = sign(rd.xz);',
        '  vec2 tDelta = abs(1. / rd.xz);',
        '  vec2 tMax = (cell + max(st, 0.) - ro.xz) / rd.xz;',
        '  int axis = -1;',
        '  for (int i = 0; i < 110; i++) {',
        '    float h = height(cell);',
        '    float tExit = min(tMax.x, tMax.y);',
        '    vec3 col; bool hit = false; float th = t;',
        '    if (ro.y + rd.y * t < h && axis >= 0) {',
        '      hit = true;',
        '      vec3 hp = ro + rd * t;',
        '      float strata = 1. - smoothstep(0., .035, abs(fract(hp.y * 4. + .5) - .5) * .25);',
        '      col = axis == 0 ? mix(uBg, uLine, .6) : mix(uBg, uLine, .32);',
        '      col = mix(col, uBg, strata * .35);',
        '    } else if (ro.y + rd.y * tExit < h) {',
        '      hit = true;',
        '      th = (h - ro.y) / rd.y;',
        '      vec2 f = fract((ro + rd * th).xz);',
        '      float edge = min(min(f.x, 1. - f.x), min(f.y, 1. - f.y));',
        '      float lit = hash12(cell) > .93 ? 1. : 0.;',
        '      col = mix(mix(uBg, uLine, .85), uAccent, max(smoothstep(1.4, 2.8, h), lit));',
        '      col = mix(col, uHi, lit * smoothstep(2., 2.8, h));',
        '      col = mix(uBg, col, smoothstep(.02, .05, edge));',
        '    }',
        '    if (hit) return mix(col, uBg, smoothstep(14., 42., th));',
        '    if (tMax.x < tMax.y) { t = tMax.x; tMax.x += tDelta.x; cell.x += st.x; axis = 0; }',
        '    else { t = tMax.y; tMax.y += tDelta.y; cell.y += st.y; axis = 1; }',
        '  }',
        '  return uBg;',
        '}'
      ].join('\n')
    },
    {
      name: 'tunnel.glsl',
      sub: 'A corridor that never ends',
      still: 9,
      frag: [
        'vec3 scene(vec2 uv, vec2 p) {',
        '  vec2 q = p - uMouse * .14;',
        '  float a = .12 * sin(uTime * .11);',
        '  q = mat2(cos(a), -sin(a), sin(a), cos(a)) * q;',
        '  float r = max(max(abs(q.x), abs(q.y)), 1e-3);',
        '  float z = .32 / r;',
        '  float zt = z + uTime * 1.1;',
        // Perimeter coordinate 0..4: right wall, top, left, bottom.
        '  vec2 n = q / r;',
        '  float s = abs(q.x) >= abs(q.y)',
        '    ? (q.x > 0. ? (n.y + 1.) * .5 : 2. + (1. - n.y) * .5)',
        '    : (q.y > 0. ? 1. + (1. - n.x) * .5 : 3. + (n.x + 1.) * .5);',
        '  vec2 g = vec2(s * 6., zt * 1.3);',
        // Distance to the nearest grid line, in pixels.
        '  vec2 gd = abs(fract(g - .5) - .5) / max(fwidth(g), vec2(1e-4));',
        '  float grid = 1. - smoothstep(.5, 1.3, min(gd.x, gd.y));',
        '  vec2 tile = floor(g);',
        '  float ring = step(mod(tile.y, 8.), .5);',
        '  float fog = exp(-z * .32);',
        '  vec3 c = uBg;',
        '  float lit = step(.94, hash12(tile + floor(uTime * .5) * .13)) * smoothstep(.9, 2.2, z);',
        '  c = mix(c, uAccent, lit * .3 * fog);',
        '  vec3 ink = mix(uLine, uAccent, ring);',
        '  c = mix(c, ink, grid * fog);',
        // A pulse of light rides the corridor toward the viewer.
        '  float pulse = exp(-pow(fract(zt * .12) - .5, 2.) * 300.);',
        '  c = mix(c, uAlt, pulse * grid * fog);',
        '  return c;',
        '}'
      ].join('\n')
    }
  ];

  // ---- GL plumbing ---------------------------------------------------------
  var VERT = '#version 300 es\nin vec2 aPos;\nvoid main() { gl_Position = vec4(aPos, 0., 1.); }';
  var UNIFORMS = ['uRes', 'uTime', 'uMouse', 'uReveal', 'uBg', 'uLayer', 'uLine', 'uAccent', 'uHi', 'uAlt'];
  var vbo;

  function compile(type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS) && !gl.isContextLost()) {
      console.warn('shader-reel:', gl.getShaderInfoLog(sh));
      return null;
    }
    return sh;
  }

  function program(track) {
    if (track.prog !== undefined) return track.prog;
    var vs = compile(gl.VERTEX_SHADER, VERT);
    var fs = compile(gl.FRAGMENT_SHADER, PRELUDE + track.frag + '\n' + MAIN);
    track.prog = null;
    if (!vs || !fs) return null;
    var pr = gl.createProgram();
    gl.attachShader(pr, vs);
    gl.attachShader(pr, fs);
    gl.bindAttribLocation(pr, 0, 'aPos');
    gl.linkProgram(pr);
    gl.deleteShader(vs);
    gl.deleteShader(fs);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) {
      console.warn('shader-reel:', gl.getProgramInfoLog(pr));
      return null;
    }
    var loc = {};
    UNIFORMS.forEach(function (u) { loc[u] = gl.getUniformLocation(pr, u); });
    track.prog = { pr: pr, loc: loc };
    return track.prog;
  }

  function setupGL() {
    TRACKS.forEach(function (t) { delete t.prog; });
    vbo = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
    // One oversized triangle covers the viewport.
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
  }

  // ---- Theme colours -------------------------------------------------------
  var TOKENS = {
    uBg: '--cds-background',
    uLayer: '--cds-layer-01',
    uLine: '--cds-border-subtle-01',
    uAccent: '--cds-interactive',
    uHi: '--cds-link-primary',
    uAlt: '--cds-tag-color-teal'
  };
  var colors = {};
  var probe = document.createElement('span');
  probe.hidden = true;
  root.appendChild(probe);

  function readColors() {
    Object.keys(TOKENS).forEach(function (u) {
      probe.style.color = 'var(' + TOKENS[u] + ')';
      var m = getComputedStyle(probe).color.match(/[\d.]+/g) || [0, 0, 0];
      colors[u] = [m[0] / 255, m[1] / 255, m[2] / 255];
    });
  }

  // ---- UI ------------------------------------------------------------------
  var ui = {
    index: root.querySelector('[data-reel-index]'),
    title: root.querySelector('[data-reel-title]'),
    sub: root.querySelector('[data-reel-sub]'),
    tracks: root.querySelector('[data-reel-tracks]'),
    toggle: root.querySelector('[data-reel-toggle]'),
    iconPlay: root.querySelector('[data-reel-icon="play"]'),
    iconPause: root.querySelector('[data-reel-icon="pause"]')
  };
  var segments = TRACKS.map(function (t, i) {
    var li = document.createElement('li');
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'site-reel__track';
    b.setAttribute('aria-label', 'Play ' + t.name);
    b.addEventListener('click', function () { go(i); });
    li.appendChild(b);
    ui.tracks.appendChild(li);
    return b;
  });

  function pad(n) { return (n < 10 ? '0' : '') + n; }

  function renderLabels() {
    var t = TRACKS[current];
    ui.index.textContent = pad(current + 1) + ' / ' + pad(TRACKS.length);
    ui.title.textContent = t.name;
    ui.sub.textContent = t.sub;
    segments.forEach(function (b, i) {
      if (i === current) b.setAttribute('aria-current', 'true');
      else b.removeAttribute('aria-current');
    });
  }

  function renderProgress() {
    var p = Math.min(elapsed / TRACK_SECONDS, 1);
    segments.forEach(function (b, i) {
      b.style.setProperty('--reel-progress', i < current ? 1 : i === current ? p.toFixed(4) : 0);
    });
  }

  function renderToggle() {
    ui.iconPlay.hidden = playing;
    ui.iconPause.hidden = !playing;
    ui.toggle.setAttribute('aria-label', (playing ? 'Pause' : 'Play') + ' shader playlist');
  }

  // ---- State ---------------------------------------------------------------
  var reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  var current = 0;
  var playing = !reduceMotion.matches;
  var elapsed = 0;          // seconds into the current track
  var clock = 0;            // shader time, frozen while paused
  var phase = 'in';         // 'in' | 'show' | 'out'
  var phaseT = 0;
  var pending = null;
  var visible = true;
  var dirty = true;
  var mouse = { x: 0, y: 0, tx: 0, ty: 0, seen: false };

  function go(i) {
    var n = (i + TRACKS.length) % TRACKS.length;
    if (n === current && phase !== 'out') return;
    if (reduceMotion.matches && !playing) {
      current = n;
      elapsed = 0;
      phase = 'show';
      renderLabels();
      dirty = true;
      kick();
      return;
    }
    pending = n;
    if (phase !== 'out') {
      // Wipe out from wherever the reveal currently is.
      phaseT = phase === 'in' ? (1 - ease(phaseT / WIPE_IN)) * WIPE_OUT : 0;
      phase = 'out';
    }
    kick();
  }

  function ease(x) {
    x = Math.min(Math.max(x, 0), 1);
    return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  }

  function reveal() {
    if (phase === 'in') return ease(phaseT / WIPE_IN);
    if (phase === 'out') return 1 - ease(phaseT / WIPE_OUT);
    return 1;
  }

  // ---- Sizing --------------------------------------------------------------
  function resize() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = canvas.clientWidth * dpr;
    var h = canvas.clientHeight * dpr;
    // Cap the fragment count: the reel is decoration, not a benchmark.
    var cap = 1100000;
    if (w * h > cap) {
      var k = Math.sqrt(cap / (w * h));
      w *= k;
      h *= k;
    }
    w = Math.max(1, Math.round(w));
    h = Math.max(1, Math.round(h));
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
      dirty = true;
      kick();
    }
  }

  // ---- Frame loop ----------------------------------------------------------
  var raf = 0;
  var last = 0;
  var running = false;

  // Schedule a frame unless one is already pending. `last = 0` marks a fresh
  // start: rAF timestamps can precede performance.now(), so a resumed loop must
  // not measure dt against a clock read outside the frame.
  function kick() {
    if (!raf && visible && !document.hidden) {
      if (!running) last = 0;
      running = true;
      raf = requestAnimationFrame(frame);
    }
  }

  function frame(now) {
    raf = 0;
    if (!visible || document.hidden) { running = false; return; }
    var dt = last ? Math.min(Math.max((now - last) / 1000, 0), 0.1) : 1 / 60;
    last = now;
    var animating = playing;

    // Pointer, eased. Touch screens get a slow drift instead.
    var still = reduceMotion.matches && !playing;
    if (!mouse.seen && playing) {
      mouse.tx = Math.sin(clock * 0.21) * 0.35;
      mouse.ty = Math.cos(clock * 0.17) * 0.25;
    }
    var tx = still ? 0 : mouse.tx;
    var ty = still ? 0 : mouse.ty;
    var k = 1 - Math.exp(-dt * 5);
    mouse.x += (tx - mouse.x) * k;
    mouse.y += (ty - mouse.y) * k;
    var settling = Math.abs(tx - mouse.x) + Math.abs(ty - mouse.y) > 0.0005;

    if (playing) {
      clock += dt;
      if (phase === 'show') {
        elapsed += dt;
        if (elapsed >= TRACK_SECONDS) go(current + 1);
      }
    }
    if (phase !== 'show') {
      animating = true;
      phaseT += dt;
      if (phase === 'out' && phaseT >= WIPE_OUT) {
        current = pending;
        pending = null;
        elapsed = 0;
        phase = 'in';
        phaseT = 0;
        renderLabels();
      } else if (phase === 'in' && phaseT >= WIPE_IN) {
        phase = 'show';
      }
    }

    if (animating || settling || dirty) {
      draw();
      dirty = false;
      stage.style.setProperty('--reel-tilt-x', (-mouse.y * 7).toFixed(3) + 'deg');
      stage.style.setProperty('--reel-tilt-y', (mouse.x * 9).toFixed(3) + 'deg');
      stage.style.setProperty('--reel-glare-x', (50 + mouse.x * 45).toFixed(2) + '%');
      stage.style.setProperty('--reel-glare-y', (50 + mouse.y * 45).toFixed(2) + '%');
      renderProgress();
      kick();
    } else {
      running = false;
    }
  }

  function draw() {
    var track = TRACKS[current];
    var p = program(track);
    gl.viewport(0, 0, canvas.width, canvas.height);
    if (!p) {
      var bg = colors.uBg;
      gl.clearColor(bg[0], bg[1], bg[2], 1);
      gl.clear(gl.COLOR_BUFFER_BIT);
      return;
    }
    var still = reduceMotion.matches && !playing;
    gl.useProgram(p.pr);
    gl.uniform2f(p.loc.uRes, canvas.width, canvas.height);
    gl.uniform1f(p.loc.uTime, still ? track.still : clock + track.still);
    gl.uniform2f(p.loc.uMouse, mouse.x, -mouse.y);
    gl.uniform1f(p.loc.uReveal, still ? 1 : reveal());
    Object.keys(TOKENS).forEach(function (u) { gl.uniform3fv(p.loc[u], colors[u]); });
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }

  // ---- Wiring --------------------------------------------------------------
  root.querySelector('[data-reel-prev]').addEventListener('click', function () { go(current - 1); });
  root.querySelector('[data-reel-next]').addEventListener('click', function () { go(current + 1); });
  ui.toggle.addEventListener('click', function () {
    playing = !playing;
    renderToggle();
    dirty = true;
    kick();
  });

  window.addEventListener('pointermove', function (e) {
    if (e.pointerType !== 'mouse') return;
    var r = stage.getBoundingClientRect();
    mouse.seen = true;
    mouse.tx = Math.max(-1, Math.min(1, (e.clientX - (r.left + r.width / 2)) / (window.innerWidth / 2)));
    mouse.ty = Math.max(-1, Math.min(1, (e.clientY - (r.top + r.height / 2)) / (window.innerHeight / 2)));
    kick();
  }, { passive: true });
  document.documentElement.addEventListener('pointerleave', function () {
    mouse.tx = 0;
    mouse.ty = 0;
    kick();
  });

  new MutationObserver(function () {
    readColors();
    dirty = true;
    kick();
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  reduceMotion.addEventListener('change', function () {
    playing = !reduceMotion.matches;
    renderToggle();
    dirty = true;
    kick();
  });

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      if (visible) { dirty = true; kick(); }
    }).observe(root);
  }
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) { dirty = true; kick(); }
  });

  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas);
  else window.addEventListener('resize', resize);

  canvas.addEventListener('webglcontextlost', function (e) {
    e.preventDefault();
    root.classList.remove('is-live');
    cancelAnimationFrame(raf);
    raf = 0;
  });
  canvas.addEventListener('webglcontextrestored', function () {
    setupGL();
    root.classList.add('is-live');
    dirty = true;
    kick();
  });

  // ---- Go ------------------------------------------------------------------
  setupGL();
  readColors();
  if (reduceMotion.matches) phase = 'show';
  renderLabels();
  renderToggle();
  resize();
  if (!program(TRACKS[current])) return;   // leave the static panel in place
  root.classList.add('is-live');
  dirty = true;
  kick();
})();
