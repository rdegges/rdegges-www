// Interactive widgets for "The Programmer Trolley Problem".
//
// Every number comes from window.TROLLEY_DATA (data.js), which `trolley
// export` builds from a real run. Nothing here is made up or re-rolled:
// the only randomness is the diorama's coin flip, which uses Jev's own
// probability for that exact track layout.
(function () {
  "use strict";

  var DATA = window.TROLLEY_DATA;
  if (!DATA) return;

  var SVGNS = "http://www.w3.org/2000/svg";
  var REDUCED = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------- small helpers ----------

  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    setAttrs(n, attrs);
    append(n, kids);
    return n;
  }

  function sv(tag, attrs, kids) {
    var n = document.createElementNS(SVGNS, tag);
    setAttrs(n, attrs);
    append(n, kids);
    return n;
  }

  function setAttrs(n, attrs) {
    for (var k in attrs || {}) {
      if (attrs[k] == null) continue;
      if (k === "text") n.textContent = attrs[k];
      else if (k === "on") for (var ev in attrs.on) n.addEventListener(ev, attrs.on[ev]);
      else n.setAttribute(k, attrs[k]);
    }
  }

  function append(n, kids) {
    (kids || []).forEach(function (k) {
      if (k == null) return;
      n.appendChild(typeof k === "string" ? document.createTextNode(k) : k);
    });
  }

  function fmt(x, d) { return x.toFixed(d == null ? 3 : d); }
  function pct(x) { return Math.round(x * 100) + "%"; }
  function wait(ms) { return new Promise(function (r) { setTimeout(r, REDUCED ? 0 : ms); }); }

  function phrase(g) {
    return g.n + " " + g.name + " " + (g.n === 1 ? DATA.noun.one : DATA.noun.many);
  }

  function key(main, side) {
    return main.name + "×" + main.n + "|" + side.name + "×" + side.n;
  }

  function seedOf(name) {
    for (var i = 0; i < DATA.contestants.length; i++) {
      if (DATA.contestants[i].name === name) return DATA.contestants[i].seed;
    }
    return null;
  }

  // The same template fill as the Go code, so "what Jev was asked" is the
  // exact text Jev saw.
  function fill(text, main, side) {
    function agree(g, one, many) { return g.n === 1 ? one : many; }
    var map = {
      "{main}": phrase(main), "{side}": phrase(side),
      "{main_is}": agree(main, "is", "are"), "{side_is}": agree(side, "is", "are"),
      "{main_dies}": agree(main, "dies", "die"), "{side_dies}": agree(side, "dies", "die"),
      "{main_lives}": agree(main, "lives", "live"), "{side_lives}": agree(side, "lives", "live"),
      "{context}": DATA.context
    };
    return text.replace(/\{[a-z_]+\}/g, function (m) { return map[m] != null ? map[m] : m; });
  }

  // One tooltip for the whole page; charts position it on hover and focus.
  var tip = null;
  function showTip(evt, html) {
    if (!tip) {
      tip = el("div", { "class": "tw-tip", role: "tooltip" });
      document.body.appendChild(tip);
    }
    tip.innerHTML = html;
    tip.style.display = "block";
    var r = evt.target.getBoundingClientRect();
    var x = (evt.clientX != null && evt.clientX !== 0 ? evt.clientX : r.left + r.width / 2);
    var y = (evt.clientY != null && evt.clientY !== 0 ? evt.clientY : r.top);
    var w = tip.offsetWidth;
    var left = Math.min(Math.max(8, x - w / 2), window.innerWidth - w - 8);
    tip.style.left = left + window.scrollX + "px";
    tip.style.top = y + window.scrollY - tip.offsetHeight - 14 + "px";
  }
  function hideTip() { if (tip) tip.style.display = "none"; }

  function hoverable(node, html) {
    node.setAttribute("tabindex", "0");
    node.addEventListener("mousemove", function (e) { showTip(e, html()); });
    node.addEventListener("focus", function (e) { showTip(e, html()); });
    node.addEventListener("mouseleave", hideTip);
    node.addEventListener("blur", hideTip);
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  // ---------- the diorama ----------

  var MAIN_Y = 190, SIDE_Y = 84, JUNCTION_X = 230, VICTIM_X = 452;
  var PATHS = {
    leave: "M 70 190 L 636 190",
    pull: "M 70 190 L 230 190 C 300 190 320 84 400 84 L 636 84"
  };

  function drawTrack(g, d) {
    g.appendChild(sv("path", { d: d, "class": "tw-ties" }));
    g.appendChild(sv("path", { d: d, "class": "tw-rail-out" }));
    g.appendChild(sv("path", { d: d, "class": "tw-rail-in" }));
  }

  function person(x, y, i) {
    // A tied-up stick figure. Rows alternate slightly so a crowd of ten
    // still reads as separate people.
    var dy = i % 2 ? -4 : 0;
    return sv("g", { "class": "tw-person", transform: "translate(" + x + "," + (y + dy) + ") scale(1.25)" }, [
      sv("g", { "class": "tw-body" }, [
        sv("circle", { cx: 0, cy: -27, r: 5.5 }),
        sv("line", { x1: 0, y1: -21, x2: 0, y2: -9 }),
        sv("line", { x1: 0, y1: -9, x2: -5, y2: 0 }),
        sv("line", { x1: 0, y1: -9, x2: 5, y2: 0 }),
        sv("line", { x1: -6, y1: -17, x2: 6, y2: -17 }),
        sv("rect", { "class": "tw-rope", x: -6, y: -16, width: 12, height: 3, rx: 1 })
      ])
    ]);
  }

  function crowd(layer, group, y) {
    var g = sv("g", { "class": "tw-crowd" });
    var gap = group.n > 5 ? 18 : 24;
    for (var i = 0; i < group.n; i++) g.appendChild(person(VICTIM_X + i * gap, y, i));
    var label = phrase(group);
    // Sized for a phone, where the whole stage shrinks to about 40%.
    var w = label.length * 8.4 + 22;
    g.appendChild(sv("g", { "class": "tw-tag", transform: "translate(" + (VICTIM_X - 12) + "," + (y - 72) + ")" }, [
      sv("rect", { x: 0, y: 0, width: w, height: 24, rx: 12 }),
      sv("text", { x: w / 2, y: 17, "text-anchor": "middle", text: label })
    ]));
    layer.appendChild(g);
    return g;
  }

  function trolleyShape() {
    return sv("g", { "class": "tw-trolley" }, [
      sv("rect", { x: -36, y: -50, width: 72, height: 36, rx: 7, "class": "tw-trolley-body" }),
      sv("rect", { x: -30, y: -56, width: 60, height: 8, rx: 3, "class": "tw-trolley-roof" }),
      sv("rect", { x: -28, y: -43, width: 14, height: 12, rx: 2, "class": "tw-trolley-window" }),
      sv("rect", { x: -7, y: -43, width: 14, height: 12, rx: 2, "class": "tw-trolley-window" }),
      sv("rect", { x: 14, y: -43, width: 14, height: 12, rx: 2, "class": "tw-trolley-window" }),
      sv("circle", { cx: -20, cy: -10, r: 7, "class": "tw-wheel" }),
      sv("circle", { cx: 20, cy: -10, r: 7, "class": "tw-wheel" })
    ]);
  }

  function robot() {
    // Jev, standing by the lever, looking like it would rather not.
    return sv("g", { "class": "tw-robot", transform: "translate(318,262)" }, [
      sv("line", { x1: 0, y1: -52, x2: 0, y2: -60, "class": "tw-robot-line" }),
      sv("circle", { cx: 0, cy: -62, r: 3, "class": "tw-robot-bulb" }),
      sv("rect", { x: -13, y: -52, width: 26, height: 18, rx: 5, "class": "tw-robot-head" }),
      sv("circle", { cx: -5, cy: -43, r: 2.4, "class": "tw-robot-eye" }),
      sv("circle", { cx: 5, cy: -43, r: 2.4, "class": "tw-robot-eye" }),
      sv("rect", { x: -11, y: -32, width: 22, height: 24, rx: 4, "class": "tw-robot-head" }),
      sv("line", { x1: -11, y1: -26, x2: -24, y2: -20, "class": "tw-robot-line tw-robot-arm" }),
      sv("line", { x1: -5, y1: -8, x2: -6, y2: 0, "class": "tw-robot-line" }),
      sv("line", { x1: 5, y1: -8, x2: 6, y2: 0, "class": "tw-robot-line" }),
      sv("text", { x: 0, y: 16, "text-anchor": "middle", "class": "tw-robot-name", text: "Jev" })
    ]);
  }

  function lever() {
    var handle = sv("g", { "class": "tw-lever-handle", transform: "rotate(-28 284 258)" }, [
      sv("line", { x1: 284, y1: 258, x2: 284, y2: 222 }),
      sv("circle", { cx: 284, cy: 220, r: 5 })
    ]);
    var g = sv("g", { "class": "tw-lever" }, [
      sv("rect", { x: 270, y: 254, width: 28, height: 10, rx: 3, "class": "tw-lever-base" }),
      handle
    ]);
    return { g: g, handle: handle };
  }

  function bubble(text) {
    var w = Math.max(80, text.length * 8 + 20);
    return sv("g", { "class": "tw-bubble", transform: "translate(344,214)" }, [
      // The tail points left, at Jev.
      sv("path", { d: "M0 0 h" + w + " a8 8 0 0 1 8 8 v16 a8 8 0 0 1 -8 8 h-" + w + " a8 8 0 0 1 -8 -8 v-4 l-10 -2 l10 -6 v-4 a8 8 0 0 1 8 -8 z" }),
      sv("text", { x: w / 2 + 4, y: 21, "text-anchor": "middle", text: text })
    ]);
  }

  function bonk(x, y) {
    var pts = [];
    for (var i = 0; i < 16; i++) {
      var r = i % 2 ? 13 : 26, a = (Math.PI * 2 * i) / 16;
      pts.push((x + r * Math.cos(a)).toFixed(1) + "," + (y + r * Math.sin(a)).toFixed(1));
    }
    return sv("g", { "class": "tw-bonk" }, [
      sv("polygon", { points: pts.join(" ") }),
      sv("text", { x: x, y: y + 4, "text-anchor": "middle", text: "BONK" })
    ]);
  }

  // isLive lets the caller abandon an animation: once it returns false the
  // trolley stops where it is and the promise resolves false.
  function animateAlong(node, pathD, ms, onTick, isLive) {
    var path = sv("path", { d: pathD });
    var tmp = sv("svg", { width: 0, height: 0, style: "position:absolute" }, [path]);
    document.body.appendChild(tmp);
    var len = path.getTotalLength();
    function at(t) {
      var l = len * t;
      var p = path.getPointAtLength(l), q = path.getPointAtLength(Math.min(len, l + 1));
      var deg = Math.atan2(q.y - p.y, q.x - p.x) * 180 / Math.PI;
      node.setAttribute("transform", "translate(" + p.x + "," + p.y + ") rotate(" + deg + ")");
      if (onTick) onTick(p);
    }
    return new Promise(function (resolve) {
      if (REDUCED) { at(1); tmp.remove(); resolve(true); return; }
      var start = null;
      function step(ts) {
        if (isLive && !isLive()) { tmp.remove(); resolve(false); return; }
        if (start == null) start = ts;
        var t = Math.min(1, (ts - start) / ms);
        // Ease in only: trolleys do not slow down for anybody.
        at(t * t * (3 - 2 * t) * 0.35 + t * 0.65);
        if (t < 1) requestAnimationFrame(step);
        else { tmp.remove(); resolve(true); }
      }
      requestAnimationFrame(step);
    });
  }

  // opts.mode is "pair" (pick any two languages, 1 each) or "crowd"
  // (1 champion against N of one language). opts.onChange lets a chart
  // below follow the selection.
  function diorama(root, opts) {
    var names = DATA.contestants.map(function (c) { return c.name; });
    var champ = DATA.exchange ? DATA.exchange.champion : names[0];
    var state = opts.mode === "crowd"
      ? { main: { name: champ, n: 1 }, side: { name: "Python", n: 3 } }
      : { main: { name: "Python", n: 1 }, side: { name: champ, n: 1 } };
    // Every redraw bumps this, which cancels any trolley still in motion.
    var token = 0;

    var wrap = el("div", { "class": "tw-diorama" });
    var controls = el("div", { "class": "tw-controls" });
    var svg = sv("svg", { viewBox: "0 0 680 290", "class": "tw-stage", role: "img" });
    var desc = sv("desc");
    svg.appendChild(desc);

    var tracks = sv("g");
    drawTrack(tracks, "M -20 190 L 230 190");
    drawTrack(tracks, "M 230 190 L 700 190");
    drawTrack(tracks, "M 230 190 C 300 190 320 84 400 84 L 700 84");
    svg.appendChild(tracks);
    svg.appendChild(sv("text", { x: 664, y: MAIN_Y + 30, "text-anchor": "end", "class": "tw-track-label", text: "main track" }));
    svg.appendChild(sv("text", { x: 664, y: SIDE_Y - 64, "text-anchor": "end", "class": "tw-track-label", text: "side track" }));
    var people = sv("g");
    svg.appendChild(people);
    var lv = lever();
    svg.appendChild(lv.g);
    svg.appendChild(robot());
    var fx = sv("g");
    svg.appendChild(fx);
    var trolley = trolleyShape();
    svg.appendChild(trolley);

    var meter = el("div", { "class": "tw-meter" });
    var caption = el("p", { "class": "tw-caption", "aria-live": "polite" });
    var send = el("button", { type: "button", "class": "tw-btn tw-primary", text: "Send the trolley" });
    var reset = el("button", { type: "button", "class": "tw-btn", text: "Reset" });
    var swap = el("button", { type: "button", "class": "tw-btn", text: "Swap tracks" });
    var asked = el("details", { "class": "tw-asked" });

    function select(label, value, onPick) {
      var s = el("select", { "aria-label": label });
      names.forEach(function (n) { s.appendChild(el("option", { value: n, text: n })); });
      s.value = value;
      s.addEventListener("change", function () { onPick(s.value); });
      return el("label", { "class": "tw-field" }, [el("span", { text: label }), s]);
    }

    function buildControls() {
      controls.innerHTML = "";
      if (opts.mode === "crowd") {
        var other = state.main.name === champ ? state.side : state.main;
        var langs = names.filter(function (n) { return n !== champ; });
        var s = el("select", { "aria-label": "Language of the crowd" });
        langs.forEach(function (n) { s.appendChild(el("option", { value: n, text: n })); });
        s.value = other.name;
        s.addEventListener("change", function () { other.name = s.value; changed(); });
        var seg = el("div", { "class": "tw-seg", role: "group", "aria-label": "Crowd size" });
        DATA.exchange.crowds.forEach(function (n) {
          var b = el("button", { type: "button", text: String(n), "aria-pressed": String(n === other.n) });
          b.addEventListener("click", function () { other.n = n; changed(); });
          seg.appendChild(b);
        });
        controls.appendChild(el("span", { "class": "tw-field" }, [el("span", { text: "1 " + champ + " vs" }), seg]));
        controls.appendChild(el("label", { "class": "tw-field" }, [el("span", { text: "programmers of" }), s]));
      } else {
        controls.appendChild(select("Main track", state.main.name, function (v) { state.main.name = v; changed(); }));
        controls.appendChild(select("Side track", state.side.name, function (v) { state.side.name = v; changed(); }));
      }
    }

    function pPull() { return DATA.pull[key(state.main, state.side)]; }

    function changed() {
      buildControls();
      draw();
      if (opts.onChange) opts.onChange(state.main.name === champ ? state.side : state.main);
    }

    function draw() {
      token++;
      people.innerHTML = "";
      fx.innerHTML = "";
      state.mainG = crowd(people, state.main, MAIN_Y);
      state.sideG = crowd(people, state.side, SIDE_Y);
      trolley.setAttribute("transform", "translate(70,190)");
      lv.handle.setAttribute("transform", "rotate(-28 284 258)");
      svg.classList.remove("tw-route-pull", "tw-route-leave");
      var p = pPull();
      send.disabled = p == null;
      desc.textContent = phrase(state.main) + " on the main track, " + phrase(state.side) + " on the side track.";
      meter.innerHTML = "";
      if (p == null) {
        caption.textContent = state.main.name === state.side.name
          ? "Pick two different languages. (I did run 1 Python programmer against 1 Python programmer once, as a control. Jev shrugged: 0.498.)"
          : "No data for this layout.";
        asked.innerHTML = "";
        return;
      }
      meter.appendChild(el("div", { "class": "tw-meter-bar" }, [
        el("span", { "class": "tw-meter-pull", style: "width:" + (p * 100).toFixed(1) + "%" }),
        el("span", { "class": "tw-meter-leave", style: "width:" + ((1 - p) * 100).toFixed(1) + "%" })
      ]));
      meter.appendChild(el("div", { "class": "tw-meter-legend" }, [
        el("span", { text: "pulls the lever " + pct(p) }),
        el("span", { text: "leaves it alone " + pct(1 - p) })
      ]));
      caption.textContent = "In this exact setup Jev pulls the lever " + pct(p) +
        " of the time (averaged over " + DATA.runs + " runs and " + DATA.wordings.length + " wordings). Each send flips that coin.";
      var w = DATA.wordings[0];
      asked.innerHTML = "";
      asked.appendChild(el("summary", { text: "What Jev was asked" }));
      asked.appendChild(el("p", { "class": "tw-prompt", text: fill(w.state, state.main, state.side) }));
      asked.appendChild(el("p", { "class": "tw-prompt" }, [el("strong", { text: fill(w.question, state.main, state.side) })]));
      asked.appendChild(el("ul", { "class": "tw-prompt" }, [
        el("li", {}, [el("code", { text: "pull" }), " " + fill(w.pull, state.main, state.side)]),
        el("li", {}, [el("code", { text: "leave" }), " " + fill(w.leave, state.main, state.side)])
      ]));
      asked.appendChild(el("p", { "class": "tw-note", text: "This is the \"" + w.id + "\" wording. There are " + (DATA.wordings.length - 1) + " more, and every matchup also runs with the tracks swapped." }));
    }

    function go() {
      draw();
      var my = token;
      var p = pPull();
      if (p == null) return;
      send.disabled = true;
      var pull = Math.random() < p;
      var hit = pull ? state.sideG : state.mainG;
      var spared = pull ? state.mainG : state.sideG;
      var victims = pull ? state.side : state.main;
      var bonked = false;
      if (pull) lv.handle.setAttribute("transform", "rotate(28 284 258)");
      svg.classList.add(pull ? "tw-route-pull" : "tw-route-leave");
      var lines = pull
        ? ["Sorry, " + state.side.name + ".", "Fine. *pulls*", "Yoink."]
        : ["Not my lever.", "I'd rather not.", "Lever? What lever?"];
      fx.appendChild(bubble(lines[Math.floor(Math.random() * lines.length)]));
      animateAlong(trolley, PATHS[pull ? "pull" : "leave"], 1900, function (pt) {
        if (!bonked && pt.x > VICTIM_X - 40) {
          bonked = true;
          hit.classList.add("tw-hit");
          spared.classList.add("tw-spared");
          fx.appendChild(bonk(VICTIM_X + 10, (pull ? SIDE_Y : MAIN_Y) - 22));
        }
      }, function () { return my === token; }).then(function (finished) {
        if (!finished) return;
        caption.textContent = (pull ? "Jev pulled the lever. " : "Jev did not touch the lever. ") +
          "The trolley hit " + phrase(victims) + ". (It pulls " + pct(p) + " of the time here, so send it again and you might get a different answer. Jev would.)";
        send.disabled = false;
        send.textContent = "Send it again";
      });
    }

    send.addEventListener("click", go);
    reset.addEventListener("click", function () { send.textContent = "Send the trolley"; draw(); });
    swap.addEventListener("click", function () {
      var t = state.main; state.main = state.side; state.side = t;
      send.textContent = "Send the trolley";
      changed();
    });

    wrap.appendChild(controls);
    wrap.appendChild(svg);
    wrap.appendChild(meter);
    wrap.appendChild(el("div", { "class": "tw-buttons" }, [send, swap, reset]));
    wrap.appendChild(caption);
    wrap.appendChild(asked);
    root.appendChild(wrap);
    changed();
  }

  // ---------- the bracket ----------

  function seedOrder(size) {
    var order = [1];
    while (order.length < size) {
      var next = [];
      order.forEach(function (s) { next.push(s, 2 * order.length + 1 - s); });
      order = next;
    }
    return order;
  }

  function findMatch(round, x, y) {
    for (var i = 0; i < round.matches.length; i++) {
      var m = round.matches[i];
      if ((m.a.name === x && m.b.name === y) || (m.a.name === y && m.b.name === x)) return m;
    }
    return null;
  }

  // winnerSide gives the winner's name and its P(survives).
  function verdict(m) {
    var aWon = m.mean >= 0.5;
    return {
      winner: aWon ? m.a.name : m.b.name,
      loser: aWon ? m.b.name : m.a.name,
      p: aWon ? m.mean : 1 - m.mean,
      runs: aWon ? m.runs_for_a : m.runs.length - m.runs_for_a,
      flip: !aWon
    };
  }

  // Lay out the bracket from the data: which names sit in which card, and
  // which match each card is.
  function bracketPlan() {
    var rounds = DATA.bracket.rounds;
    var size = 1;
    while (size < DATA.contestants.length) size *= 2;
    var bySeed = {};
    DATA.contestants.forEach(function (c) { bySeed[c.seed] = c.name; });
    var slots = seedOrder(size).map(function (s) { return bySeed[s] || null; });
    var plan = [];
    rounds.forEach(function (round) {
      var cards = [], next = [];
      for (var i = 0; i < slots.length; i += 2) {
        var x = slots[i], y = slots[i + 1];
        if (x && y) {
          var m = findMatch(round, x, y);
          var v = verdict(m);
          cards.push({ names: [x, y], match: m, v: v });
          next.push(v.winner);
        } else {
          cards.push({ names: [x || y], bye: true });
          next.push(x || y);
        }
      }
      plan.push({ name: round.name, cards: cards });
      slots = next;
    });
    return plan;
  }

  function detailPanel(panel, card, roundName) {
    var m = card.match;
    panel.innerHTML = "";
    if (!m) return;
    var v = verdict(m);
    var winP = v.p, loseP = 1 - v.p;
    panel.appendChild(el("h4", { text: roundName + ": " + v.winner + " vs " + v.loser }));
    function line(name, p, win) {
      return el("div", { "class": "tw-dline" + (win ? " tw-win" : "") }, [
        el("span", { "class": "tw-dname", text: "[" + seedOf(name) + "] " + name }),
        el("span", { "class": "tw-dbar" }, [el("span", { style: "width:" + (p * 100).toFixed(1) + "%" })]),
        el("span", { "class": "tw-dnum", text: fmt(p) })
      ]);
    }
    panel.appendChild(line(v.winner, winP, true));
    panel.appendChild(line(v.loser, loseP, false));
    var runs = m.runs.map(function (r) { return v.flip ? 1 - r : r; });
    var lo = v.flip ? 1 - m.hi : m.lo, hi = v.flip ? 1 - m.lo : m.hi;
    panel.appendChild(el("p", { "class": "tw-note", text: "Each dot is one run: " + DATA.wordings.length * 2 + " calls, every wording with the tracks both ways. The band is the 95% confidence interval." }));
    panel.appendChild(strip([{ label: v.winner, runs: runs, lo: lo, hi: hi, mean: winP }], { width: 600, labelW: 90 }));
    var words = Object.keys(m.by_wording).sort().map(function (k) {
      var p = v.flip ? 1 - m.by_wording[k] : m.by_wording[k];
      return el("span", { "class": "tw-chip" }, [k + " ", el("strong", { text: fmt(p, 2) })]);
    });
    panel.appendChild(el("p", { "class": "tw-chips" }, [el("span", { text: v.winner + " survives, by wording: " })].concat(words)));
    panel.appendChild(el("p", { "class": "tw-note", text: v.winner + " won " + v.runs + " of " + m.runs.length + " runs. Jev left the lever alone in " + pct(m.inaction) + " of the calls." }));
  }

  function bracket(root) {
    var plan = bracketPlan();
    var wrap = el("div", { "class": "tw-bracket-wrap" });
    var scroller = el("div", { "class": "tw-scroll" });
    var grid = el("div", { "class": "tw-bracket" });
    var panel = el("div", { "class": "tw-detail", "aria-live": "polite" });
    var play = el("button", { type: "button", "class": "tw-btn tw-primary", text: "Run the bracket" });
    var all = el("button", { type: "button", "class": "tw-btn", text: "Just show me" });
    var status = el("p", { "class": "tw-caption", "aria-live": "polite", text: "Seeds are the TIOBE rank for October 2026. Python, the 1 seed, gets the bye." });
    var cols = [];
    var runId = 0;

    function row(name, cls) {
      var seed = name ? seedOf(name) : null;
      return el("div", { "class": "tw-slot " + (cls || "") }, [
        el("span", { "class": "tw-seed", text: seed ? String(seed) : "" }),
        el("span", { "class": "tw-name", text: name || "" }),
        el("span", { "class": "tw-score" })
      ]);
    }

    plan.forEach(function (round, ri) {
      var col = el("div", { "class": "tw-col" }, [el("div", { "class": "tw-col-head", text: round.name })]);
      var body = el("div", { "class": "tw-col-body" });
      round.cards.forEach(function (card) {
        var names = ri === 0 ? card.names : card.names.map(function () { return null; });
        var c = el("button", { type: "button", "class": "tw-card" + (card.bye ? " tw-bye" : ""), disabled: card.bye ? "disabled" : null });
        if (card.bye) {
          c.appendChild(row(names[0]));
          c.appendChild(el("div", { "class": "tw-slot tw-byeline", text: "bye" }));
        } else {
          c.appendChild(row(names[0]));
          c.appendChild(row(names[1]));
          c.addEventListener("click", function () {
            if (!c.classList.contains("tw-done")) return;
            grid.querySelectorAll(".tw-card.tw-selected").forEach(function (n) { n.classList.remove("tw-selected"); });
            c.classList.add("tw-selected");
            detailPanel(panel, card, round.name);
          });
        }
        card.node = c;
        body.appendChild(c);
      });
      col.appendChild(body);
      grid.appendChild(col);
      cols.push(col);
    });
    var champCol = el("div", { "class": "tw-col tw-champ-col" }, [
      el("div", { "class": "tw-col-head", text: "Champion" }),
      el("div", { "class": "tw-col-body" }, [el("div", { "class": "tw-champ" }, [
        el("span", { "class": "tw-trophy", "aria-hidden": "true", text: "🏆" }),
        el("span", { "class": "tw-champ-name", text: "?" })
      ])])
    ]);
    grid.appendChild(champCol);

    function setNames(card, names) {
      var slots = card.node.querySelectorAll(".tw-slot");
      names.forEach(function (n, i) {
        if (!slots[i] || slots[i].classList.contains("tw-byeline")) return;
        slots[i].querySelector(".tw-seed").textContent = n ? seedOf(n) : "";
        slots[i].querySelector(".tw-name").textContent = n || "";
      });
    }

    function resolve(card) {
      var slots = card.node.querySelectorAll(".tw-slot");
      var v = card.v;
      card.names.forEach(function (n, i) {
        var won = n === v.winner;
        slots[i].classList.add(won ? "tw-won" : "tw-lost");
        slots[i].querySelector(".tw-score").textContent = fmt(won ? v.p : 1 - v.p);
      });
      card.node.classList.add("tw-done");
      card.node.setAttribute("aria-label", v.winner + " beat " + v.loser + ", " + fmt(v.p) + " to " + fmt(1 - v.p) + ". Show details.");
    }

    function clear() {
      plan.forEach(function (round, ri) {
        round.cards.forEach(function (card) {
          card.node.classList.remove("tw-done", "tw-live", "tw-selected");
          card.node.querySelectorAll(".tw-slot").forEach(function (s) {
            s.classList.remove("tw-won", "tw-lost");
            var sc = s.querySelector(".tw-score");
            if (sc) sc.textContent = "";
          });
          if (ri > 0) setNames(card, card.names.map(function () { return null; }));
        });
      });
      champCol.querySelector(".tw-champ-name").textContent = "?";
      champCol.classList.remove("tw-crowned");
      panel.innerHTML = "";
    }

    function fillIn(ri, card) {
      if (ri > 0) setNames(card, card.names);
      if (!card.bye) resolve(card);
    }

    function finish() {
      champCol.querySelector(".tw-champ-name").textContent = DATA.bracket.champion;
      champCol.classList.add("tw-crowned");
      var finalCard = plan[plan.length - 1].cards[0];
      finalCard.node.classList.add("tw-selected");
      detailPanel(panel, finalCard, plan[plan.length - 1].name);
      status.textContent = "The " + seedOf(DATA.bracket.champion) + " seed takes the title. Click any match for its runs.";
    }

    play.addEventListener("click", function () {
      var my = ++runId;
      clear();
      play.disabled = true;
      var chain = Promise.resolve();
      plan.forEach(function (round, ri) {
        chain = chain.then(function () {
          if (my !== runId) return;
          status.textContent = round.name + "...";
        });
        round.cards.forEach(function (card) {
          chain = chain.then(function () {
            if (my !== runId) return;
            if (ri > 0) setNames(card, card.names);
            if (card.bye) return;
            card.node.classList.add("tw-live");
            if (card.node.scrollIntoView && scroller.scrollWidth > scroller.clientWidth) {
              scroller.scrollTo({ left: card.node.offsetLeft - 40, behavior: REDUCED ? "auto" : "smooth" });
            }
            return wait(520).then(function () {
              if (my !== runId) return;
              card.node.classList.remove("tw-live");
              resolve(card);
              status.textContent = round.name + ": " + card.v.winner + " survives, " + fmt(card.v.p) + " to " + fmt(1 - card.v.p) + ".";
              return wait(260);
            });
          });
        });
      });
      chain.then(function () {
        if (my !== runId) return;
        finish();
        play.disabled = false;
        play.textContent = "Run it again";
      });
    });

    all.addEventListener("click", function () {
      runId++;
      clear();
      plan.forEach(function (round, ri) { round.cards.forEach(function (card) { fillIn(ri, card); }); });
      finish();
      play.disabled = false;
    });

    scroller.appendChild(grid);
    wrap.appendChild(el("div", { "class": "tw-buttons" }, [play, all]));
    wrap.appendChild(scroller);
    wrap.appendChild(status);
    wrap.appendChild(panel);
    root.appendChild(wrap);
  }

  // ---------- strip chart: every run of every match ----------

  // rows: [{label, runs, lo, hi, mean}]. Scores are P(winner survives).
  function strip(rows, o) {
    var labelW = o.labelW || 170, W = o.width || 640, rowH = 26, top = 8, bottom = 30;
    var all = [];
    rows.forEach(function (r) { all = all.concat(r.runs, [r.lo, r.hi]); });
    var min = Math.min(0.46, Math.floor(Math.min.apply(null, all) * 50) / 50);
    var max = Math.max(0.56, Math.ceil(Math.max.apply(null, all) * 50) / 50);
    var H = top + rows.length * rowH + bottom;
    var x = function (p) { return labelW + ((p - min) / (max - min)) * (W - labelW - 16); };
    var g = sv("svg", { viewBox: "0 0 " + W + " " + H, "class": "tw-strip", role: "img", "aria-label": "Run scores for " + rows.length + " matchups" });
    for (var t = Math.ceil(min * 50) / 50; t <= max + 1e-9; t += 0.02) {
      g.appendChild(sv("line", { x1: x(t), x2: x(t), y1: top, y2: H - bottom, "class": "tw-grid" + (Math.abs(t - 0.5) < 1e-9 ? " tw-even" : "") }));
      g.appendChild(sv("text", { x: x(t), y: H - bottom + 16, "text-anchor": "middle", "class": "tw-axis", text: t.toFixed(2) }));
    }
    g.appendChild(sv("text", { x: x(0.5) + 4, y: H - 2, "class": "tw-axis", text: "← coin flip" }));
    rows.forEach(function (r, i) {
      var y = top + i * rowH + rowH / 2;
      g.appendChild(sv("text", { x: labelW - 10, y: y + 4, "text-anchor": "end", "class": "tw-rowlabel", text: r.label }));
      g.appendChild(sv("rect", { x: x(r.lo), y: y - 7, width: Math.max(2, x(r.hi) - x(r.lo)), height: 14, rx: 4, "class": "tw-ci" }));
      r.runs.forEach(function (p, k) {
        var dot = sv("circle", { cx: x(p), cy: y, r: 4.5, "class": "tw-dot" + (p < 0.5 ? " tw-dot-flip" : "") });
        hoverable(dot, function () {
          return "<strong>" + esc(r.label) + "</strong><br>run " + (k + 1) + ": " + fmt(p) + (p < 0.5 ? " (this run went the other way)" : "");
        });
        g.appendChild(dot);
      });
      var m = sv("line", { x1: x(r.mean), x2: x(r.mean), y1: y - 9, y2: y + 9, "class": "tw-mean" });
      g.appendChild(m);
    });
    return g;
  }

  function reliability(root) {
    var rows = [];
    DATA.bracket.rounds.forEach(function (round) {
      round.matches.forEach(function (m) {
        var v = verdict(m);
        var short = { "Round of 16": "R16", "Quarterfinals": "QF", "Semifinals": "SF", "Final": "F" }[round.name] || round.name;
        rows.push({
          label: short + " · " + v.winner + " over " + v.loser,
          runs: m.runs.map(function (r) { return v.flip ? 1 - r : r; }),
          lo: v.flip ? 1 - m.hi : m.lo, hi: v.flip ? 1 - m.lo : m.hi, mean: v.p
        });
      });
    });
    root.appendChild(el("div", { "class": "tw-scroll" }, [strip(rows, { width: 680, labelW: 230 })]));
    root.appendChild(el("p", { "class": "tw-legend" }, [
      el("span", { "class": "tw-key tw-key-dot" }), "one run (" + DATA.wordings.length * 2 + " calls)  ",
      el("span", { "class": "tw-key tw-key-flip" }), "a run that went the other way  ",
      el("span", { "class": "tw-key tw-key-ci" }), "95% confidence interval  ",
      el("span", { "class": "tw-key tw-key-mean" }), "mean"
    ]));
  }

  // ---------- round-robin heatmap ----------

  function mix(a, b, t) {
    function h(s, i) { return parseInt(s.substr(1 + i * 2, 2), 16); }
    var out = "#";
    for (var i = 0; i < 3; i++) {
      var v = Math.round(h(a, i) + (h(b, i) - h(a, i)) * t);
      out += ("0" + v.toString(16)).slice(-2);
    }
    return out;
  }

  // Diverging: blue when the row survives more, red when it dies more, gray
  // at a coin flip. Saturates at ±0.06, the widest margin in the data.
  function divColor(p) {
    var t = Math.max(-1, Math.min(1, (p - 0.5) / 0.06));
    return t >= 0 ? mix("#f0efec", "#2a78d6", t) : mix("#f0efec", "#e34948", -t);
  }

  function heatmap(root) {
    var rr = DATA.round_robin;
    var order = rr.standings.map(function (s) { return s.name; });
    var rec = {};
    rr.standings.forEach(function (s) { rec[s.name] = s; });
    var look = {};
    rr.matches.forEach(function (m) {
      look[m.a.name + "|" + m.b.name] = { p: m.mean, lo: m.lo, hi: m.hi, runs: m.runs_for_a, n: m.runs.length };
      look[m.b.name + "|" + m.a.name] = { p: 1 - m.mean, lo: 1 - m.hi, hi: 1 - m.lo, runs: m.runs.length - m.runs_for_a, n: m.runs.length };
    });
    var cell = 30, labelW = 150, top = 92, N = order.length;
    var W = labelW + N * cell + 60, H = top + N * cell + 10;
    var g = sv("svg", { viewBox: "0 0 " + W + " " + H, "class": "tw-heat", role: "img", "aria-label": "Round-robin results: chance each row's programmer survives against each column's" });
    g.appendChild(sv("defs", {}, [sv("pattern", { id: "tw-hatch", width: 6, height: 6, patternUnits: "userSpaceOnUse", patternTransform: "rotate(45)" }, [
      sv("line", { x1: 0, y1: 0, x2: 0, y2: 6, "class": "tw-hatch-line" })
    ])]));
    order.forEach(function (name, c) {
      var cx = labelW + c * cell + cell / 2;
      g.appendChild(sv("text", { x: cx, y: top - 8, transform: "rotate(-55 " + cx + " " + (top - 8) + ")", "class": "tw-collabel", text: name }));
    });
    order.forEach(function (row, r) {
      var y = top + r * cell;
      var s = rec[row];
      g.appendChild(sv("text", { x: labelW - 8, y: y + cell / 2 + 4, "text-anchor": "end", "class": "tw-rowlabel", text: row + "  " + s.wins + "-" + s.losses }));
      order.forEach(function (col, c) {
        var x = labelW + c * cell;
        if (row === col) {
          g.appendChild(sv("rect", { x: x + 1, y: y + 1, width: cell - 2, height: cell - 2, rx: 3, "class": "tw-diag" }));
          return;
        }
        var d = look[row + "|" + col];
        var tossup = d.lo <= 0.5 && d.hi >= 0.5;
        var rect = sv("rect", { x: x + 1, y: y + 1, width: cell - 2, height: cell - 2, rx: 3, fill: divColor(d.p), "class": "tw-cell" });
        g.appendChild(rect);
        if (tossup) g.appendChild(sv("rect", { x: x + 1, y: y + 1, width: cell - 2, height: cell - 2, rx: 3, fill: "url(#tw-hatch)", "pointer-events": "none" }));
        hoverable(rect, function () {
          return "<strong>" + esc(row) + "</strong> vs " + esc(col) + "<br>" + esc(row) + " survives " + fmt(d.p) +
            " (95% CI " + fmt(d.lo) + "–" + fmt(d.hi) + ")<br>" + esc(row) + " won " + d.runs + "/" + d.n + " runs" +
            (tossup ? "<br><em>too close to call</em>" : "");
        });
      });
    });
    root.appendChild(el("div", { "class": "tw-scroll" }, [g]));
    var grad = el("span", { "class": "tw-grad" });
    root.appendChild(el("p", { "class": "tw-legend" }, [
      "row dies more ", grad, " row survives more   ",
      el("span", { "class": "tw-key tw-key-hatch" }), " too close to call (95% CI includes 0.5)"
    ]));
    var tossups = rr.matches.filter(function (m) { return m.lo <= 0.5 && m.hi >= 0.5; }).length;
    root.appendChild(el("p", { "class": "tw-note", text: "Rows are sorted by record. Hover or tab to a cell for its numbers. " + tossups + " of " + rr.matches.length + " pairings are too close to call." }));
  }

  // ---------- exchange: diorama + curves + the rate board ----------

  function curves(root) {
    var ex = DATA.exchange;
    var W = 640, H = 260, L = 46, R = 16, T = 14, B = 36;
    var maxN = ex.crowds[ex.crowds.length - 1];
    var x = function (n) { return L + ((n - 1) / (maxN - 1)) * (W - L - R); };
    var y = function (p) { return T + (1 - (p - 0.4) / 0.6) * (H - T - B); };
    var g = sv("svg", { viewBox: "0 0 " + W + " " + H, "class": "tw-curves", role: "img" });
    [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0].forEach(function (p) {
      g.appendChild(sv("line", { x1: L, x2: W - R, y1: y(p), y2: y(p), "class": "tw-grid" + (p === 0.5 ? " tw-even" : "") }));
      g.appendChild(sv("text", { x: L - 6, y: y(p) + 4, "text-anchor": "end", "class": "tw-axis", text: p.toFixed(1) }));
    });
    ex.crowds.forEach(function (n) {
      g.appendChild(sv("text", { x: x(n), y: H - B + 18, "text-anchor": "middle", "class": "tw-axis", text: String(n) }));
    });
    g.appendChild(sv("text", { x: (L + W - R) / 2, y: H - 4, "text-anchor": "middle", "class": "tw-axis", text: "programmers on the other track, against 1 " + ex.champion + " programmer" }));
    g.appendChild(sv("text", { x: W - R - 4, y: y(0.5) - 6, "text-anchor": "end", "class": "tw-axis", text: "coin flip" }));
    var lines = {};
    ex.rows.forEach(function (row) {
      var d = row.points.map(function (pt, i) { return (i ? "L" : "M") + x(pt.n).toFixed(1) + " " + y(pt.p).toFixed(1); }).join(" ");
      var path = sv("path", { d: d, "class": "tw-curve" });
      g.appendChild(path);
      lines[row.name] = path;
    });
    var hi = sv("g");
    g.appendChild(hi);
    root.appendChild(el("div", { "class": "tw-scroll" }, [g]));
    var label = el("p", { "class": "tw-note" });
    root.appendChild(label);

    return function highlight(lang) {
      var row = ex.rows.filter(function (r) { return r.name === lang.name; })[0];
      Object.keys(lines).forEach(function (k) { lines[k].classList.toggle("tw-curve-on", k === lang.name); });
      hi.innerHTML = "";
      if (!row) return;
      g.appendChild(lines[row.name]); // draw on top
      g.appendChild(hi);
      row.points.forEach(function (pt) {
        var c = sv("circle", { cx: x(pt.n), cy: y(pt.p), r: pt.n === lang.n ? 7 : 5, "class": "tw-pt" + (pt.n === lang.n ? " tw-pt-on" : "") });
        hoverable(c, function () {
          return "<strong>" + pt.n + " " + esc(row.name) + "</strong> vs 1 " + esc(ex.champion) + "<br>the " + pt.n + " survive " + fmt(pt.p) + " (95% CI " + fmt(pt.lo) + "–" + fmt(pt.hi) + ")";
        });
        hi.appendChild(c);
      });
      label.textContent = "Gray lines are the other " + (ex.rows.length - 1) + " languages. They sit almost on top of each other, which is the whole story: Jev counts heads.";
    };
  }

  var FLAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.+#";

  function flapText(node, text, delay) {
    var target = text.toUpperCase();
    if (REDUCED) { node.textContent = target; return; }
    var t0 = null, dur = 700;
    function step(ts) {
      if (t0 == null) t0 = ts + delay;
      var t = (ts - t0) / dur;
      if (t < 0) { requestAnimationFrame(step); return; }
      var settled = Math.floor(Math.max(0, Math.min(1, t)) * target.length);
      var s = target.slice(0, settled);
      for (var i = settled; i < target.length; i++) {
        s += target[i] === " " ? " " : FLAP[Math.floor(Math.random() * FLAP.length)];
      }
      node.textContent = s;
      if (t < 1) requestAnimationFrame(step);
      else node.textContent = target;
    }
    requestAnimationFrame(step);
  }

  function board(root) {
    var ex = DATA.exchange;
    var rows = ex.rows.slice().sort(function (a, b) { return (a.rate || 1e9) - (b.rate || 1e9); });
    var b = el("div", { "class": "tw-board", role: "table", "aria-label": "Exchange rates against 1 " + ex.champion + " programmer" });
    b.appendChild(el("div", { "class": "tw-board-head", role: "row" }, [
      el("span", { role: "columnheader", text: "TODAY'S RATES" }),
      el("span", { role: "columnheader", text: "1 " + ex.champion.toUpperCase() + " =" })
    ]));
    var cells = [];
    rows.forEach(function (r) {
      var name = el("span", { "class": "tw-flap", role: "cell", text: r.name.toUpperCase() });
      var rate = el("span", { "class": "tw-flap tw-rate", role: "cell", text: r.rate ? r.rate.toFixed(2) : "N/A" });
      b.appendChild(el("div", { "class": "tw-board-row", role: "row" }, [name, rate]));
      cells.push([name, r.name, rate, r.rate ? r.rate.toFixed(2) : "N/A"]);
    });
    root.appendChild(b);
    root.appendChild(el("p", { "class": "tw-note", text: "Each rate is where the curve above crosses a coin flip, drawn as a straight line between 1 and 2 programmers. Jev never saw 1.07 of anybody." }));
    var spun = false;
    function spin() {
      if (spun) return;
      spun = true;
      cells.forEach(function (c, i) { flapText(c[0], c[1], i * 70); flapText(c[2], c[3], i * 70 + 200); });
    }
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        if (es.some(function (e) { return e.isIntersecting; })) { spin(); io.disconnect(); }
      }, { threshold: 0.4 });
      io.observe(b);
    }
  }

  function exchange(root) {
    var highlight = null;
    var holder = el("div");
    root.appendChild(holder);
    var chart = el("div", { "class": "tw-chart" });
    root.appendChild(chart);
    highlight = curves(chart);
    diorama(holder, { mode: "crowd", onChange: function (g) { if (highlight) highlight(g); } });
  }

  // ---------- matchup cards (the custom questions) ----------

  function matchups(root) {
    var list = el("div", { "class": "tw-matchups" });
    DATA.matchups.forEach(function (m) {
      var aWon = m.mean >= 0.5;
      var same = m.a.name === m.b.name && m.a.n === m.b.n;
      function side(g, p, won) {
        return el("div", { "class": "tw-mside" + (won && !same ? " tw-win" : "") }, [
          el("div", { "class": "tw-mcount", text: phrase(g) }),
          el("div", { "class": "tw-dbar" }, [el("span", { style: "width:" + (p * 100).toFixed(1) + "%" })]),
          el("div", { "class": "tw-dnum", text: fmt(p) })
        ]);
      }
      list.appendChild(el("div", { "class": "tw-mcard" }, [
        side(m.a, m.mean, aWon),
        el("div", { "class": "tw-vs", text: same ? "control" : "vs" }),
        side(m.b, 1 - m.mean, !aWon)
      ]));
    });
    root.appendChild(list);
  }

  // ---------- boot ----------

  var WIDGETS = { diorama: function (r) { diorama(r, { mode: "pair" }); }, bracket: bracket, reliability: reliability, heatmap: heatmap, exchange: exchange, board: board, matchups: matchups };

  function boot() {
    document.querySelectorAll(".tw[data-widget]").forEach(function (root) {
      var make = WIDGETS[root.getAttribute("data-widget")];
      if (!make) return;
      root.innerHTML = "";
      try { make(root); }
      catch (e) {
        root.appendChild(el("p", { "class": "tw-note", text: "This widget failed to load. The numbers are in the text and in the GitHub repo." }));
        if (window.console) console.error(e);
      }
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
