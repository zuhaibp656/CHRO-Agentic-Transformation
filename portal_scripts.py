"""Interactive JavaScript & SVG engine for the CHRO Office Agentic Transformation Portal."""

PORTAL_JS = r"""
    const CATALOG = __EMBEDDED_CATALOG_JSON__;
    const META = CATALOG.metadata || {};
    const PILLARS = CATALOG.pillars || {};
    const AGENTS = CATALOG.agents || {};
    const VALUE_CHAINS = CATALOG.valueChains || {};
    const KEYNOTE_SLIDES_V1 = CATALOG.keynoteSlides || [];
    const KEYNOTE_SLIDES_V2 = CATALOG.keynoteSlidesV2 || [];
    const KEYNOTE_SLIDES = KEYNOTE_SLIDES_V1;

    let selectedPillarId = null;
    let slideDeckVersion = KEYNOTE_SLIDES_V2.length ? 'v2' : 'v1'; // 'v2' (Stage Keynote) | 'v1' (Architecture Deck)
    let currentSlideIdx = 0;
    let slideViewMode = 'presenter'; // 'presenter' | 'grid'
    let showSpeakerNotes = true;
    let currentMatrixFilter = 'ALL';
    let currentMindMapPillarId = Object.keys(PILLARS)[0] || 'requisition_screening';
    let currentMindMapAgentId = null;
    const selectedVcStageByVc = {};

    function getActiveKeynoteSlides() {
      return (slideDeckVersion === 'v2' && KEYNOTE_SLIDES_V2.length) ? KEYNOTE_SLIDES_V2 : KEYNOTE_SLIDES_V1;
    }

    function esc(str) {
      return String(str == null ? '' : str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function tierBadgeHtml(tier) {
      const t = String(tier || 'No-Code');
      const cls = t === 'No-Code' ? 'tier-nocode' : (t === 'Low-Code' ? 'tier-lowcode' : 'tier-highcode');
      const label = t === 'No-Code'
        ? 'No-Code · Gemini Enterprise'
        : (t === 'Low-Code' ? 'Low-Code · Connector' : 'High-Code · Google ADK + MCP');
      return `<span class="build-tier-badge ${cls}">${esc(label)}</span>`;
    }

    /* =========================================================================
       1. THEME TOGGLE (ALWAYS INITIALIZES IN LIGHT THEME BY DEFAULT)
       ========================================================================= */
    function initThemeDefaultLight() {
      document.documentElement.setAttribute('data-theme', 'light');
      updateThemeToggleLabel('light');
    }

    function updateThemeToggleLabel(theme) {
      const btn = document.getElementById('themeToggleBtn');
      if (!btn) return;
      btn.innerHTML = theme === 'dark'
        ? '<span>☀️</span><span>Light Theme</span>'
        : '<span>🌙</span><span>Dark Theme</span>';
    }

    function togglePortalTheme() {
      const cur = document.documentElement.getAttribute('data-theme') || 'light';
      const next = cur === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', next);
      updateThemeToggleLabel(next);
    }

    /* =========================================================================
       2. KINETIC CHRO NETWORK HERO CANVAS
       ========================================================================= */
    function initHeroHrCanvas() {
      const canvas = document.getElementById('heroHrCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      const palette = ['#4285f4', '#ea4335', '#fbbc04', '#34a853', '#0097a7', '#7e57c2'];
      let w = 0, h = 0;
      const nodes = [];
      for (let i = 0; i < 34; i++) {
        nodes.push({
          x: Math.random(),
          y: Math.random(),
          vx: (Math.random() - 0.5) * 0.00045,
          vy: (Math.random() - 0.5) * 0.00045,
          r: 2.5 + (i % 4) * 1.1,
          c: palette[i % palette.length]
        });
      }

      function resize() {
        const rect = canvas.parentElement ? canvas.parentElement.getBoundingClientRect() : { width: 1200, height: 600 };
        w = canvas.width = Math.max(320, rect.width);
        h = canvas.height = Math.max(320, rect.height);
      }
      resize();
      window.addEventListener('resize', resize);

      function draw() {
        const isDark = (document.documentElement.getAttribute('data-theme') || 'light') === 'dark';
        ctx.clearRect(0, 0, w, h);
        for (const n of nodes) {
          n.x += n.vx;
          n.y += n.vy;
          if (n.x < 0.03 || n.x > 0.97) n.vx *= -1;
          if (n.y < 0.05 || n.y > 0.95) n.vy *= -1;
        }
        for (let i = 0; i < nodes.length; i++) {
          for (let j = i + 1; j < nodes.length; j++) {
            const dx = (nodes[i].x - nodes[j].x) * w;
            const dy = (nodes[i].y - nodes[j].y) * h;
            const dist = Math.hypot(dx, dy);
            if (dist < 175) {
              const alpha = (1 - dist / 175) * (isDark ? 0.22 : 0.14);
              ctx.strokeStyle = `rgba(66, 133, 244, ${alpha.toFixed(3)})`;
              ctx.lineWidth = 1.1;
              ctx.beginPath();
              ctx.moveTo(nodes[i].x * w, nodes[i].y * h);
              ctx.lineTo(nodes[j].x * w, nodes[j].y * h);
              ctx.stroke();
            }
          }
        }
        for (const n of nodes) {
          ctx.fillStyle = n.c;
          ctx.globalAlpha = isDark ? 0.55 : 0.42;
          ctx.beginPath();
          ctx.arc(n.x * w, n.y * h, n.r, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.globalAlpha = 1;
        requestAnimationFrame(draw);
      }
      requestAnimationFrame(draw);
    }

    /* =========================================================================
       3. BESPOKE INLINE VECTOR STAGE ARTWORK FOR THE 6 HR PILLARS
       ========================================================================= */
    function renderHrSvg(type, color) {
      const c = color || '#4285f4';
      if (type === 'talent_magnet') {
        return `<svg viewBox="0 0 280 110" aria-hidden="true">
          <circle cx="48" cy="55" r="26" fill="${c}18" stroke="${c}" stroke-width="1.5" stroke-dasharray="4 3"/>
          <circle cx="48" cy="55" r="10" fill="${c}"/>
          <path d="M76 55 C110 25, 130 25, 165 40" fill="none" stroke="${c}" stroke-width="2" stroke-dasharray="6 4"/>
          <path d="M76 55 C110 85, 130 85, 165 70" fill="none" stroke="#34a853" stroke-width="2" stroke-dasharray="6 4"/>
          <rect x="166" y="24" width="94" height="26" rx="8" fill="#ffffff" stroke="${c}" stroke-width="1.5"/>
          <text x="213" y="41" text-anchor="middle" font-size="10" font-weight="700" fill="#202124">Skill Graph Match</text>
          <rect x="166" y="60" width="94" height="26" rx="8" fill="#ceead6" stroke="#34a853" stroke-width="1.5"/>
          <text x="213" y="77" text-anchor="middle" font-size="10" font-weight="700" fill="#137333">DPDP Blind Pass</text>
        </svg>`;
      }
      if (type === 'interview_clock') {
        return `<svg viewBox="0 0 280 110" aria-hidden="true">
          <rect x="18" y="30" width="84" height="50" rx="10" fill="#fce8e6" stroke="#ea4335" stroke-width="1.5"/>
          <text x="60" y="51" text-anchor="middle" font-size="10" font-weight="700" fill="#c5221f">LEGACY</text>
          <text x="60" y="67" text-anchor="middle" font-size="13" font-weight="800" fill="#202124">4 Days</text>
          <path d="M108 55 L162 55" stroke="${c}" stroke-width="2.5" stroke-dasharray="5 3"/>
          <polygon points="160,49 170,55 160,61" fill="${c}"/>
          <rect x="174" y="24" width="90" height="62" rx="12" fill="#e8f0fe" stroke="#185abc" stroke-width="1.8"/>
          <text x="219" y="46" text-anchor="middle" font-size="10" font-weight="800" fill="#185abc">ZERO-TOUCH</text>
          <text x="219" y="66" text-anchor="middle" font-size="15" font-weight="800" fill="#202124">&lt; 1 Hour</text>
        </svg>`;
      }
      if (type === 'dayone_hub') {
        return `<svg viewBox="0 0 280 110" aria-hidden="true">
          <rect x="16" y="26" width="56" height="56" rx="10" fill="#e0f7fa" stroke="${c}" stroke-width="1.5"/>
          <text x="44" y="50" text-anchor="middle" font-size="10" font-weight="800" fill="#007b83">DAY 1</text>
          <text x="44" y="66" text-anchor="middle" font-size="9" font-weight="600" fill="#202124">Laptop+ID</text>
          <line x1="72" y1="54" x2="94" y2="54" stroke="${c}" stroke-width="2"/>
          <rect x="94" y="26" width="54" height="56" rx="10" fill="#ffffff" stroke="${c}" stroke-width="1.5"/>
          <text x="121" y="50" text-anchor="middle" font-size="10" font-weight="800" fill="${c}">DAY 30</text>
          <text x="121" y="66" text-anchor="middle" font-size="9" font-weight="600" fill="#202124">Buddy</text>
          <line x1="148" y1="54" x2="170" y2="54" stroke="${c}" stroke-width="2"/>
          <rect x="170" y="26" width="92" height="56" rx="10" fill="#ceead6" stroke="#34a853" stroke-width="1.5"/>
          <text x="216" y="49" text-anchor="middle" font-size="10" font-weight="800" fill="#137333">DAY 60 → 90</text>
          <text x="216" y="66" text-anchor="middle" font-size="9.5" font-weight="700" fill="#202124">&gt;95% Ready</text>
        </svg>`;
      }
      if (type === 'career_saathi') {
        return `<svg viewBox="0 0 280 110" aria-hidden="true">
          <path d="M26 84 C70 76, 120 56, 165 44 C205 34, 228 24, 256 18" fill="none" stroke="${c}" stroke-width="3"/>
          <circle cx="42" cy="80" r="7" fill="#ffffff" stroke="${c}" stroke-width="2"/>
          <text x="42" y="98" text-anchor="middle" font-size="9.5" font-weight="700" fill="#5f6368">Retail RM</text>
          <circle cx="145" cy="50" r="8" fill="#ceead6" stroke="${c}" stroke-width="2"/>
          <text x="145" y="72" text-anchor="middle" font-size="9.5" font-weight="700" fill="#137333">3-Min Sim</text>
          <circle cx="242" cy="22" r="9" fill="${c}"/>
          <text x="218" y="44" text-anchor="middle" font-size="9.5" font-weight="800" fill="#202124">Phygital Leader</text>
        </svg>`;
      }
      if (type === 'concierge_pulse') {
        return `<svg viewBox="0 0 280 110" aria-hidden="true">
          <rect x="18" y="20" width="114" height="70" rx="12" fill="#fff2cc" stroke="#e37400" stroke-width="1.5"/>
          <text x="75" y="46" text-anchor="middle" font-size="18" font-weight="800" fill="#e37400">~70%</text>
          <text x="75" y="65" text-anchor="middle" font-size="9.5" font-weight="700" fill="#202124">Zero-Touch Resolve</text>
          <text x="75" y="79" text-anchor="middle" font-size="8.5" fill="#5f6368">HCM + ITSM MCP</text>
          <rect x="148" y="20" width="114" height="70" rx="12" fill="#fce8e6" stroke="#ea4335" stroke-width="1.5"/>
          <text x="205" y="45" text-anchor="middle" font-size="11" font-weight="800" fill="#c5221f">EMPLOYEE PULSE</text>
          <text x="205" y="64" text-anchor="middle" font-size="9.5" font-weight="700" fill="#202124">30% Care + Burnout</text>
          <text x="205" y="78" text-anchor="middle" font-size="8.5" fill="#5f6368">k-Anonymity (N≥10)</text>
        </svg>`;
      }
      return `<svg viewBox="0 0 280 110" aria-hidden="true">
        <rect x="20" y="22" width="108" height="66" rx="12" fill="#e6e7fb" stroke="${c}" stroke-width="1.5"/>
        <text x="74" y="46" text-anchor="middle" font-size="10.5" font-weight="800" fill="${c}">WORKFORCE SIM</text>
        <text x="74" y="64" text-anchor="middle" font-size="10" font-weight="700" fill="#202124">Build vs. Upskill</text>
        <text x="74" y="78" text-anchor="middle" font-size="8.5" fill="#5f6368">GCC Macro Signals</text>
        <rect x="148" y="22" width="112" height="66" rx="12" fill="#ffffff" stroke="#185abc" stroke-width="1.5"/>
        <text x="204" y="48" text-anchor="middle" font-size="14" font-weight="800" fill="#185abc">&lt;1%–2%</text>
        <text x="204" y="65" text-anchor="middle" font-size="9.5" font-weight="700" fill="#202124">Pay Gap Variance</text>
        <text x="204" y="79" text-anchor="middle" font-size="8.5" fill="#5f6368">Cloud DLP + HITL</text>
      </svg>`;
    }

    /* =========================================================================
       4. NAVIGATION & ROUTER
       ========================================================================= */
    function showActivePage(pageId) {
      document.querySelectorAll('.page-view').forEach(el => {
        el.classList.toggle('active', el.id === pageId);
      });
      document.querySelectorAll('.nav-pill-btn[data-nav]').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-nav') === pageId);
      });
      const menu = document.getElementById('navQuickMenu');
      if (menu) menu.classList.remove('open');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function toggleQuickJumpMenu(ev) {
      if (ev) ev.stopPropagation();
      const menu = document.getElementById('navQuickMenu');
      if (menu) menu.classList.toggle('open');
    }

    function populateQuickJumpMenu() {
      const menu = document.getElementById('navQuickMenu');
      if (!menu) return;
      const pHtml = Object.values(PILLARS).map(p =>
        `<button type="button" class="nav-quick-item" onclick="jumpToPillar('${p.id}')">
          <span><strong style="color:${p.color};">${p.vNum}</strong> · ${esc(p.shortName)}</span>
          <span style="font-size:11px; color:var(--text-muted);">${p.agentIds.length} Agents</span>
        </button>`
      ).join('');
      const aHtml = Object.values(AGENTS).map(a =>
        `<button type="button" class="nav-quick-item" onclick="openAgentPage('${a.id}', true)">
          <span>${esc(a.num)} · ${esc(a.name)}</span>
          ${tierBadgeHtml(a.buildTier)}
        </button>`
      ).join('');
      menu.innerHTML = `
        <div class="nav-quick-group-title">6 HR Pillars (Slide 17 Framework)</div>
        ${pHtml}
        <div class="nav-quick-group-title">14 Process-Led AI Agents</div>
        ${aHtml}
      `;
    }

    function goToHome(pushHash = true) {
      if (pushHash) history.pushState({ page: 'home' }, '', '#top');
      showActivePage('pageHome');
    }

    function goToOrgChart() {
      history.pushState({ page: 'home' }, '', '#org');
      showActivePage('pageHome');
      setTimeout(() => {
        const el = document.getElementById('orgChartSection');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 40);
    }

    function scrollToProcessJourneys() {
      history.pushState({ page: 'home' }, '', '#processes');
      showActivePage('pageHome');
      setTimeout(() => {
        const el = document.getElementById('processJourneysSection');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 40);
    }

    function jumpToPillar(pillarId) {
      history.pushState({ page: 'home', pillarId }, '', `#pillar/${pillarId}`);
      showActivePage('pageHome');
      selectedPillarId = pillarId;
      switchVerticalTab(pillarId, true);
    }

    /* =========================================================================
       5. HOME PAGE RENDERING: HR PARADOX, 6 PILLARS TREE, SHOWCASE, E2E FLOWS
       ========================================================================= */
    function renderHomeSections() {
      renderParadoxBand();
      renderVerticalTabsBar();
      renderOrgChart();
      renderPillarShowcaseDrawer();
      renderValueChainEntryCards();
      populateQuickJumpMenu();
    }

    function renderParadoxBand() {
      const el = document.getElementById('hrParadoxBand');
      if (!el || !META.hrParadox) return;
      const hp = META.hrParadox;
      const segs = [...hp.operationalBreakdown, ...hp.strategicBreakdown];
      el.innerHTML = `
        <div class="paradox-panel">
          <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px;">
            <div>
              <span class="build-tier-badge" style="background:var(--g-red-bg); color:#c5221f; border-color:rgba(234,67,53,0.4);">KEYNOTE CORE THESIS · GOOGLE CLOUD HR TRANSFORMATION FRAMEWORK</span>
              <h2 style="font-family:var(--font-display); font-size:24px; font-weight:800; margin:10px 0 4px;">${esc(hp.headline)}</h2>
              <p style="margin:0; color:var(--text-muted); font-size:14.5px;">${esc(hp.subhead)}</p>
            </div>
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              <div style="padding:10px 16px; border-radius:14px; background:var(--g-red-bg); border:1px solid rgba(234,67,53,0.35);">
                <div style="font-family:var(--font-display); font-size:22px; font-weight:800; color:#c5221f;">~${hp.operationalTaxPct}%</div>
                <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary);">Coordination Tax</div>
              </div>
              <div style="padding:10px 16px; border-radius:14px; background:var(--g-green-bg); border:1px solid rgba(52,168,83,0.4);">
                <div style="font-family:var(--font-display); font-size:22px; font-weight:800; color:#137333;">~${hp.strategicWorkPct}%</div>
                <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary);">Strategic People Impact</div>
              </div>
            </div>
          </div>

          <div class="paradox-bar-wrap" title="HR Time Allocation Benchmark">
            ${segs.map(s => `<div class="paradox-seg" style="width:${s.pct}%; background:${s.color};">${s.pct}%</div>`).join('')}
          </div>

          <div class="paradox-grid">
            <div class="paradox-col-card" style="background:var(--g-red-bg); border-color:rgba(234,67,53,0.35);">
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; color:#c5221f; margin-bottom:8px;">Where 75% Administrative Time Goes Today</div>
              <div style="display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px;">
                ${hp.operationalBreakdown.map(b => `
                  <div style="background:var(--bg-surface); padding:8px 10px; border-radius:10px; border-left:4px solid ${b.color};">
                    <strong style="font-family:var(--font-display); color:${b.color};">${b.pct}%</strong>
                    <div style="font-size:12px; color:var(--text-secondary); font-weight:600;">${esc(b.label)}</div>
                  </div>
                `).join('')}
              </div>
            </div>
            <div class="paradox-col-card" style="background:var(--g-green-bg); border-color:rgba(52,168,83,0.35);">
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; color:#137333; margin-bottom:8px;">4 Value Levers Expanding Strategic 25% ("Orchestrator")</div>
              <div style="display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px;">
                ${(META.fourValueLevers || []).map(v => `
                  <div style="background:var(--bg-surface); padding:8px 10px; border-radius:10px; border-left:4px solid ${v.color};">
                    <strong style="font-family:var(--font-display); font-size:12.5px; color:${v.color};">${esc(v.name)}</strong>
                    <div style="font-size:11.5px; color:var(--text-muted);">${esc(v.title)}</div>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
          <div style="font-size:11.5px; color:var(--text-muted); margin-top:12px;">${esc(hp.sourceNote)}</div>
        </div>
      `;
    }

    function renderVerticalTabsBar() {
      const bar = document.getElementById('verticalTabsNavBar');
      if (!bar) return;
      const allBtn = `
        <button type="button" class="v-tab-btn ${selectedPillarId === null ? 'active' : ''}" data-vtab="all" onclick="switchVerticalTab('all')" style="--v-accent:#4285f4;">
          <span class="v-tab-num">ALL 6 PILLARS</span>
          <span class="v-tab-title">Office of the CHRO</span>
          <span class="v-tab-tag">14 Process Agents</span>
        </button>
      `;
      const pBtns = Object.values(PILLARS).map(p => {
        const isActive = selectedPillarId === p.id;
        return `
          <button type="button" class="v-tab-btn ${isActive ? 'active' : ''}" data-vtab="${p.id}" onclick="switchVerticalTab('${p.id}')" style="--v-accent:${p.color};">
            <span class="v-tab-num">${esc(p.vNum)} · SLIDE 17</span>
            <span class="v-tab-title">${esc(p.shortName)}</span>
            <span class="v-tab-tag">${p.agentIds.length} AI Agents</span>
          </button>
        `;
      }).join('');
      bar.innerHTML = allBtn + pBtns;
    }

    function switchVerticalTab(vId, scrollToDrawer = false) {
      selectedPillarId = (vId === 'all') ? null : (selectedPillarId === vId && !scrollToDrawer ? null : vId);
      renderVerticalTabsBar();
      renderOrgChart();
      renderPillarShowcaseDrawer();
      if (selectedPillarId) {
        setTimeout(() => {
          const box = document.getElementById('deptShowcaseContainer');
          if (box) box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 60);
      }
    }

    function selectPillar(pillarId) {
      selectedPillarId = (selectedPillarId === pillarId) ? null : pillarId;
      renderVerticalTabsBar();
      renderOrgChart();
      renderPillarShowcaseDrawer();
      if (selectedPillarId) {
        setTimeout(() => {
          const box = document.getElementById('deptShowcaseContainer');
          if (box) box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 60);
      }
    }

    function renderOrgChart() {
      const row = document.getElementById('deptRowContainer');
      if (!row) return;
      row.innerHTML = Object.values(PILLARS).map(p => {
        const isActive = p.id === selectedPillarId;
        const agList = p.agentIds.map(id => AGENTS[id]).filter(Boolean);
        const noLow = agList.filter(a => a.buildTier === 'No-Code' || a.buildTier === 'Low-Code').length;
        const high = agList.length - noLow;
        return `
          <div class="dept-node cs-pillar-card ${isActive ? 'active' : ''}" style="--dept-accent:${p.color};" onclick="selectPillar('${p.id}')">
            <div>
              <div style="display:inline-flex; align-items:center; gap:6px; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:800; letter-spacing:0.05em; background:${p.softBg || '#E8F0FE'}; color:${p.color}; border:1px solid #d2e3fc; margin-bottom:10px;">
                <span>${esc(p.apqcBadge)}</span>
              </div>
              <div class="dept-node-title">${esc(p.name)}</div>
              <div class="dept-node-sub">${esc(p.subtitle)}</div>
            </div>
            <div class="dept-anim-stage">
              ${renderHrSvg(p.watermarkType, p.color)}
              <span class="dept-anim-meta">${agList.length} Agents · ${noLow} No/Low-Code · ${high} ADK</span>
              <span class="dept-anim-cta">${isActive ? 'Hide Agents ↑' : 'View Agents →'}</span>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderPillarShowcaseDrawer() {
      const container = document.getElementById('deptShowcaseContainer');
      if (!container) return;
      if (!selectedPillarId || !PILLARS[selectedPillarId]) {
        container.innerHTML = `
          <div style="margin-top:20px; padding:14px 20px; border-radius:14px; background:var(--bg-surface); border:1px dashed var(--border-strong); text-align:center; color:var(--text-muted); font-size:13.5px;">
            👆 Click any of the <strong>6 HR Function Pillars</strong> above (or select a tab) to view and open its AI agents directly.
          </div>
        `;
        return;
      }

      const p = PILLARS[selectedPillarId];
      const pAgents = p.agentIds.map(id => AGENTS[id]).filter(Boolean);
      const slideMatch = KEYNOTE_SLIDES.findIndex(s => s.pillarId === p.id);

      const stageLine = (p.processStages || []).map(s => esc(s.name)).join(' &rarr; ');
      container.innerHTML = `
        <div class="dept-showcase-box simple-drawer-box" style="--dept-accent:${p.color}; padding:22px 24px;">
          <div class="showcase-header" style="padding-bottom:14px; margin-bottom:16px;">
            <div>
              <div class="showcase-dept-name">
                <span style="width:12px; height:12px; border-radius:50%; background:${p.color}; display:inline-block;"></span>
                <span>${esc(p.name)}</span>
                <span class="drawer-count-pill" style="background:${p.softBg || '#E8F0FE'}; color:${p.color};">${pAgents.length} AI Agents</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-muted); margin-top:4px;">${stageLine}</div>
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:8px;">
              ${slideMatch >= 0 ? `<button type="button" class="switch-pill" onclick="openSlidesPage(${slideMatch}, true)">📊 Keynote Slide &rarr;</button>` : ''}
              <button type="button" class="switch-pill" onclick="openValueChainPage('${p.vcId}', true)">${esc(p.vcLabel)}</button>
              <button type="button" class="switch-pill" onclick="selectPillar('${p.id}')">&#10005; Close</button>
            </div>
          </div>

          <div class="agent-cards-grid agent-cards-simple">
            ${pAgents.map(ag => {
              const shortMetric = String(ag.outcomeBadge || '').split('·')[0].trim();
              const cleanTitle = ag.simpleName || ag.name;
              return `
              <div class="agent-card agent-card-simple" style="--dept-accent:${p.color};" onclick="openAgentPage('${ag.id}', true)">
                <div class="agent-card-simple-top">
                  <span class="agent-num-chip" style="color:${p.color}; background:${p.softBg || '#E8F0FE'};">#${esc(ag.num)}</span>
                  ${tierBadgeHtml(ag.buildTier)}
                </div>
                <div class="agent-card-simple-title">${esc(cleanTitle)}</div>
                <div class="agent-card-simple-foot">
                  <span class="agent-outcome-mini">${esc(shortMetric)}</span>
                  <span class="agent-open-link">Open Agent &rarr;</span>
                </div>
              </div>`;
            }).join('')}
          </div>
        </div>
      `;
    }

    function renderValueChainEntryCards() {
      const container = document.getElementById('valueChainEntryContainer');
      if (!container) return;
      container.innerHTML = Object.values(VALUE_CHAINS).map(vc => `
        <div class="vc-entry-card" style="--vc-accent:${vc.color};" onclick="openValueChainPage('${vc.id}', true)">
          <div>
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
              <span style="font-size:11px; font-weight:800; padding:4px 10px; border-radius:999px; background:${vc.color}18; color:${vc.color}; border:1px solid ${vc.color}45;">🔗 ${esc(vc.flowBadge)}</span>
              <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; padding:4px 10px; border-radius:8px; background:${vc.color}18; color:${vc.color};">${esc(vc.headlineStat)}</span>
            </div>
            <div class="dept-node-title" style="font-size:21px;">${esc(vc.shortTitle)}</div>
            <div style="font-size:13.5px; color:var(--text-secondary); margin-bottom:10px;">${esc(vc.cardSubtitle)}</div>
            <div class="vc-mini-pipeline">
              ${vc.stages.map((st, idx) => `
                <span class="vc-mini-stage-pill"><span class="st-idx">0${idx + 1}</span><span>${esc(st.name)}</span></span>
                ${idx < vc.stages.length - 1 ? '<span style="color:var(--text-muted); font-weight:800;">&rarr;</span>' : ''}
              `).join('')}
            </div>
          </div>
          <div style="display:flex; align-items:center; justify-content:space-between; padding-top:10px; border-top:1px solid var(--border-subtle); font-size:12.5px; font-weight:700; color:var(--text-muted);">
            <span>${esc(vc.cardFooterLeft)}</span>
            <span style="color:${vc.color}; font-weight:800;">Open Interactive Flow &rarr;</span>
          </div>
        </div>
      `).join('');
    }

    /* =========================================================================
       6. AGENT DEEP-DIVE STUDIO (WITH BRANCHING ARCHITECTURE SVG)
       ========================================================================= */
    function renderBranchingAgentSvg(ag) {
      const arch = ag.architectureNodes || {};
      const specs = arch.specialists || [];
      const conns = arch.connectors || [];
      const tierCol = ag.buildTier === 'No-Code' ? '#34a853' : (ag.buildTier === 'Low-Code' ? '#4285f4' : '#7e57c2');
      return `
        <svg viewBox="0 0 980 270" style="width:100%; height:auto; display:block;" role="img" aria-label="${esc(ag.name)} Multi-Agent Architecture">
          <defs>
            <linearGradient id="agFlowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="${ag.pillarColor}"/>
              <stop offset="100%" stop-color="${tierCol}"/>
            </linearGradient>
          </defs>
          <!-- Connector Curves -->
          <path d="M210,135 C255,135 255,54 310,54 M210,135 L310,135 M210,135 C255,135 255,216 310,216" fill="none" stroke="url(#agFlowGrad)" stroke-width="2.4" stroke-dasharray="6 4"/>
          <path d="M590,54 C635,54 635,54 680,54 M590,135 L680,135 M590,216 L680,216" fill="none" stroke="#0097a7" stroke-width="2.2" stroke-dasharray="6 4"/>

          <!-- Orchestrator Root -->
          <rect x="16" y="72" width="194" height="126" rx="16" fill="#e8f0fe" stroke="${ag.pillarColor}" stroke-width="2.2"/>
          <text x="113" y="98" text-anchor="middle" font-size="10.5" font-weight="800" fill="${ag.pillarColor}">PROCESS ORCHESTRATOR</text>
          <text x="113" y="124" text-anchor="middle" font-size="12.5" font-weight="800" fill="#202124">${esc((arch.orchestrator || ag.name).slice(0, 26))}</text>
          <rect x="44" y="142" width="138" height="26" rx="13" fill="${tierCol}"/>
          <text x="113" y="159" text-anchor="middle" font-size="10.5" font-weight="800" fill="#ffffff">${esc(ag.buildTier.toUpperCase())}</text>

          <!-- 3 Specialist Sub-Agents / Modules -->
          ${[0, 1, 2].map(i => {
            const y = 24 + i * 81;
            const title = specs[i] || 'Reasoning Module';
            const tool = ag.mcpTools[i] || 'Grounded Tool';
            return `
              <rect x="310" y="${y}" width="280" height="60" rx="12" fill="#ffffff" stroke="${tierCol}" stroke-width="1.6"/>
              <text x="326" y="${y + 24}" font-size="12" font-weight="800" fill="#202124">${esc(title)}</text>
              <text x="326" y="${y + 44}" font-size="10.5" font-weight="600" fill="#5f6368">${esc(tool)}</text>
            `;
          }).join('')}

          <!-- 3 Enterprise Systems / Guardrails -->
          ${[0, 1, 2].map(i => {
            const y = 24 + i * 81;
            const conn = conns[i] || 'Enterprise System';
            return `
              <rect x="680" y="${y}" width="280" height="60" rx="12" fill="#f8f9fa" stroke="#d2e3fc" stroke-width="1.6"/>
              <text x="696" y="${y + 24}" font-size="10" font-weight="800" fill="#0097a7">CONNECTOR / SYSTEM 0${i + 1}</text>
              <text x="696" y="${y + 45}" font-size="12" font-weight="700" fill="#202124">${esc(conn)}</text>
            `;
          }).join('')}
        </svg>
      `;
    }

    function renderAgentRuntimeBlueprint(ag) {
      const arch = ag.architectureNodes || {};
      const hw = ag.howItWorks || {};
      const specs = arch.specialists || [];
      const conns = arch.connectors || [];
      const isNoCode = ag.buildTier === 'No-Code';
      const isLowCode = ag.buildTier === 'Low-Code';
      const tierModeLabel = isNoCode
        ? 'Studio Configuration'
        : (isLowCode ? 'Hybrid Studio + Connectors' : 'Google ADK + FastMCP Orchestrator');
      const primaryPersona = (ag.personasServed || ['HR Specialist'])[0];
      const guardrailSummary = arch.guardrail || ag.guardrails;

      const triggerText = hw.trigger || (`Triggered by ${primaryPersona} when executing ${ag.simpleName || ag.name}`);
      const inputsList = Array.isArray(hw.inputs) && hw.inputs.length
        ? hw.inputs
        : [`${primaryPersona} request payload`, ...((ag.systems || []).slice(0, 2).map(s => `Policy & employee context from ${s}`))];
      const stepsList = Array.isArray(hw.steps) && hw.steps.length
        ? hw.steps
        : specs.map((sp, i) => ({ title: `Stage 0${i + 1}`, detail: sp }));
      const readsList = Array.isArray(hw.readsFrom) && hw.readsFrom.length ? hw.readsFrom : conns;
      const writesList = Array.isArray(hw.writesTo) && hw.writesTo.length ? hw.writesTo : ['HR Operations Audit Log (Immutable Trail)'];
      const outputsList = Array.isArray(hw.outputs) && hw.outputs.length
        ? hw.outputs
        : [String(ag.outcomeBadge || '').split('·')[0].trim() || ag.simpleName || ag.name];
      const humanGate = hw.humanCheckpoint || guardrailSummary;

      const hasExample = Boolean(hw.exampleBefore && hw.exampleAfter);

      return `
        <div class="hw-trigger-bar" role="note" aria-label="Agent Trigger">
          <div class="hw-trigger-badge">⚡ TRIGGERED WHEN</div>
          <div class="hw-trigger-text">${esc(triggerText)}</div>
          <div class="hw-tier-tag">${esc(ag.buildTier)} · ${esc(tierModeLabel)}</div>
        </div>

        <div class="arch-pipeline hw-pipeline" role="region" aria-label="${esc(ag.name)} End-to-End Agent Workflow">
          <div class="arch-stage-card arch-stage-intake hw-stage-card">
            <div class="arch-stage-kicker">1. WHAT IT TAKES</div>
            <div class="arch-stage-title">Inputs &amp; Privacy Check</div>
            <div class="arch-node-pill">👤 ${esc(primaryPersona)}</div>
            <ul class="hw-input-list">
              ${inputsList.map(item => `<li><span class="hw-bullet-dot"></span><span>${esc(item)}</span></li>`).join('')}
            </ul>
            <div class="hw-mini-shield">🔒 Masks sensitive Personal Identifiable Information (PII) via Model Armor before reasoning.</div>
          </div>

          <div class="arch-flow-arrow" aria-hidden="true"><span>&rarr;</span></div>

          <div class="arch-stage-card arch-stage-brain hw-stage-card">
            <div class="arch-stage-kicker">2. WHAT IT DOES (STEP-BY-STEP)</div>
            <div class="arch-stage-title">${esc(arch.orchestrator || ag.simpleName || ag.name)}</div>
            <div class="hw-steps-stack">
              ${stepsList.map((st, idx) => `
                <div class="hw-step-card">
                  <div class="hw-step-num">0${idx + 1}</div>
                  <div class="hw-step-body">
                    <div class="hw-step-title">${esc(st.title || ('Step ' + (idx + 1)))}</div>
                    <div class="hw-step-detail">${esc(st.detail || '')}</div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="arch-flow-arrow" aria-hidden="true"><span>&rarr;</span></div>

          <div class="arch-stage-card arch-stage-tools hw-stage-card">
            <div class="arch-stage-kicker">3. SYSTEMS CONNECTED</div>
            <div class="arch-stage-title">Reads vs. Updates</div>
            <div class="hw-io-split">
              <div class="hw-io-group">
                <div class="hw-io-label hw-io-read-label">📖 READS FROM (Read-Only Context)</div>
                <div class="hw-chip-group">
                  ${readsList.map(r => `<span class="hw-read-chip">${esc(r)}</span>`).join('')}
                </div>
              </div>
              <div class="hw-io-group">
                <div class="hw-io-label hw-io-write-label">✍️ UPDATES / NOTIFIES</div>
                <div class="hw-chip-group">
                  ${writesList.map(w => `<span class="hw-write-chip">${esc(w)}</span>`).join('')}
                </div>
              </div>
            </div>
          </div>

          <div class="arch-flow-arrow" aria-hidden="true"><span>&rarr;</span></div>

          <div class="arch-stage-card arch-stage-outcome hw-stage-card">
            <div class="arch-stage-kicker">4. WHAT IT PRODUCES</div>
            <div class="arch-stage-title">Outputs &amp; Human Sign-Off</div>
            <ul class="hw-output-list">
              ${outputsList.map(out => `<li><span class="hw-check-icon">✓</span><span>${esc(out)}</span></li>`).join('')}
            </ul>
            <div class="hw-human-box">
              <div class="hw-human-title">🛡️ Human-in-the-Loop (HITL) Sign-Off</div>
              <div class="hw-human-text">${esc(humanGate)}</div>
            </div>
          </div>
        </div>

        ${hasExample ? `
          <div class="hw-before-after-strip" role="region" aria-label="Concrete Before and After Example">
            <div class="hw-ba-col hw-ba-before">
              <div class="hw-ba-kicker">BEFORE AGENT (RAW INPUT)</div>
              <div class="hw-ba-text">${esc(hw.exampleBefore)}</div>
            </div>
            <div class="hw-ba-arrow" aria-hidden="true"><span>⚡</span></div>
            <div class="hw-ba-col hw-ba-after">
              <div class="hw-ba-kicker">AFTER AGENT (VERIFIED OUTPUT)</div>
              <div class="hw-ba-text">${esc(hw.exampleAfter)}</div>
            </div>
          </div>
        ` : ''}

        <div class="plain-explainer-grid">
          <div class="plain-explainer-card">
            <div class="plain-explainer-num">WHY IT'S SAFE</div>
            <div class="plain-explainer-title">India Digital Personal Data Protection (DPDP) &amp; Privacy Guardrails</div>
            <p>${esc(ag.guardrails)}</p>
          </div>
          <div class="plain-explainer-card">
            <div class="plain-explainer-num">HOW IT'S BUILT</div>
            <div class="plain-explainer-title">${esc(ag.buildTier)} Architecture Fit</div>
            <p>${isNoCode
              ? 'Built in Vertex AI / Gemini Enterprise No-Code Studio using policy grounding so Human Resources (HR) owners can update rules without engineering tickets.'
              : (isLowCode
                ? 'Combines rapid studio workflows with light connectors to turn unstructured talent and market signals into compliant campaigns.'
                : 'Uses Python Google Agent Development Kit (ADK) with Model Context Protocol (MCP) contracts for multi-system transactional writes and strict audit trails.')}</p>
          </div>
          <div class="plain-explainer-card">
            <div class="plain-explainer-num">MEASURED IMPACT</div>
            <div class="plain-explainer-title">${esc(String(ag.outcomeBadge || '').split('·')[0].trim())}</div>
            <p>Connects across <strong>${esc((ag.systems || []).join(', '))}</strong> while keeping every sensitive approval under human review (${esc(primaryPersona)}).</p>
          </div>
        </div>
      `;
    }

    function renderTraceStepsHtml(traceText) {
      const lines = String(traceText || '').split('\n').map(l => l.trim()).filter(Boolean);
      if (!lines.length) return '';
      return `
        <div class="trace-steps-list">
          ${lines.map((line, i) => {
            const cleanLine = line.replace(/^\d+[\.\)]\s*/, '');
            return `
              <div class="trace-step-row">
                <span class="trace-step-badge">0${i + 1}</span>
                <span class="trace-step-text">${esc(cleanLine)}</span>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    function openAgentPage(agentId, pushHash = true) {
      const ag = AGENTS[agentId];
      if (!ag) return;
      if (pushHash) history.pushState({ page: 'agent', id: agentId }, '', `#agent/${agentId}`);
      showActivePage('pageAgent');

      const pillar = PILLARS[ag.pillarId];
      const slideIdx = KEYNOTE_SLIDES.findIndex(s => s.agentId === ag.id || s.pillarId === ag.pillarId);
      const container = document.getElementById('agentPageContent');
      container.innerHTML = `
        <div class="back-bar">
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button type="button" class="back-btn" onclick="jumpToPillar('${ag.pillarId}')">&larr; Back to ${esc(ag.pillarName)}</button>
            <button type="button" class="back-btn" onclick="openMatrixPage(true)">All 14 Agents Matrix</button>
            <button type="button" class="back-btn" onclick="openArchitecturePage(true)">Platform Stack &amp; Proof</button>
          </div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            ${slideIdx >= 0 ? `<button type="button" class="switch-pill" onclick="openSlidesPage(${slideIdx}, true)">📊 View Keynote Slide &rarr;</button>` : ''}
            <button type="button" class="switch-pill" onclick="openValueChainPage('${pillar ? pillar.vcId : 'r2h'}', true)">Open End-to-End Flow &rarr;</button>
          </div>
        </div>

        <div class="simple-arch-card agent-hero-card">
          <div style="display:flex; flex-wrap:wrap; align-items:flex-start; justify-content:space-between; gap:18px;">
            <div style="max-width:780px;">
              <div style="display:flex; flex-wrap:wrap; align-items:center; gap:8px; margin-bottom:10px;">
                <span class="agent-num-chip" style="background:${pillar ? pillar.softBg : '#E8F0FE'}; color:${ag.pillarColor};">AGENT #${esc(ag.num)} &middot; ${esc(ag.pillarName)}</span>
                ${tierBadgeHtml(ag.buildTier)}
              </div>
              <h1 style="font-family:var(--font-display); font-size:clamp(26px,3.2vw,36px); font-weight:800; margin:0 0 6px 0;">${esc(ag.name)}</h1>
              <div style="font-size:14px; font-weight:700; color:var(--g-cobalt); margin-bottom:10px;">Owned HR Process: ${esc(ag.processName)}</div>
              <p style="font-size:15.5px; color:var(--text-secondary); margin:0 0 14px 0; line-height:1.55;">${esc(ag.shortDesc)}</p>
              <div style="display:flex; flex-wrap:wrap; gap:6px; align-items:center;">
                <span style="font-size:12px; font-weight:700; color:var(--text-muted);">Personas Served:</span>
                ${ag.personasServed.map(per => `<span class="persona-mini-chip">👤 ${esc(per)}</span>`).join('')}
              </div>
            </div>
            <div class="agent-value-callout">
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; color:var(--g-cobalt); letter-spacing:0.5px;">Target Business Outcome</div>
              <div style="font-family:var(--font-display); font-size:19px; font-weight:800; color:var(--text-primary); margin:6px 0 4px;">${esc(ag.outcomeBadge)}</div>
              <div style="font-size:12.5px; color:var(--text-secondary); line-height:1.4;">${esc(ag.baselineVsTarget)}</div>
            </div>
          </div>
        </div>

        <div class="showcase-compare-grid" style="grid-template-columns:repeat(3,minmax(0,1fr));">
          <div class="compare-card" style="border-top:3px solid #ea4335;">
            <div style="font-size:11.5px; font-weight:800; color:#c5221f; margin-bottom:6px; letter-spacing:0.4px;">CURRENT BOTTLENECK</div>
            <div style="font-size:14px; color:var(--text-secondary); line-height:1.5;">${esc(ag.problem)}</div>
          </div>
          <div class="compare-card" style="border-top:3px solid #4285f4;">
            <div style="font-size:11.5px; font-weight:800; color:#185abc; margin-bottom:6px; letter-spacing:0.4px;">AGENTIC DESIGN &amp; WORKFLOW</div>
            <div style="font-size:14px; color:var(--text-secondary); margin-bottom:8px; line-height:1.5;">${esc(ag.solution)}</div>
            <div style="font-size:12px; font-weight:700; color:var(--g-cobalt);">${esc(ag.platformLayer)}</div>
          </div>
          <div class="compare-card" style="border-top:3px solid #1e8e3e;">
            <div style="font-size:11.5px; font-weight:800; color:#137333; margin-bottom:6px; letter-spacing:0.4px;">GROUNDED ENTERPRISE IMPACT</div>
            <div style="font-size:14px; color:var(--text-secondary); line-height:1.5;">${esc(ag.advantage)}</div>
          </div>
        </div>

        <div class="simple-arch-card">
          <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px; margin-bottom:16px;">
            <div>
              <h2 style="font-family:var(--font-display); font-size:20px; font-weight:800; margin:0 0 4px;">How This Agent Works &mdash; End-to-End Runtime Architecture</h2>
              <div style="font-size:13px; color:var(--text-muted);">Clear 4-stage execution flow from employee/manager request through Gemini reasoning and Model Context Protocol (MCP) connectors</div>
            </div>
            ${tierBadgeHtml(ag.buildTier)}
          </div>
          ${renderAgentRuntimeBlueprint(ag)}
        </div>

        <div class="showcase-compare-grid">
          <div class="simple-arch-card" style="margin-bottom:0;">
            <h3 style="font-family:var(--font-display); font-size:17px; font-weight:800; margin:0 0 10px 0;">Connected HR Systems &amp; MCP Tools</h3>
            <ul style="margin:0 0 14px 0; padding-left:18px; font-size:13.5px; color:var(--text-secondary);">
              ${ag.systems.map(s => `<li style="margin-bottom:5px;">${esc(s)}</li>`).join('')}
            </ul>
            <div style="font-size:11.5px; font-weight:800; color:var(--text-muted); text-transform:uppercase; margin-bottom:8px; letter-spacing:0.4px;">Key Tools &amp; Connectors</div>
            <div style="display:flex; flex-direction:column; gap:6px;">
              ${ag.mcpTools.map(t => `<code class="tool-code-pill">${esc(t)}</code>`).join('')}
            </div>
          </div>
          <div class="simple-arch-card" style="margin-bottom:0;">
            <h3 style="font-family:var(--font-display); font-size:17px; font-weight:800; margin:0 0 10px 0;">Live Conversation &amp; Execution Walkthrough</h3>
            <div style="font-size:11.5px; font-weight:800; color:var(--g-cobalt); margin-bottom:6px; text-transform:uppercase; letter-spacing:0.4px;">Sample Plain-English Request</div>
            <div class="sample-prompt-box">
              "${esc(ag.samplePrompt)}"
            </div>
            <div style="font-size:11.5px; font-weight:800; color:#137333; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.4px;">What Happens Behind the Scenes</div>
            ${renderTraceStepsHtml(ag.sampleTrace)}
          </div>
        </div>
      `;
    }

    /* =========================================================================
       7. END-TO-END VALUE CHAIN PROCESS PAGE
       ========================================================================= */
    function selectVcStage(vcId, stageIdx) {
      selectedVcStageByVc[vcId] = stageIdx;
      openValueChainPage(vcId, false);
    }

    function openValueChainPage(vcId, pushHash = true) {
      const vc = VALUE_CHAINS[vcId];
      if (!vc) return;
      if (pushHash) history.pushState({ page: 'process', id: vcId }, '', `#process/${vcId}`);
      showActivePage('pageValueChain');

      const activeIdx = Math.min(selectedVcStageByVc[vcId] || 0, vc.stages.length - 1);
      const st = vc.stages[activeIdx];
      const container = document.getElementById('valueChainPageContent');

      container.innerHTML = `
        <div class="back-bar">
          <button type="button" class="back-btn" onclick="scrollToProcessJourneys()">&larr; Back to 4 E2E HR Processes</button>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            ${Object.values(VALUE_CHAINS).map(other => `
              <button type="button" class="switch-pill ${other.id === vc.id ? 'active' : ''}" onclick="openValueChainPage('${other.id}', true)">${esc(other.shortTitle)}</button>
            `).join('')}
          </div>
        </div>

        <div class="simple-arch-card" style="border-top:5px solid ${vc.color};">
          <span style="font-size:11.5px; font-weight:800; padding:4px 12px; border-radius:999px; background:${vc.color}18; color:${vc.color};">${esc(vc.flowBadge)}</span>
          <h1 style="font-family:var(--font-display); font-size:clamp(26px,3vw,36px); font-weight:800; margin:12px 0 8px;">${esc(vc.title)}</h1>
          <p style="font-size:15.5px; color:var(--text-secondary); margin:0 0 14px 0;">${esc(vc.summary)}</p>
          <div style="display:flex; flex-wrap:wrap; gap:12px;">
            <span style="padding:6px 14px; border-radius:10px; background:var(--g-red-bg); font-size:13px; font-weight:700; color:#c5221f;">Legacy Cycle: ${esc(vc.toilHoursBefore)}</span>
            <span style="padding:6px 14px; border-radius:10px; background:var(--g-green-bg); font-size:13px; font-weight:700; color:#137333;">Agentic State: ${esc(vc.headlineStat)} — ${esc(vc.toilHoursAfter)}</span>
          </div>
        </div>

        <h3 style="font-family:var(--font-display); font-size:18px; font-weight:800; margin:0 0 12px;">Interactive Stage Flow (Click Any Stage to Inspect Handoff &amp; Agent)</h3>
        <div class="vc-pipeline-strip-grid">
          ${vc.stages.map((s, idx) => `
            <div class="vc-pipe-step-card ${idx === activeIdx ? 'active' : ''}" style="--st-color:${vc.color};" onclick="selectVcStage('${vc.id}', ${idx})">
              <div style="display:flex; flex-direction:column; align-items:flex-start; gap:5px;">
                <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:${vc.color};">${esc(s.num)}</span>
                ${tierBadgeHtml(s.tier)}
              </div>
              <div style="font-family:var(--font-display); font-size:15px; font-weight:800; color:var(--text-primary); margin-top:8px;">${esc(s.name)}</div>
              <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">${esc(s.pillar)}</div>
            </div>
          `).join('')}
        </div>

        <div class="simple-arch-card" style="border-left:5px solid ${vc.color};">
          <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px;">
            <div>
              <div style="font-size:12px; font-weight:800; color:${vc.color};">${esc(st.num)} · ${esc(st.pillar)}</div>
              <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; margin:4px 0 8px;">${esc(st.name)} &rarr; ${esc(st.agentName)}</h2>
              <p style="font-size:15px; color:var(--text-secondary); margin:0;">${esc(st.summary)}</p>
            </div>
            <button type="button" class="hero-cta-btn hero-cta-primary" onclick="openAgentPage('${st.agentId}', true)">Open ${esc(st.agentName)} Studio &rarr;</button>
          </div>
        </div>

        <div class="showcase-compare-grid">
          <div class="compare-card" style="border-left:4px solid #ea4335;">
            <div style="font-size:11.5px; font-weight:800; color:#c5221f; margin-bottom:6px;">DISCONNECTED SILO PROBLEM</div>
            <div style="font-size:14px; color:var(--text-secondary);">${esc(vc.problem)}</div>
          </div>
          <div class="compare-card" style="border-left:4px solid #34a853;">
            <div style="font-size:11.5px; font-weight:800; color:#137333; margin-bottom:6px;">CONNECTED AGENTIC VALUE</div>
            <div style="font-size:14px; color:var(--text-secondary);">${esc(vc.solution)} ${esc(vc.advantage)}</div>
          </div>
        </div>

        <div class="simple-arch-card">
          <div style="font-size:11.5px; font-weight:800; color:var(--g-cobalt); margin-bottom:4px;">GROUNDED BENCHMARK &amp; EVIDENCE</div>
          <div style="font-weight:700; color:var(--text-primary); margin-bottom:6px;">${esc(vc.proofTitle)}</div>
          <div style="font-size:13.5px; color:var(--text-muted); margin-bottom:6px;">${esc(vc.proofBenchmark)}</div>
          <div style="font-size:14px; color:var(--text-secondary);">${esc(vc.proofDetail)}</div>
        </div>
      `;
    }

    /* =========================================================================
       8. KEYNOTE SLIDES VIEW (16:9 PPTX-READY + VISUAL CHARTS/ICONS + DOWNLOAD)
       ========================================================================= */
    const SLIDE_PILLAR_ICONS = {
      requisition_screening: 'assets/icons/pillar_workforce.png',
      candidate_hiring: 'assets/icons/pillar_attract.png',
      onboarding: 'assets/icons/pillar_ops.png',
      continuous_learning: 'assets/icons/pillar_develop.png',
      people_ops: 'assets/icons/pillar_engage.png',
      hr_strategy_rewards: 'assets/icons/pillar_perform.png'
    };

    const SLIDE_PILLAR_GCP = {
      requisition_screening: 'assets/gcp_icons/Agents-512-color.png',
      candidate_hiring: 'assets/gcp_icons/Collaboration-512-color.png',
      onboarding: 'assets/gcp_icons/IntegrationServices-512-color.png',
      continuous_learning: 'assets/gcp_icons/AIMachineLearning-512-color.png',
      people_ops: 'assets/gcp_icons/Operations-512-color.png',
      hr_strategy_rewards: 'assets/gcp_icons/BusinessIntelligence-512-color.png'
    };

    function shortSlidePhrase(str, maxWords = 8, keepDash = false) {
      const raw = String(str || '').trim();
      const s = keepDash ? raw : raw.split('—')[0].trim();
      const words = s.split(/\s+/);
      if (words.length <= maxWords) return s.replace(/[.,;]+$/, '');
      return words.slice(0, maxWords).join(' ').replace(/[.,;]+$/, '') + '…';
    }

    function renderSingleSlideHtml(sc, activeSlidesOverride = null) {
      const activeSlides = activeSlidesOverride || getActiveKeynoteSlides();
      const total = activeSlides.length;
      const fourBar = `<div class="slide-four-bar"><span style="background:#4285f4;"></span><span style="background:#ea4335;"></span><span style="background:#fbbc04;"></span><span style="background:#34a853;"></span></div>`;
      let bodyHtml = '';
      let headerIconHtml = '';

      if (sc.layout === 'hero') {
        const hlColors = ['#4285f4', '#ea4335', '#34a853'];
        const hlIcons = ['assets/icons/badge_sparkle.png', 'assets/icons/pillar_attract.png', 'assets/gcp_icons/Agents-512-color.png'];
        const items = (sc.highlights || []).map((h, i) => ({
          title: `0${i + 1}`,
          text: h,
          col: hlColors[i % 3],
          icon: hlIcons[i % 3]
        }));
        bodyHtml = `
          <div style="display:grid; grid-template-columns:1.25fr 0.95fr; gap:20px; align-items:center; flex:1; min-height:0;">
            <div style="display:flex; flex-direction:column; gap:10px;">
              <div>
                <span style="display:inline-block; padding:4px 12px; border-radius:999px; background:#e8f0fe; border:1px solid #d2e3fc; color:#185abc; font-size:10px; font-weight:800; letter-spacing:0.06em;">${esc(sc.eyebrow)}</span>
                <h2 style="font-family:var(--font-display); font-size:clamp(26px,2.8vw,38px); font-weight:800; color:#202124; margin:8px 0 6px; line-height:1.1;">${esc(sc.title)}</h2>
                <p style="font-size:14.5px; color:#5f6368; margin:0 0 8px;">${esc(sc.subtitle)}</p>
              </div>
              <div style="display:flex; flex-direction:column; gap:8px;">
                ${items.map(it => `
                  <div style="display:flex; align-items:center; gap:12px; padding:10px 12px; border-radius:12px; background:#f8f9fa; border:1px solid #e8eaed; border-left:5px solid ${it.col};">
                    <img src="${it.icon}" alt="" style="width:28px; height:28px; object-fit:contain; flex-shrink:0;" />
                    <div style="font-size:12.5px; font-weight:700; color:#202124; line-height:1.3;">${esc(it.text)}</div>
                  </div>
                `).join('')}
              </div>
            </div>
            <div class="slide-img-card" style="height:100%; max-height:420px; border-color:#d2e3fc;">
              <img src="assets/hero_chro_keynote.jpg" alt="Agentic HR Transformation Orbital Architecture" style="width:100%; height:100%; object-fit:contain; border-radius:8px;" />
            </div>
          </div>
        `;
      } else if (sc.layout === 'closing') {
        const steps = (Array.isArray(sc.ctaBoxes) && sc.ctaBoxes.length)
          ? sc.ctaBoxes.map(b => ({ num: b.num, title: b.title, text: b.desc, col: b.color, icon: b.icon }))
          : [
              { num: '01', title: "Today's Builder Lab", text: 'Policy Agent: Vertex AI RAG vs. Open Knowledge Format (OKF) + MCP.', col: '#4285f4', icon: 'assets/gcp_icons/Developer_Tools-512-color.png' },
              { num: '02', title: 'Week 1 Quick Wins', text: 'Ship No-Code Policy Pilot, JD Harmonizer & Onboarding Navigator.', col: '#34a853', icon: 'assets/icons/badge_nocode.png' },
              { num: '03', title: 'Quarter 1 Scale', text: 'Deploy ADK Concierge (~70% deflection) & Career Saathi Mobility.', col: '#7e57c2', icon: 'assets/gcp_icons/Agents-512-color.png' }
            ];
        bodyHtml = `
          <div style="display:grid; grid-template-columns:1.3fr 0.85fr; gap:20px; align-items:center; flex:1; min-height:0;">
            <div style="display:flex; flex-direction:column; gap:10px;">
              <div>
                <span style="display:inline-block; padding:4px 12px; border-radius:999px; background:#e8f0fe; border:1px solid #d2e3fc; color:#185abc; font-size:10px; font-weight:800; letter-spacing:0.06em;">${esc(sc.eyebrow)}</span>
                <h2 style="font-family:var(--font-display); font-size:clamp(22px,2.2vw,30px); font-weight:800; color:#202124; margin:8px 0 4px; line-height:1.15;">${esc(sc.title)}</h2>
                <p style="font-size:13px; color:#5f6368; margin:0 0 6px;">${esc(sc.subtitle)}</p>
              </div>
              <div style="display:flex; flex-direction:column; gap:8px;">
                ${steps.map(st => `
                  <div style="display:flex; align-items:center; gap:12px; padding:10px 14px; border-radius:12px; background:#f8f9fa; border:1.5px solid ${st.col};">
                    <span style="width:30px; height:30px; border-radius:50%; background:${st.col}; color:#fff; font-weight:800; font-size:12px; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;">${st.num}</span>
                    <div style="flex:1;">
                      <div style="font-size:13px; font-weight:800; color:${st.col};">${esc(st.title)}</div>
                      <div style="font-size:12px; color:#3c4043;">${esc(st.text)}</div>
                    </div>
                    <img src="${st.icon}" alt="" style="width:30px; height:30px; object-fit:contain; flex-shrink:0;" />
                  </div>
                `).join('')}
              </div>
            </div>
            <div class="slide-img-card" style="height:100%; max-height:420px; border-color:#d2e3fc;">
              <img src="assets/roadmap_launch.jpg" alt="HR Agentic Launch Roadmap" style="width:100%; height:100%; object-fit:contain; border-radius:8px;" />
            </div>
          </div>
        `;
      } else if (sc.layout === 'split_metrics') {
        headerIconHtml = `<img src="assets/icons/badge_clock.png" alt="" style="width:36px; height:36px; object-fit:contain;" />`;
        bodyHtml = `
          <div style="display:grid; grid-template-columns:1.05fr 1.25fr 0.9fr; gap:12px; flex:1; min-height:0; align-items:stretch;">
            <div class="slide-img-card"><img src="assets/charts/hr_paradox_donut.png" alt="75% Admin Tax vs 25% Strategy Donut Chart" /></div>
            <div class="slide-img-card"><img src="assets/charts/hr_paradox_bars.png" alt="Where HR Coordination Time Goes" /></div>
            <div style="display:flex; flex-direction:column; gap:10px;">
              <div style="flex:1; padding:12px; border-radius:12px; background:#fce8e6; border:1.5px solid #ea4335;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                  <img src="assets/icons/badge_clock.png" alt="" style="width:24px; height:24px;" />
                  <span style="font-family:var(--font-display); font-size:14px; font-weight:800; color:#c5221f;">~75% ADMIN TAX</span>
                </div>
                ${sc.leftItems.slice(0, 2).map(i => `<div style="font-size:11px; color:#202124; margin-bottom:4px;">• ${esc(shortSlidePhrase(i, 7, true))}</div>`).join('')}
              </div>
              <div style="flex:1; padding:12px; border-radius:12px; background:#ceead6; border:1.5px solid #34a853;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                  <img src="assets/gcp_icons/Collaboration-512-color.png" alt="" style="width:24px; height:24px;" />
                  <span style="font-family:var(--font-display); font-size:14px; font-weight:800; color:#137333;">~25% STRATEGY</span>
                </div>
                ${sc.rightItems.slice(0, 2).map(i => `<div style="font-size:11px; color:#202124; margin-bottom:4px;">• ${esc(shortSlidePhrase(i, 7, true))}</div>`).join('')}
              </div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:10px; padding:10px 14px; border-radius:10px; background:#e8f0fe; border:1px solid #d2e3fc; margin-top:10px;">
            <img src="assets/icons/badge_sparkle.png" alt="" style="width:26px; height:26px; object-fit:contain;" />
            <div style="font-size:12px; font-weight:700; color:#185abc;">Keynote Thesis: Agentic AI eliminates the ~75% administrative coordination tax — flipping HR from ticket handler to enterprise talent strategist.</div>
          </div>
        `;
      } else if (sc.layout === 'pillars4') {
        headerIconHtml = `<img src="assets/icons/badge_sparkle.png" alt="" style="width:36px; height:36px; object-fit:contain;" />`;
        const leverIcons = [
          'assets/gcp_icons/Agents-512-color.png',
          'assets/gcp_icons/Operations-512-color.png',
          'assets/gcp_icons/Collaboration-512-color.png',
          'assets/gcp_icons/AIMachineLearning-512-color.png'
        ];
        bodyHtml = `
          <div style="display:grid; grid-template-columns:1.12fr 1fr; gap:16px; flex:1; min-height:0; align-items:stretch;">
            <div style="padding:12px 14px; border-radius:12px; background:#ffffff; border:1px solid #e8eaed; display:flex; flex-direction:column; justify-content:space-between;">
              <div style="display:flex; justify-content:space-between; font-size:10.5px; font-weight:800;">
                <span style="color:#c5221f;">SILOED DOER</span>
                <span style="color:#137333;">STRATEGIC ORCHESTRATOR</span>
              </div>
              <div style="flex:1; display:flex; align-items:center; justify-content:center; min-height:0; padding:6px 0;">
                <img src="assets/orchestrator_shift.jpg" alt="Siloed Doer to Strategic Orchestrator" style="max-width:100%; max-height:255px; object-fit:contain;" />
              </div>
              <div style="padding:7px 10px; border-radius:8px; background:#f8f9fa; border:1px solid #e8eaed; font-size:11px; font-weight:700; color:#185abc; text-align:center;">
                Gemini Enterprise acts as the bridge — never replacing human empathy.
              </div>
            </div>
            <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:12px;">
              ${(sc.cards || META.fourValueLevers || []).map((c, idx) => `
                <div style="padding:14px; border-radius:12px; background:#f8f9fa; border:1px solid #e8eaed; border-top:4px solid ${c.color}; display:flex; flex-direction:column; gap:8px;">
                  <div style="display:flex; align-items:center; gap:8px;">
                    <img src="${leverIcons[idx % 4]}" alt="" style="width:26px; height:26px; object-fit:contain;" />
                    <div style="font-family:var(--font-display); font-size:14.5px; font-weight:800; color:#202124;">${esc(c.title)}</div>
                  </div>
                  <div style="padding:5px 8px; border-radius:6px; background:#ffffff; border:1px solid ${c.color}; color:${c.color}; font-size:11.5px; font-weight:800; text-align:center;">${esc(c.metric)}</div>
                  <div style="font-size:11.5px; color:#3c4043; line-height:1.35;">${esc(c.desc)}</div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      } else if (sc.layout === 'section_break') {
        const acc = sc.accent || '#4285f4';
        const chips = sc.chips || [];
        bodyHtml = `
          <div style="position:relative; flex:1; display:flex; flex-direction:column; justify-content:space-between; padding:18px 8px 10px;">
            <div style="position:absolute; top:-20px; left:-26px; right:-26px; height:7px; background:${acc}; border-radius:20px 20px 0 0;"></div>
            <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:18px; margin-top:16px;">
              <div style="max-width:78%;">
                <div style="display:inline-block; padding:4px 12px; border-radius:999px; background:#e8f0fe; border:1px solid #d2e3fc; color:${acc}; font-size:10.5px; font-weight:800; letter-spacing:0.06em;">${esc(sc.eyebrow)}</div>
                <h2 style="font-family:var(--font-display); font-size:clamp(26px,2.8vw,34px); font-weight:800; color:#202124; margin:14px 0 10px; line-height:1.12;">${esc(sc.title)}</h2>
                ${sc.subtitle ? `<p style="font-size:15px; color:#5f6368; margin:0; line-height:1.45;">${esc(sc.subtitle)}</p>` : ''}
              </div>
              <img src="assets/icons/badge_sparkle.png" alt="" style="width:68px; height:68px; object-fit:contain; flex-shrink:0;" />
            </div>
            ${chips.length ? `
              <div style="display:grid; grid-template-columns:repeat(${chips.length}, 1fr); gap:12px; margin-top:20px;">
                ${chips.map(ch => `
                  <div style="padding:14px 10px; border-radius:12px; background:#f8f9fa; border:1px solid #e8eaed; border-top:4px solid ${ch.color}; text-align:center;">
                    <div style="font-family:var(--font-display); font-size:12px; font-weight:800; color:${ch.color}; margin-bottom:4px;">${esc(ch.num)}</div>
                    <div style="font-family:var(--font-display); font-size:13px; font-weight:800; color:#202124; line-height:1.25;">${esc(ch.label)}</div>
                  </div>
                `).join('')}
              </div>
            ` : ''}
          </div>
        `;
      } else if (sc.layout === 'pillar_map') {
        headerIconHtml = `<img src="assets/gcp_icons/Agents-512-color.png" alt="" style="width:32px; height:32px; object-fit:contain;" />`;
        bodyHtml = `
          <div style="display:flex; align-items:center; justify-content:center; gap:8px; padding:5px 12px; border-radius:9px; background:#e8f0fe; border:1.5px solid #4285f4; color:#185abc; font-family:var(--font-display); font-size:11.5px; font-weight:800; margin-bottom:8px;">
            <img src="assets/icons/badge_sparkle.png" alt="" style="width:16px; height:16px;" />
            <span>OFFICE OF THE CHRO · 6 PILLARS · 14 PROCESS AGENTS</span>
            <img src="assets/gcp_icons/Agents-512-color.png" alt="" style="width:16px; height:16px;" />
          </div>
          <div style="display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:9px; flex:1; min-height:0;">
            ${Object.values(PILLARS).map(p => `
              <div style="padding:9px 11px; border-radius:10px; background:#f8f9fa; border:1px solid #e8eaed; border-top:3.5px solid ${p.color}; display:flex; flex-direction:column; justify-content:space-between; gap:5px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <img src="${SLIDE_PILLAR_ICONS[p.id] || 'assets/icons/badge_sparkle.png'}" alt="" style="width:26px; height:26px; object-fit:contain; flex-shrink:0;" />
                  <div style="min-width:0;">
                    <div style="font-size:8.5px; font-weight:800; color:${p.color};">${esc(p.apqcBadge)}</div>
                    <div style="font-family:var(--font-display); font-size:12px; font-weight:800; color:#202124; line-height:1.12;">${esc(p.shortName || p.name)}</div>
                  </div>
                </div>
                <div style="font-family:var(--font-display); font-size:12.5px; font-weight:800; color:${p.color}; line-height:1.15;">${esc(p.slideMetric || p.impactMetric)}</div>
                <div style="padding:4px 7px; border-radius:7px; background:#ffffff; border:1px solid #d2e3fc; font-size:9.5px; font-weight:700; color:#3c4043; text-align:center;">
                  ${esc(p.slideMixPill || (p.agentIds.length + ' Process Agents'))}
                </div>
              </div>
            `).join('')}
          </div>
        `;
      } else if (sc.layout === 'pillar_deepdive') {
        const p = PILLARS[sc.pillarId];
        const pAgents = p.agentIds.map(id => AGENTS[id]);
        const pIcon = SLIDE_PILLAR_ICONS[p.id] || 'assets/icons/badge_sparkle.png';
        const gIcon = SLIDE_PILLAR_GCP[p.id] || 'assets/gcp_icons/Agents-512-color.png';
        headerIconHtml = `<img src="${pIcon}" alt="" style="width:38px; height:38px; object-fit:contain;" />`;
        const chevronColors = [p.color, '#185abc', '#4285f4', '#0097a7', '#34a853'];
        const shortStages = p.slideShortStages || p.processStages.map(s => s.name);
        bodyHtml = `
          <div class="slide-chevron-strip" style="margin-bottom:14px;">
            ${shortStages.map((stLabel, idx) => `
              <div class="slide-chevron-step" style="background:${chevronColors[idx % chevronColors.length]};">
                <div style="font-size:11px; font-weight:800; line-height:1.15;">${esc(stLabel)}</div>
              </div>
            `).join('')}
          </div>
          <div style="display:grid; grid-template-columns:1fr 1.65fr; gap:14px; flex:1; min-height:0;">
            <div style="padding:16px 18px; border-radius:12px; background:#e8f0fe; border:1.5px solid ${p.color}; display:flex; flex-direction:column; justify-content:space-between;">
              <div style="display:flex; align-items:center; justify-content:space-between;">
                <img src="${pIcon}" alt="" style="width:46px; height:46px; object-fit:contain;" />
                <img src="${gIcon}" alt="" style="width:40px; height:40px; object-fit:contain;" />
              </div>
              <div>
                <div style="font-size:10px; font-weight:800; color:${p.color}; letter-spacing:0.04em; margin-bottom:4px;">BENCHMARK OUTCOME</div>
                <div style="font-family:var(--font-display); font-size:23px; font-weight:800; color:#202124; line-height:1.12; margin-bottom:6px;">${esc(p.slideMetric || p.impactMetric)}</div>
                ${p.slideMetricSub ? `<div style="font-size:12.5px; font-weight:700; color:#185abc; line-height:1.3;">${esc(p.slideMetricSub)}</div>` : ''}
              </div>
              <div style="padding:10px 12px; border-radius:10px; background:#ffffff; border:1px solid #e8eaed; font-size:11.5px; color:#3c4043; line-height:1.35;">
                <strong>Solves:</strong> ${esc(p.slideChallenge || '')}
              </div>
            </div>
            <div style="display:flex; flex-direction:column; gap:12px;">
              ${pAgents.map(ag => {
                const tCol = ag.buildTier === 'No-Code' ? '#34a853' : (ag.buildTier === 'Low-Code' ? '#4285f4' : '#7e57c2');
                const tIcon = ag.buildTier === 'No-Code' ? 'assets/icons/badge_nocode.png' : (ag.buildTier === 'High-Code' ? 'assets/icons/badge_adk.png' : 'assets/icons/badge_sparkle.png');
                return `
                  <div style="padding:12px 14px; border-radius:12px; background:#ffffff; border:1px solid #d2e3fc; border-left:5px solid ${tCol}; flex:1; display:flex; align-items:center; gap:14px;">
                    <img src="${tIcon}" alt="" style="width:36px; height:36px; object-fit:contain; flex-shrink:0;" />
                    <div style="flex:1;">
                      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:4px;">
                        <strong style="font-size:14px; color:#202124;">${esc(ag.name)}</strong>
                        <span style="font-size:9.5px; font-weight:800; padding:2px 9px; border-radius:999px; background:#f8f9fa; color:${tCol}; border:1px solid ${tCol};">${esc(ag.buildTier.toUpperCase())}</span>
                      </div>
                      <div style="font-size:12px; color:#3c4043; line-height:1.3;">${esc(ag.slideOutcome || ag.outcomeBadge)}</div>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;
      } else if (sc.layout === 'agent_spotlight') {
        const ag = AGENTS[sc.agentId];
        const tIcon = ag.buildTier === 'No-Code' ? 'assets/icons/badge_nocode.png' : (ag.buildTier === 'High-Code' ? 'assets/icons/badge_adk.png' : 'assets/icons/badge_sparkle.png');
        const sysIcon = ag.buildTier === 'Low-Code' ? 'assets/gcp_icons/IntegrationServices-512-color.png' : 'assets/gcp_icons/Databases-512-color.png';
        const specs = ag.slideSpecs || ag.architectureNodes.specialists.slice(0, 2);
        const systems = ag.slideSystems || ag.architectureNodes.connectors.slice(0, 2);
        headerIconHtml = `<img src="${tIcon}" alt="" style="width:38px; height:38px; object-fit:contain;" />`;
        bodyHtml = `
          <div style="display:grid; grid-template-columns:1fr 34px 1fr; gap:8px; align-items:center; margin-bottom:14px;">
            <div style="padding:10px 12px; border-radius:10px; background:#fce8e6; border:1px solid #ea4335; display:flex; align-items:center; gap:10px;">
              <img src="assets/icons/badge_clock.png" alt="" style="width:26px; height:26px; flex-shrink:0;" />
              <div>
                <div style="font-size:9.5px; font-weight:800; color:#c5221f;">BEFORE</div>
                <div style="font-size:12px; font-weight:700; color:#202124;">${esc(ag.slideBefore || ag.problem)}</div>
              </div>
            </div>
            <div class="slide-flow-arrow">&rarr;</div>
            <div style="padding:10px 12px; border-radius:10px; background:#ceead6; border:1px solid #34a853; display:flex; align-items:center; gap:10px;">
              <img src="assets/icons/badge_check.png" alt="" style="width:26px; height:26px; flex-shrink:0;" />
              <div>
                <div style="font-size:9.5px; font-weight:800; color:#137333;">AFTER</div>
                <div style="font-size:12px; font-weight:700; color:#202124;">${esc(ag.slideAfter || ag.outcomeBadge)}</div>
              </div>
            </div>
          </div>

          <div style="display:grid; grid-template-columns:1fr 28px 1fr 28px 1fr; gap:8px; align-items:stretch; flex:1; min-height:0;">
            <div style="padding:14px; border-radius:12px; background:#e8f0fe; border:1.5px solid #4285f4; display:flex; flex-direction:column; align-items:center; justify-content:space-between; text-align:center; gap:8px;">
              <img src="assets/gcp_icons/Agents-512-color.png" alt="" style="width:40px; height:40px; object-fit:contain;" />
              <div style="font-size:9.5px; font-weight:800; color:#185abc;">1. AGENT ORCHESTRATOR</div>
              <div style="font-size:13.5px; font-weight:800; color:#202124;">${esc(ag.slideOrch || ag.name)}</div>
              <div style="width:100%; padding:6px 8px; border-radius:6px; background:#ffffff; border:1px solid #d2e3fc; font-size:11px; font-weight:700; color:#185abc;">For: ${esc(ag.personasServed[0])}</div>
            </div>
            <div class="slide-flow-arrow">&rarr;</div>
            <div style="padding:14px; border-radius:12px; background:#f8f9fa; border:1px solid #e8eaed; display:flex; flex-direction:column; align-items:center; justify-content:space-between; text-align:center; gap:8px;">
              <img src="assets/gcp_icons/AIMachineLearning-512-color.png" alt="" style="width:40px; height:40px; object-fit:contain;" />
              <div style="font-size:9.5px; font-weight:800; color:#4285f4;">2. KEY CAPABILITIES</div>
              <div style="display:flex; flex-direction:column; gap:7px; width:100%;">
                ${specs.map(s => `<div style="width:100%; padding:7px 8px; border-radius:6px; background:#ffffff; border:1px solid #d2e3fc; font-size:11.5px; font-weight:700; color:#202124;">${esc(s)}</div>`).join('')}
              </div>
            </div>
            <div class="slide-flow-arrow" style="color:#0097a7;">&rarr;</div>
            <div style="padding:14px; border-radius:12px; background:#f8f9fa; border:1px solid #e8eaed; display:flex; flex-direction:column; align-items:center; justify-content:space-between; text-align:center; gap:8px;">
              <img src="${sysIcon}" alt="" style="width:40px; height:40px; object-fit:contain;" />
              <div style="font-size:9.5px; font-weight:800; color:#0097a7;">3. CONNECTED SYSTEMS</div>
              <div style="display:flex; flex-direction:column; gap:7px; width:100%;">
                ${systems.map(c => `<div style="width:100%; padding:7px 8px; border-radius:6px; background:#e0f7fa; border:1px solid #0097a7; font-size:11.5px; font-weight:700; color:#006978;">${esc(c)}</div>`).join('')}
              </div>
            </div>
          </div>

          <div style="display:flex; align-items:center; gap:10px; padding:10px 14px; border-radius:10px; background:#fff2cc; border:1px solid #e37400; margin-top:12px;">
            <img src="assets/gcp_icons/SecurityIdentity-512-color.png" alt="" style="width:28px; height:28px; flex-shrink:0;" />
            <div style="font-size:12px; color:#202124;"><strong>India DPDP &amp; HITL Lock:</strong> ${esc(ag.slideGuardrail || ag.guardrails)}</div>
          </div>
        `;
      } else if (sc.layout === 'enterprise_proof') {
        headerIconHtml = `<img src="assets/icons/badge_check.png" alt="" style="width:36px; height:36px; object-fit:contain;" />`;
        const proof = META.enterpriseProofPoint;
        const kpiIcons = [
          'assets/gcp_icons/Agents-512-color.png',
          'assets/gcp_icons/BusinessIntelligence-512-color.png',
          'assets/icons/badge_nocode.png',
          'assets/gcp_icons/SecurityIdentity-512-color.png'
        ];
        bodyHtml = `
          <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:12px;">
            ${proof.metrics.map((m, i) => `
              <div style="padding:10px 12px; border-radius:10px; background:${i % 2 === 0 ? '#e8f0fe' : '#ceead6'}; border:1px solid #d2e3fc; display:flex; align-items:center; gap:10px;">
                <img src="${kpiIcons[i % 4]}" alt="" style="width:28px; height:28px; object-fit:contain; flex-shrink:0;" />
                <div>
                  <div style="font-family:var(--font-display); font-size:19px; font-weight:800; color:#185abc; line-height:1.1;">${esc(m.value)}</div>
                  <div style="font-size:10px; font-weight:700; color:#202124;">${esc(m.label)}</div>
                </div>
              </div>
            `).join('')}
          </div>
          <div style="display:grid; grid-template-columns:1.1fr 1fr; gap:14px; flex:1; min-height:0; align-items:stretch;">
            <div class="slide-img-card"><img src="assets/charts/enterprise_proof_bars.png" alt="Enterprise Production Benchmark Impact" /></div>
            <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:10px;">
              ${proof.liveHrAgents.map((la, i) => `
                <div style="padding:12px; border-radius:10px; background:#f8f9fa; border:1px solid #e8eaed; border-top:4px solid ${['#4285f4','#ea4335','#fbbc04','#34a853'][i]}; display:flex; flex-direction:column; justify-content:space-between;">
                  <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px;">
                    <img src="assets/icons/badge_nocode.png" alt="" style="width:18px; height:18px;" />
                    <div style="font-weight:800; font-size:12.5px; color:#202124;">${esc(la.name)}</div>
                  </div>
                  <div style="font-size:11px; color:#3c4043; line-height:1.35;">${esc(la.slideDesc || la.desc)}</div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      } else if (sc.layout === 'architecture_layers') {
        headerIconHtml = `<img src="assets/gcp_icons/Storage-512-color.png" alt="" style="width:36px; height:36px; object-fit:contain;" />`;
        const layers = [
          ['1. THE TASKFORCE (HR Experiences)', '14 Process Agents + PeopleStrong / Workday / ServiceNow', '#4285f4', '#e8f0fe', 'assets/gcp_icons/Agents-512-color.png', 'assets/gcp_icons/Collaboration-512-color.png'],
          ['2. THE WORKBENCH (Dual Build Tier)', '6 No/Low-Code Studio Agents + 8 Code-First ADK Agents', '#34a853', '#ceead6', 'assets/gcp_icons/Developer_Tools-512-color.png', 'assets/gcp_icons/IntegrationServices-512-color.png'],
          ['3. THE CONTEXT (Enterprise Memory)', 'Open Knowledge Format (OKF) + Vertex AI RAG + FastMCP', '#0097a7', '#e0f7fa', 'assets/gcp_icons/Storage-512-color.png', 'assets/gcp_icons/Databases-512-color.png'],
          ['4. THE BRAINS (Model Tiering)', 'Gemini Flash (Sub-Second FAQ) + Gemini Pro (Deep Reasoning)', '#7e57c2', '#e6e7fb', 'assets/gcp_icons/AIMachineLearning-512-color.png', 'assets/gcp_icons/BusinessIntelligence-512-color.png']
        ];
        bodyHtml = `
          <div style="display:grid; grid-template-columns:3fr 1fr; gap:14px; flex:1; min-height:0;">
            <div style="display:flex; flex-direction:column; gap:10px; justify-content:space-between;">
              ${layers.map(l => `
                <div style="flex:1; padding:12px 16px; border-radius:12px; background:${l[3]}; border:1.5px solid ${l[2]}; display:flex; align-items:center; gap:14px;">
                  <img src="${l[4]}" alt="" style="width:34px; height:34px; object-fit:contain; flex-shrink:0;" />
                  <div style="flex:1;">
                    <div style="font-size:11.5px; font-weight:800; color:${l[2]};">${l[0]}</div>
                    <div style="font-size:13px; font-weight:700; color:#202124;">${l[1]}</div>
                  </div>
                  <img src="${l[5]}" alt="" style="width:28px; height:28px; object-fit:contain; flex-shrink:0;" />
                </div>
              `).join('')}
            </div>
            <div style="padding:14px 12px; border-radius:12px; background:#fff2cc; border:1.5px solid #e37400; display:flex; flex-direction:column; align-items:center; justify-content:space-between; text-align:center;">
              <img src="assets/gcp_icons/SecurityIdentity-512-color.png" alt="" style="width:44px; height:44px; object-fit:contain;" />
              <div style="font-size:11.5px; font-weight:800; color:#b05a00;">TRUST &amp; INDIA DPDP SHIELD</div>
              ${['Model Armor Guard', 'Cloud DLP Redaction', 'Consent Ledger', 'Least Privilege IAM'].map(s => `
                <div style="width:100%; padding:7px 8px; border-radius:8px; background:#ffffff; border:1px solid #e37400; font-size:10.5px; font-weight:700; color:#202124;">${s}</div>
              `).join('')}
            </div>
          </div>
        `;
      } else if (sc.layout === 'adoption_curve') {
        headerIconHtml = `<img src="assets/gcp_icons/BusinessIntelligence-512-color.png" alt="" style="width:36px; height:36px; object-fit:contain;" />`;
        const adIcons = [
          'assets/gcp_icons/Collaboration-512-color.png',
          'assets/gcp_icons/SecurityIdentity-512-color.png',
          'assets/gcp_icons/Operations-512-color.png',
          'assets/gcp_icons/AIMachineLearning-512-color.png'
        ];
        bodyHtml = `
          <div style="display:flex; flex-direction:column; gap:12px; flex:1; min-height:0;">
            <div class="slide-img-card" style="flex:1.25; min-height:0;"><img src="assets/charts/value_scurve.png" alt="3-Horizon Agentic HR Value Curve" /></div>
            <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px;">
              ${META.adoptionPillars.map((ap, i) => `
                <div style="padding:12px; border-radius:10px; background:#f8f9fa; border:1px solid #e8eaed; border-top:4px solid ${['#4285f4','#ea4335','#e37400','#34a853'][i]};">
                  <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px;">
                    <img src="${adIcons[i % 4]}" alt="" style="width:22px; height:22px; object-fit:contain;" />
                    <span style="font-size:9.5px; font-weight:800; color:${['#4285f4','#ea4335','#e37400','#34a853'][i]};">PILLAR #${ap.num}</span>
                  </div>
                  <div style="font-size:12px; font-weight:800; color:#202124; margin-bottom:4px;">${esc(ap.title)}</div>
                  <div style="font-size:10.5px; color:#5f6368; line-height:1.3;">${esc(ap.slideDesc || ap.desc)}</div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      } else if (sc.layout === 'macro_shift') {
        headerIconHtml = `<img src="assets/gcp_icons/Agents-512-color.png" alt="" style="width:36px; height:36px; object-fit:contain;" />`;
        bodyHtml = `
          <div style="display:grid; grid-template-columns:1.1fr 1fr; gap:16px; flex:1; min-height:0; align-items:stretch;">
            <div class="slide-img-card" style="padding:10px; border-color:#d2e3fc;">
              <img src="${esc(sc.heroImage || 'assets/zero_ui_workplace.jpg')}" alt="From Legacy HR Forms to Zero-UI Agentic Experience" style="border-radius:8px;" />
            </div>
            <div style="display:flex; flex-direction:column; gap:10px; justify-content:space-between;">
              ${(sc.cards || []).map(c => `
                <div style="flex:1; padding:10px 14px; border-radius:12px; background:#f8f9fa; border:1px solid #e8eaed; border-left:5px solid ${c.accent}; display:flex; align-items:center; gap:12px;">
                  <img src="${esc(c.icon)}" alt="" style="width:34px; height:34px; object-fit:contain; flex-shrink:0;" />
                  <div>
                    <div style="font-family:var(--font-display); font-size:13.5px; font-weight:800; color:#202124; margin-bottom:2px;">${esc(c.title)}</div>
                    <div style="font-size:11.5px; color:#3c4043; line-height:1.35;">${esc(c.desc)}</div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
          ${sc.statBanner ? `
            <div style="display:flex; align-items:center; gap:10px; padding:9px 14px; border-radius:10px; background:#e8f0fe; border:1px solid #d2e3fc; margin-top:10px;">
              <img src="assets/icons/badge_sparkle.png" alt="" style="width:22px; height:22px; object-fit:contain; flex-shrink:0;" />
              <div style="font-size:12px; font-weight:700; color:#185abc;">${esc(sc.statBanner)}</div>
            </div>
          ` : ''}
        `;
      } else if (sc.layout === 'human_premium') {
        headerIconHtml = `<img src="assets/icons/pillar_engage.png" alt="" style="width:36px; height:36px; object-fit:contain;" />`;
        bodyHtml = `
          <div style="display:grid; grid-template-columns:1.08fr 1fr; gap:16px; flex:1; min-height:0; align-items:stretch;">
            <div class="slide-img-card" style="padding:10px; border-color:#ceead6;">
              <img src="${esc(sc.heroImage || 'assets/human_premium.jpg')}" alt="Human-First Leadership Amplified by AI" style="border-radius:8px;" />
            </div>
            <div style="display:flex; flex-direction:column; gap:10px; justify-content:space-between;">
              ${(sc.pillars || []).map(p => `
                <div style="flex:1; padding:10px 14px; border-radius:12px; background:#f8f9fa; border:1px solid #e8eaed; border-top:3.5px solid ${p.color}; display:flex; align-items:center; gap:12px;">
                  <img src="${esc(p.icon)}" alt="" style="width:32px; height:32px; object-fit:contain; flex-shrink:0;" />
                  <div>
                    <div style="font-family:var(--font-display); font-size:13.5px; font-weight:800; color:#202124; margin-bottom:2px;">${esc(p.title)}</div>
                    <div style="font-size:11.5px; color:#3c4043; line-height:1.35;">${esc(p.desc)}</div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
          ${sc.quote ? `
            <div style="display:flex; align-items:center; justify-content:center; gap:10px; padding:9px 16px; border-radius:10px; background:linear-gradient(90deg, #e8f0fe 0%, #e6f4ea 100%); border:1px solid #d2e3fc; margin-top:10px;">
              <div style="font-family:var(--font-display); font-size:12.5px; font-weight:800; color:#185abc; text-align:center;">${esc(sc.quote)}</div>
            </div>
          ` : ''}
        `;
      } else if (sc.layout === 'moments_matter') {
        headerIconHtml = `<img src="assets/icons/badge_sparkle.png" alt="" style="width:32px; height:32px; object-fit:contain;" />`;
        bodyHtml = `
          <div style="display:flex; flex-direction:column; gap:8px; flex:1; min-height:0;">
            <div class="slide-img-card" style="flex:0.86; min-height:0; padding:5px 10px; border-color:#d2e3fc;">
              <img src="${esc(sc.heroImage || 'assets/moments_matter.jpg')}" alt="Five Hire-to-Retire Moments Visual Pathway" style="width:100%; height:100%; object-fit:contain;" />
            </div>
            <div style="display:grid; grid-template-columns:repeat(5, minmax(0, 1fr)); gap:8px; flex:1.1; min-height:0;">
              ${(sc.moments || []).map(m => `
                <div style="padding:8px 8px; border-radius:10px; background:#f8f9fa; border:1px solid #e8eaed; border-top:3.5px solid ${m.color}; display:flex; flex-direction:column; justify-content:space-between; text-align:center;">
                  <div style="display:flex; align-items:center; justify-content:space-between;">
                    <span style="font-family:var(--font-mono); font-size:9px; font-weight:800; color:${m.color};">${esc(m.step)}</span>
                    <img src="${esc(m.icon)}" alt="" style="width:20px; height:20px; object-fit:contain;" />
                  </div>
                  <div>
                    <div style="font-family:var(--font-display); font-size:12px; font-weight:800; color:#202124;">${esc(m.title)}</div>
                    <div style="font-family:var(--font-display); font-size:15.5px; font-weight:800; color:${m.color}; margin:3px 0 1px;">${esc(m.metric)}</div>
                    <div style="font-size:8.5px; font-weight:700; color:#5f6368; text-transform:uppercase; letter-spacing:0.04em;">${esc(m.metricLbl)}</div>
                  </div>
                  <div style="font-size:9.5px; color:#3c4043; line-height:1.22; padding-top:4px; border-top:1px dashed #dadce0;">${esc(m.desc)}</div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      } else if (sc.layout === 'mindmap_agents') {
        headerIconHtml = `<img src="assets/gcp_icons/Agents-512-color.png" alt="" style="width:32px; height:32px; object-fit:contain;" />`;
        const branchPillars = (sc.pillarIds || []).map(id => PILLARS[id]).filter(Boolean);
        bodyHtml = `
          <div class="mm-slide-grid">
            <div class="mm-hub-card">
              <div>
                <img src="assets/gcp_icons/Agents-512-color.png" alt="" style="width:34px; height:34px; object-fit:contain; margin:0 auto 4px; display:block;" />
                <div style="font-size:8.5px; font-weight:800; color:#185abc; letter-spacing:0.05em; text-transform:uppercase;">MIND MAP · ${esc(sc.part || '')}</div>
                <div style="font-family:var(--font-display); font-size:13px; font-weight:800; color:#202124; margin:3px 0 2px; line-height:1.12;">${esc(sc.hubTitle || 'Agent Ecosystem')}</div>
                <div style="font-size:9.8px; font-weight:700; color:#4285f4;">${esc(sc.hubSub || '')}</div>
              </div>
              <div style="width:100%; display:flex; flex-direction:column; gap:4px; text-align:left; padding:6px; border-radius:8px; background:#ffffff; border:1px solid #d2e3fc;">
                <div style="font-size:8px; font-weight:800; color:#5f6368; text-transform:uppercase;">${slideDeckVersion === 'v2' ? 'Solution Type' : 'Build Tier Key'}</div>
                <div style="display:flex; align-items:center; gap:4px; font-size:8.5px; font-weight:700; color:#137333;"><span style="width:7px; height:7px; border-radius:50%; background:#34a853; display:inline-block; flex-shrink:0;"></span> ${slideDeckVersion === 'v2' ? 'HR Team Studio' : 'No/Low-Code'}</div>
                <div style="display:flex; align-items:center; gap:4px; font-size:8.5px; font-weight:700; color:#185abc;"><span style="width:7px; height:7px; border-radius:50%; background:#5e35b1; display:inline-block; flex-shrink:0;"></span> ${slideDeckVersion === 'v2' ? 'Cross-System Sync' : 'ADK + MCP'}</div>
              </div>
            </div>
            <div style="display:flex; align-items:center; justify-content:center;">
              <svg width="14" height="100%" viewBox="0 0 14 240" preserveAspectRatio="none" aria-hidden="true">
                <path d="M0,120 C7,120 6,38 14,38 M0,120 L14,120 M0,120 C7,120 6,202 14,202" stroke="#aecbfa" stroke-width="2" fill="none" />
              </svg>
            </div>
            <div class="mm-branches-col">
              ${branchPillars.map(p => {
                const pAgents = p.agentIds.map(id => AGENTS[id]).filter(Boolean);
                const pIcon = SLIDE_PILLAR_ICONS[p.id] || 'assets/icons/badge_sparkle.png';
                return `
                  <div class="mm-branch-row">
                    <div class="mm-pillar-node" style="border-left:4px solid ${p.color}; border-color:${p.color}33; border-left-color:${p.color};">
                      <img src="${pIcon}" alt="" style="width:22px; height:22px; object-fit:contain; flex-shrink:0;" />
                      <div style="min-width:0;">
                        <div style="font-size:8px; font-weight:800; color:${p.color}; letter-spacing:0.03em; line-height:1.1;">${esc(p.apqcBadge || ('PILLAR 0' + p.vNum))}</div>
                        <div style="font-family:var(--font-display); font-size:11px; font-weight:800; color:#202124; line-height:1.12;">${esc(p.shortName || p.name)}</div>
                      </div>
                    </div>
                    <div style="display:flex; align-items:center; justify-content:center;">
                      <svg width="12" height="18" viewBox="0 0 12 18" aria-hidden="true">
                        <path d="M0,9 L10,9 M6.5,5 L10.5,9 L6.5,13" stroke="${p.color}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round" />
                      </svg>
                    </div>
                    <div class="mm-agents-row" style="grid-template-columns:repeat(${pAgents.length}, minmax(0, 1fr));">
                      ${pAgents.map(ag => {
                        const isAdk = ag.buildTier === 'High-Code';
                        const tierCol = isAdk ? '#5e35b1' : '#137333';
                        const tierBg = isAdk ? '#f3e8fd' : '#e6f4ea';
                        const tierTxt = slideDeckVersion === 'v2'
                          ? (isAdk ? 'Connected' : 'HR Studio')
                          : (isAdk ? 'ADK' : (ag.buildTier === 'Low-Code' ? 'Low-Code' : 'No-Code'));
                        return `
                          <div class="mm-agent-node" style="border-top:3px solid ${tierCol};" onclick="openAgentPage('${ag.id}', true)" title="Click to inspect ${esc(ag.simpleName || ag.name)} Studio">
                            <div style="display:flex; flex-direction:column; gap:2px; min-width:0;">
                              <span style="align-self:flex-start; font-size:7.5px; font-weight:800; padding:1px 5px; border-radius:999px; background:${tierBg}; color:${tierCol}; white-space:nowrap;">${tierTxt}</span>
                              <div style="font-family:var(--font-display); font-size:10.5px; font-weight:800; color:#202124; line-height:1.12;">${esc(ag.simpleName || ag.name)}</div>
                            </div>
                            <div class="mm-persona-chips">
                              ${(ag.personasServed || []).map(per => `<span class="mm-persona-chip">&#128100; ${esc(per)}</span>`).join('')}
                            </div>
                          </div>
                        `;
                      }).join('')}
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;
      } else if (sc.layout === 'governance_dpdp') {
        headerIconHtml = `<img src="assets/gcp_icons/SecurityIdentity-512-color.png" alt="" style="width:36px; height:36px; object-fit:contain;" />`;
        bodyHtml = `
          <div style="display:grid; grid-template-columns:0.88fr 1.25fr; gap:16px; flex:1; min-height:0; align-items:stretch;">
            <div class="slide-img-card" style="padding:10px; border-color:#d2e3fc;">
              <img src="${esc(sc.heroImage || 'assets/governance_dpdp.jpg')}" alt="India DPDP Privacy & Fairness Shield" style="border-radius:8px;" />
            </div>
            <div style="display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:12px;">
              ${(sc.cards || []).map(c => `
                <div style="padding:13px 14px; border-radius:12px; background:#f8f9fa; border:1px solid #e8eaed; border-top:4px solid ${c.color}; display:flex; flex-direction:column; justify-content:space-between; gap:8px;">
                  <div style="display:flex; align-items:center; gap:10px;">
                    <img src="${esc(c.icon)}" alt="" style="width:30px; height:30px; object-fit:contain; flex-shrink:0;" />
                    <div style="font-family:var(--font-display); font-size:13px; font-weight:800; color:#202124; line-height:1.2;">${esc(c.title)}</div>
                  </div>
                  <div style="font-size:11.5px; color:#3c4043; line-height:1.38;">${esc(c.desc)}</div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      } else if (sc.layout === 'workforce_readiness') {
        headerIconHtml = `<img src="assets/icons/pillar_develop.png" alt="" style="width:32px; height:32px; object-fit:contain;" />`;
        bodyHtml = `
          <div style="display:grid; grid-template-columns:1.18fr 0.94fr; gap:12px; flex:1; min-height:0; align-items:stretch;">
            <div class="slide-img-card" style="padding:8px; border-color:#d2e3fc;">
              <img src="${esc(sc.chartImage || 'assets/charts/workforce_readiness_chart.png')}" alt="Workforce AI Readiness Strategic Time Shift" />
            </div>
            <div style="display:flex; flex-direction:column; gap:5px; justify-content:space-between; min-height:0;">
              ${(sc.personas || []).map(p => `
                <div style="flex:1; padding:6px 10px; border-radius:9px; background:#f8f9fa; border:1px solid #e8eaed; border-left:4px solid ${p.color}; display:flex; align-items:center; gap:8px;">
                  <img src="${esc(p.icon)}" alt="" style="width:24px; height:24px; object-fit:contain; flex-shrink:0;" />
                  <div style="flex:1; min-width:0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin-bottom:1px;">
                      <span style="font-family:var(--font-display); font-size:11px; font-weight:800; color:#202124;">${esc(p.role)}</span>
                      <span style="font-size:8.5px; font-weight:800; padding:1.5px 6px; border-radius:999px; background:#e8f0fe; color:${p.color}; white-space:nowrap;">${esc(p.lift)}</span>
                    </div>
                    <div style="font-size:9.8px; color:#3c4043; line-height:1.22;">${esc(p.action)}</div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      } else if (sc.layout === 'touchpoints_grid') {
        headerIconHtml = `<img src="assets/icons/badge_sparkle.png" alt="" style="width:36px; height:36px; object-fit:contain;" />`;
        bodyHtml = `
          <div class="tp-levers-bar">
            ${(sc.levers || []).map(lv => `
              <div class="tp-lever-pill" style="border-top:3.5px solid ${lv.color};">
                <div style="font-family:var(--font-display); font-size:12px; font-weight:800; color:${lv.color};">${esc(lv.title)}</div>
                <div style="font-size:10px; color:#3c4043; line-height:1.25;">${esc(lv.desc)}</div>
              </div>
            `).join('')}
          </div>
          <div class="tp-grid-4x2">
            ${(sc.touchpoints || []).map(tp => `
              <div class="tp-card" style="border-top:4px solid ${tp.color};">
                <div style="display:flex; align-items:center; gap:9px;">
                  <img src="${esc(tp.icon)}" alt="" style="width:28px; height:28px; object-fit:contain; flex-shrink:0;" />
                  <div style="font-family:var(--font-display); font-size:13px; font-weight:800; color:#202124; line-height:1.15;">${esc(tp.title)}</div>
                </div>
                <div style="font-size:11px; color:#3c4043; line-height:1.35;">${esc(tp.desc)}</div>
              </div>
            `).join('')}
          </div>
        `;
      } else if (sc.layout === 'pillar_functions_map') {
        headerIconHtml = `<img src="assets/icons/pillar_workforce.png" alt="" style="width:32px; height:32px; object-fit:contain;" />`;
        bodyHtml = `
          <div style="display:flex; align-items:center; justify-content:center; gap:8px; padding:4px 12px; border-radius:9px; background:#e8f0fe; border:1.5px solid #4285f4; color:#185abc; font-family:var(--font-display); font-size:10.8px; font-weight:800; margin-bottom:6px;">
            <img src="assets/icons/badge_sparkle.png" alt="" style="width:15px; height:15px;" />
            <span>${esc(sc.banner || 'OFFICE OF THE CHRO · 6 PILLARS · 25 BUSINESS FUNCTIONS')}</span>
          </div>
          <div class="pf-grid-3x2">
            ${(sc.pillarsData || []).map(item => {
              const p = PILLARS[item.pillarId];
              if (!p) return '';
              const pIcon = SLIDE_PILLAR_ICONS[p.id] || 'assets/icons/badge_sparkle.png';
              return `
                <div class="pf-card" style="border-top:3.5px solid ${p.color};" onclick="selectPillar('${p.id}'); goToOrgChart();" title="Explore ${esc(p.shortName || p.name)} in Portal">
                  <div style="display:flex; align-items:center; gap:7px;">
                    <img src="${pIcon}" alt="" style="width:22px; height:22px; object-fit:contain; flex-shrink:0;" />
                    <div style="min-width:0;">
                      <div style="font-size:8px; font-weight:800; color:${p.color}; letter-spacing:0.03em; line-height:1.1;">${esc(p.apqcBadge)}</div>
                      <div style="font-family:var(--font-display); font-size:11.5px; font-weight:800; color:#202124; line-height:1.12;">${esc(p.shortName || p.name)}</div>
                    </div>
                  </div>
                  <div style="padding:3px 6px; border-radius:6px; background:#ffffff; border:1px solid ${p.color}44; font-family:var(--font-display); font-size:10px; font-weight:800; color:${p.color}; text-align:center;">
                    ${esc(item.outcome)}
                  </div>
                  <div class="pf-fn-grid">
                    ${(item.functions || []).map(fn => `<div class="pf-fn-pill">${esc(fn)}</div>`).join('')}
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        `;
      } else if (sc.layout === 'pillar_value_pair') {
        headerIconHtml = `<img src="assets/icons/pillar_perform.png" alt="" style="width:32px; height:32px; object-fit:contain;" />`;
        bodyHtml = `
          ${sc.topBanner ? `
            <div style="display:flex; align-items:center; gap:7px; padding:4px 10px; border-radius:8px; background:#e8f0fe; border:1px solid #d2e3fc; margin-bottom:6px;">
              <img src="assets/icons/badge_sparkle.png" alt="" style="width:15px; height:15px; flex-shrink:0;" />
              <div style="font-size:10px; font-weight:700; color:#185abc; line-height:1.2;">${esc(sc.topBanner)}</div>
            </div>
          ` : ''}
          <div class="pv-pair-grid">
            ${(sc.cards || []).map(c => `
              <div class="pv-col-card" style="border-top:4px solid ${c.color};">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                  <div style="display:flex; align-items:center; gap:7px; min-width:0;">
                    <img src="${esc(c.icon)}" alt="" style="width:25px; height:25px; object-fit:contain; flex-shrink:0;" />
                    <div style="min-width:0;">
                      <div style="font-size:8px; font-weight:800; color:${c.color}; letter-spacing:0.03em;">${esc(c.badge)}</div>
                      <div style="font-family:var(--font-display); font-size:12px; font-weight:800; color:#202124; line-height:1.12;">${esc(c.title)}</div>
                    </div>
                  </div>
                  <div style="padding:4px 8px; border-radius:8px; background:#f8f9fa; border:1px solid ${c.color}55; text-align:center; flex-shrink:0;">
                    <div style="font-family:var(--font-display); font-size:14px; font-weight:800; color:${c.color}; line-height:1.05;">${esc(c.metric)}</div>
                    <div style="font-size:7px; font-weight:800; color:#5f6368; letter-spacing:0.04em;">${esc(c.metricLbl)}</div>
                  </div>
                </div>
                <div style="display:flex; flex-direction:column; gap:5px; flex:1; min-height:0;">
                  <div class="pv-strip" style="background:#fce8e6; border-left:3.5px solid #ea4335;">
                    <span><strong style="color:#c5221f;">Today's Friction:</strong> ${esc(c.problem)}</span>
                  </div>
                  <div class="pv-strip" style="background:#e8f0fe; border-left:3.5px solid ${c.color};">
                    <span><strong style="color:#185abc;">Solution:</strong> ${esc(c.solution)}</span>
                  </div>
                  <div class="pv-strip" style="background:#e6f4ea; border-left:3.5px solid #137333;">
                    <span><strong style="color:#137333;">Business Outcome:</strong> ${esc(c.value)}</span>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        `;
      } else if (sc.layout === 'adoption_close') {
        bodyHtml = `
          <div style="display:grid; grid-template-columns:1.38fr 0.78fr; gap:14px; align-items:stretch; flex:1; min-height:0;">
            <div style="display:flex; flex-direction:column; justify-content:space-between; gap:5px; min-height:0;">
              <div>
                <span style="display:inline-block; padding:2.5px 9px; border-radius:999px; background:#e8f0fe; border:1px solid #d2e3fc; color:#185abc; font-size:9px; font-weight:800; letter-spacing:0.05em;">${esc(sc.eyebrow)}</span>
                <h2 style="font-family:var(--font-display); font-size:clamp(17px,1.8vw,22px); font-weight:800; color:#202124; margin:3px 0 2px; line-height:1.12;">${esc(sc.title)}</h2>
                <p style="font-size:10.8px; color:#5f6368; margin:0;">${esc(sc.subtitle)}</p>
              </div>
              <div style="display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:6px;">
                ${(sc.adoptionPillars || []).map(ap => `
                  <div style="padding:6px 8px; border-radius:9px; background:#f8f9fa; border:1px solid #e8eaed; border-top:3px solid ${ap.color}; display:flex; align-items:flex-start; gap:7px;">
                    <img src="${esc(ap.icon)}" alt="" style="width:20px; height:20px; object-fit:contain; flex-shrink:0;" />
                    <div>
                      <div style="font-family:var(--font-display); font-size:10.5px; font-weight:800; color:${ap.color}; line-height:1.15;">${esc(ap.num)} · ${esc(ap.title)}</div>
                      <div style="font-size:9.3px; color:#3c4043; line-height:1.2;">${esc(ap.desc)}</div>
                    </div>
                  </div>
                `).join('')}
              </div>
              <div style="display:flex; flex-direction:column; gap:5px;">
                ${(sc.ctaBoxes || []).map(st => `
                  <div style="display:flex; align-items:center; gap:9px; padding:5px 10px; border-radius:9px; background:#ffffff; border:1.5px solid ${st.color};">
                    <span style="width:22px; height:22px; border-radius:50%; background:${st.color}; color:#fff; font-weight:800; font-size:10px; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;">${esc(st.num)}</span>
                    <div style="flex:1; min-width:0;">
                      <div style="font-size:10.8px; font-weight:800; color:${st.color}; line-height:1.15;">${esc(st.title)}</div>
                      <div style="font-size:9.8px; color:#3c4043; line-height:1.2;">${esc(st.desc)}</div>
                    </div>
                    <img src="${esc(st.icon)}" alt="" style="width:20px; height:20px; object-fit:contain; flex-shrink:0;" />
                  </div>
                `).join('')}
              </div>
            </div>
            <div class="slide-img-card" style="height:100%; max-height:440px; border-color:#d2e3fc;">
              <img src="${esc(sc.heroImage || 'assets/roadmap_launch.jpg')}" alt="90-Day HR Transformation Roadmap" style="width:100%; height:100%; object-fit:contain; border-radius:8px;" />
            </div>
          </div>
        `;
      }

      const headerBlock = (sc.layout === 'hero' || sc.layout === 'closing' || sc.layout === 'adoption_close' || sc.layout === 'section_break') ? '' : `
        <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:10px; margin-bottom:6px; flex-shrink:0;">
          <div>
            <div style="display:inline-block; padding:2.5px 9px; border-radius:999px; background:#e8f0fe; border:1px solid #d2e3fc; color:#185abc; font-size:9px; font-weight:800; letter-spacing:0.05em;">${esc(sc.eyebrow)}</div>
            <h2 style="font-family:var(--font-display); font-size:clamp(16px,1.6vw,20px); font-weight:800; color:#202124; margin:3px 0 1px; line-height:1.12;">${esc(sc.title)}</h2>
            ${(sc.layout === 'agent_spotlight' ? `${AGENTS[sc.agentId].pillarName} · ${AGENTS[sc.agentId].slideProcessShort || AGENTS[sc.agentId].processName} · ${AGENTS[sc.agentId].buildTier}` : sc.subtitle) ? `<div style="font-size:10.8px; color:#5f6368;">${esc(sc.layout === 'agent_spotlight' ? `${AGENTS[sc.agentId].pillarName} · ${AGENTS[sc.agentId].slideProcessShort || AGENTS[sc.agentId].processName} · ${AGENTS[sc.agentId].buildTier}` : sc.subtitle)}</div>` : ''}
          </div>
          ${headerIconHtml ? `<div style="flex-shrink:0; padding-top:2px;">${headerIconHtml}</div>` : ''}
        </div>
      `;

      return `
        <div class="keynote-slide-frame">
          ${headerBlock}
          ${bodyHtml}
          <div class="slide-brand-footer">
            <div class="slide-brand-lockup" aria-label="Google Cloud and Gemini">
              <img src="assets/branding/google_cloud_logo.png" alt="Google Cloud" class="slide-brand-gc" />
              <span class="slide-brand-divider" aria-hidden="true"></span>
              <img src="assets/branding/gemini_logo.png" alt="Gemini" class="slide-brand-gemini" />
            </div>
            <span style="font-family:var(--font-mono); font-weight:700;">${esc(sc.num)} / ${String(total).padStart(2, '0')}</span>
          </div>
          ${fourBar}
        </div>
      `;
    }

    function setSlideDeckVersion(ver, idx = 0) {
      const targetVer = (ver === 'v1' || ver === 'v2') ? ver : 'v2';
      slideDeckVersion = targetVer;
      const slides = getActiveKeynoteSlides();
      currentSlideIdx = Math.max(0, Math.min(idx, Math.max(0, slides.length - 1)));
      history.replaceState({ page: 'slides', ver: slideDeckVersion, idx: currentSlideIdx }, '', `#slides/${slideDeckVersion}`);
      renderSlidesPage();
    }

    function openSlidesPage(idx = null, pushHash = true, ver = null) {
      if (ver === 'v1' || ver === 'v2') slideDeckVersion = ver;
      const slides = getActiveKeynoteSlides();
      if (idx !== null && idx >= 0 && idx < slides.length) currentSlideIdx = idx;
      if (currentSlideIdx >= slides.length) currentSlideIdx = 0;
      if (pushHash) history.pushState({ page: 'slides', ver: slideDeckVersion, idx: currentSlideIdx }, '', `#slides/${slideDeckVersion}`);
      showActivePage('pageSlides');
      renderSlidesPage();
    }

    function setSlideViewMode(mode) {
      slideViewMode = mode;
      renderSlidesPage();
    }

    function stepSlide(delta) {
      const slides = getActiveKeynoteSlides();
      if (!slides.length) return;
      currentSlideIdx = (currentSlideIdx + delta + slides.length) % slides.length;
      renderSlidesPage();
    }

    function selectSlideIdx(idx) {
      currentSlideIdx = idx;
      slideViewMode = 'presenter';
      renderSlidesPage();
    }

    function printAllSlidesPdf() {
      const prevMode = slideViewMode;
      slideViewMode = 'grid';
      renderSlidesPage();
      setTimeout(() => {
        window.print();
        slideViewMode = prevMode;
        renderSlidesPage();
      }, 150);
    }

    function renderSlidesPage() {
      const container = document.getElementById('slidesPageContent');
      if (!container) return;
      const slides = getActiveKeynoteSlides();
      if (currentSlideIdx >= slides.length) currentSlideIdx = 0;
      const sc = slides[currentSlideIdx] || slides[0];
      const isV2 = slideDeckVersion === 'v2' && KEYNOTE_SLIDES_V2.length > 0;
      const pptxHref = isV2 ? 'CHRO_Agentic_Transformation_Keynote_v2.pptx?v=1' : 'CHRO_Agentic_Transformation_Keynote.pptx?v=4';
      const pptxName = isV2 ? 'CHRO_Agentic_Transformation_Keynote_v2.pptx' : 'CHRO_Agentic_Transformation_Keynote.pptx';

      const toolbar = `
        <div class="slides-toolbar">
          <div>
            <div style="font-size:11px; font-weight:800; color:var(--g-cobalt); text-transform:uppercase;">Keynote Presentation &amp; PowerPoint Mode (16:9 Widescreen)</div>
            <div style="font-family:var(--font-display); font-size:20px; font-weight:800;">
              ${isV2 ? `PeopleStrong Xponential 2026 — Stage Keynote v2 (${slides.length} Slides)` : `PeopleStrong Xponential 2026 — Architecture Deck v1 (${slides.length} Slides)`}
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
            <div class="deck-version-switcher" role="tablist" aria-label="Slide deck version">
              <button type="button" class="deck-ver-pill ${isV2 ? 'active' : ''}" onclick="setSlideDeckVersion('v2', 0)">&#10024; v2 &middot; Stage Keynote (${KEYNOTE_SLIDES_V2.length})</button>
              <button type="button" class="deck-ver-pill ${!isV2 ? 'active' : ''}" onclick="setSlideDeckVersion('v1', 0)">&#128208; v1 &middot; Full Deck (${KEYNOTE_SLIDES_V1.length})</button>
            </div>
            <button type="button" class="switch-pill ${slideViewMode === 'presenter' ? 'active' : ''}" onclick="setSlideViewMode('presenter')">🖥️ Presenter</button>
            <button type="button" class="switch-pill ${slideViewMode === 'grid' ? 'active' : ''}" onclick="setSlideViewMode('grid')">🗂️ All ${slides.length} Slides</button>
            <button type="button" class="switch-pill" onclick="printAllSlidesPdf()">🖨️ Export PDF</button>
            ${!isV2 ? `<a href="https://docs.google.com/presentation/d/1PkW9mPtL3Tta4s5xVUgxiXTlWO2FdInVRp7Hnyng6qU/edit" target="_blank" rel="noopener" class="switch-pill" style="border-color:#4285f4; color:#185abc;">🎞️ Google Slides &nearr;</a>` : ''}
            <a href="${pptxHref}" download="${pptxName}" class="pptx-download-btn">📊 Download ${isV2 ? 'v2 ' : 'v1 '}.pptx</a>
          </div>
        </div>
      `;

      if (slideViewMode === 'grid') {
        container.innerHTML = `
          ${toolbar}
          <div class="slides-overview-grid">
            ${slides.map((s, idx) => `
              <div>
                ${renderSingleSlideHtml(s, slides)}
                <div class="no-print" style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                  <span style="font-size:12px; color:var(--text-muted); font-weight:600;">Slide ${s.num}: ${esc(s.title)}</span>
                  <button type="button" class="switch-pill" style="padding:4px 10px; font-size:11.5px;" onclick="selectSlideIdx(${idx})">Present Full &rarr;</button>
                </div>
              </div>
            `).join('')}
          </div>
        `;
        return;
      }

      container.innerHTML = `
        ${toolbar}
        <div class="keynote-stage-shell">
          <div class="slide-rail">
            ${slides.map((s, idx) => `
              <button type="button" class="slide-rail-item ${idx === currentSlideIdx ? 'active' : ''}" onclick="selectSlideIdx(${idx})">
                <span style="font-family:var(--font-mono); font-weight:800;">${esc(s.num)}</span>
                <span>${esc(s.title)}</span>
              </button>
            `).join('')}
          </div>
          <div>
            ${renderSingleSlideHtml(sc, slides)}
            <div class="no-print" style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:10px; margin-top:14px;">
              <div style="display:flex; gap:8px;">
                <button type="button" class="back-btn" onclick="stepSlide(-1)">&larr; Previous (Left Arrow)</button>
                <button type="button" class="back-btn" onclick="stepSlide(1)">Next (Right Arrow) &rarr;</button>
              </div>
              <button type="button" class="switch-pill" onclick="showSpeakerNotes = !showSpeakerNotes; renderSlidesPage();">
                ${showSpeakerNotes ? 'Hide Presenter Notes' : 'Show Presenter Notes'}
              </button>
            </div>
            ${showSpeakerNotes ? `
              <div class="speaker-notes-box">
                <strong style="color:var(--g-cobalt);">Speaker Talking Point (Slide ${esc(sc.num)}):</strong> ${esc(sc.notes || '')}
              </div>
            ` : ''}
          </div>
        </div>
      `;
    }

    /* =========================================================================
       9. PERIODIC AGENT MATRIX, PLATFORM PROOF & MIND MAP
       ========================================================================= */
    function openMatrixPage(pushHash = true) {
      if (pushHash) history.pushState({ page: 'matrix' }, '', '#matrix');
      showActivePage('pageMatrix');
      renderMatrixPage();
    }

    function setMatrixFilter(f) {
      currentMatrixFilter = f;
      renderMatrixPage();
    }

    function renderMatrixPage() {
      const container = document.getElementById('matrixPageContent');
      if (!container) return;
      const allAgents = Object.values(AGENTS);
      const filtered = allAgents.filter(a => {
        if (currentMatrixFilter === 'NO_LOW') return a.buildTier === 'No-Code' || a.buildTier === 'Low-Code';
        if (currentMatrixFilter === 'HIGH') return a.buildTier === 'High-Code';
        return true;
      });

      container.innerHTML = `
        <div class="back-bar">
          <button type="button" class="back-btn" onclick="goToOrgChart()">&larr; Back to Office of the CHRO</button>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button type="button" class="switch-pill ${currentMatrixFilter === 'ALL' ? 'active' : ''}" onclick="setMatrixFilter('ALL')">All 14 HR Agents</button>
            <button type="button" class="switch-pill ${currentMatrixFilter === 'NO_LOW' ? 'active' : ''}" onclick="setMatrixFilter('NO_LOW')">No-Code &amp; Low-Code (${allAgents.filter(a => a.buildTier !== 'High-Code').length})</button>
            <button type="button" class="switch-pill ${currentMatrixFilter === 'HIGH' ? 'active' : ''}" onclick="setMatrixFilter('HIGH')">High-Code ADK + MCP (${allAgents.filter(a => a.buildTier === 'High-Code').length})</button>
          </div>
        </div>

        <div style="margin-bottom:22px;">
          <h1 style="font-family:var(--font-display); font-size:clamp(26px,3vw,34px); font-weight:800; margin:0 0 6px;">Periodic Matrix of CHRO Office AI Agents (14 Elements)</h1>
          <p style="color:var(--text-muted); margin:0;">Color-coded across the 6 Human Resources Pillars (APQC 7.0 Aligned) and tagged by Gemini Enterprise Build Tier.</p>
        </div>

        <div class="matrix-grid">
          ${filtered.map(ag => `
            <div class="matrix-cell" style="--cell-accent:${ag.pillarColor};" onclick="openAgentPage('${ag.id}', true)">
              <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                  <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:${ag.pillarColor};">${esc(ag.num)} · ${esc(ag.code)}</span>
                  ${tierBadgeHtml(ag.buildTier)}
                </div>
                <div style="font-family:var(--font-display); font-size:17px; font-weight:800; color:var(--text-primary); margin-bottom:4px;">${esc(ag.name)}</div>
                <div style="font-size:12px; font-weight:700; color:${ag.pillarColor}; margin-bottom:6px;">${esc(ag.pillarName)}</div>
                <div style="font-size:12.5px; color:var(--text-muted);">${esc(ag.processName)}</div>
              </div>
              <div style="padding-top:8px; border-top:1px solid var(--border-subtle); font-size:11.5px; font-weight:700; color:var(--text-secondary);">
                ${esc(ag.outcomeBadge)} &rarr;
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }

    let activeArchTierFilter = 'All';

    function setArchTierFilter(tier) {
      activeArchTierFilter = tier;
      const box = document.getElementById('archStackVisualHost');
      if (box) box.innerHTML = renderPlatformStackHtml(activeArchTierFilter);
    }

    function renderPlatformStackHtml(filterTier) {
      const allAgents = Object.values(AGENTS);
      const filteredAgents = filterTier === 'All'
        ? allAgents
        : allAgents.filter(a => a.buildTier === filterTier);
      const tierGuide = {
        'All': '14 HR process agents split deliberately: 5 No-Code Studio quick wins, 1 Low-Code campaign agent, and 8 High-Code Google Agent Development Kit (ADK) orchestrators.',
        'No-Code': 'Use No-Code Studio (5 Agents) when HR specialists want to update policies or FAQ reels in minutes using plain documents and Open Knowledge Format (OKF) citations.',
        'Low-Code': 'Use Low-Code Hybrid (1 Agent) when connecting structured outreach studios to public labor research and lightweight career-site Q&A widgets.',
        'High-Code': 'Use High-Code Google ADK + FastMCP (8 Agents) when an agent writes across multiple HR/IT systems, redacts Personal Identifiable Information (PII), or runs audit math.'
      };

      return `
        <div class="stack-arch-layout">
          <div class="stack-layers-col">
            <div class="stack-layer-box stack-layer-top">
              <div class="stack-layer-head">
                <div class="stack-layer-title">1. THE TASKFORCE &mdash; Where HR &amp; Employees Work</div>
                <span class="stack-layer-tag">6 HR Pillars &middot; 14 Agents</span>
              </div>
              <div class="stack-layer-desc">Embedded directly inside employee chat, Career Portal, PeopleStrong / Workday HCM, Google Meet, and ServiceNow HRSD so nobody learns another portal.</div>
            </div>

            <div class="stack-layer-box stack-layer-workbench">
              <div class="stack-layer-head">
                <div class="stack-layer-title">2. THE WORKBENCH &mdash; Select Build Complexity by Task</div>
                <span class="stack-layer-tag">Hours (Studio) &harr; Multi-System (ADK)</span>
              </div>
              <div class="stack-layer-desc">${esc(tierGuide[filterTier] || tierGuide['All'])}</div>
              <div class="stack-tier-tabs">
                ${[
                  { id: 'All', label: `All 14 Agents` },
                  { id: 'No-Code', label: `No-Code Studio (5)` },
                  { id: 'Low-Code', label: `Low-Code Hybrid (1)` },
                  { id: 'High-Code', label: `High-Code ADK + MCP (8)` }
                ].map(t => `
                  <button type="button" class="switch-pill ${filterTier === t.id ? 'active' : ''}" onclick="setArchTierFilter('${t.id}')">${esc(t.label)}</button>
                `).join('')}
              </div>
              <div class="stack-tier-agents">
                ${filteredAgents.map(a => `
                  <button type="button" class="stack-agent-link" onclick="openAgentPage('${a.id}', true)">#${esc(a.num)} ${esc(a.simpleName || a.name)} &rarr;</button>
                `).join('')}
              </div>
            </div>

            <div class="stack-layer-box stack-layer-context">
              <div class="stack-layer-head">
                <div class="stack-layer-title">3. THE CONTEXT &mdash; Grounded Memory &amp; Two-Way Tools</div>
                <span class="stack-layer-tag">OKF + Vertex AI RAG + FastMCP</span>
              </div>
              <div class="stack-layer-desc">Combines Open Knowledge Format (OKF) clause-cited HR handbooks, Vertex AI Search RAG, BigQuery workforce tables, and FastMCP enterprise API connectors.</div>
            </div>

            <div class="stack-layer-box stack-layer-brains">
              <div class="stack-layer-head">
                <div class="stack-layer-title">4. THE BRAINS &mdash; Smart Gemini Model Tiering</div>
                <span class="stack-layer-tag">Cost &amp; Latency Engineered</span>
              </div>
              <div class="stack-layer-desc"><strong>Gemini Flash</strong> handles 80% of high-volume policy Q&amp;A and resume parsing in under a second; <strong>Gemini Pro</strong> handles pay equity modeling, rubric calibration, and multi-system orchestration.</div>
            </div>
          </div>

          <div class="stack-shield-col">
            <div>
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#b06000; letter-spacing:0.4px; margin-bottom:4px;">VERTICAL TRUST SHIELD</div>
              <div style="font-family:var(--font-display); font-size:16.5px; font-weight:800; color:var(--text-primary); margin-bottom:10px;">India DPDP &amp; Safety Built In</div>
              <div style="display:flex; flex-direction:column; gap:8px;">
                <div class="stack-shield-item">
                  <strong>Model Armor Guard</strong>
                  <span>Blocks prompt injection, toxicity, and unauthorized policy exceptions in real time.</span>
                </div>
                <div class="stack-shield-item">
                  <strong>Cloud DLP Redaction</strong>
                  <span>Masks candidate names, colleges, phone numbers, and salary IDs before AI scoring.</span>
                </div>
                <div class="stack-shield-item">
                  <strong>K-Anonymity Lock (N &ge; 10)</strong>
                  <span>Aggregates pulse burnout signals only at cohort level &mdash; never individual tracking.</span>
                </div>
                <div class="stack-shield-item">
                  <strong>Human-in-the-Loop (HITL)</strong>
                  <span>Zero autonomous candidate rejections, salary edits, or disciplinary actions.</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function openArchitecturePage(pushHash = true) {
      if (pushHash) history.pushState({ page: 'architecture' }, '', '#architecture');
      showActivePage('pageArchitecture');
      const proof = META.enterpriseProofPoint || {};
      const archSlideIdx = KEYNOTE_SLIDES.findIndex(s => s.layout === 'architecture_layers');
      const container = document.getElementById('architecturePageContent');
      if (!container) return;

      container.innerHTML = `
        <div class="back-bar">
          <button type="button" class="back-btn" onclick="goToOrgChart()">&larr; Back to Office of the CHRO</button>
          <button type="button" class="switch-pill" onclick="openSlidesPage(${archSlideIdx >= 0 ? archSlideIdx : 17}, true)">📊 View Architecture Slide &rarr;</button>
        </div>

        <div class="simple-arch-card" style="border-top:4px solid #4285f4;">
          <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:var(--g-cobalt); letter-spacing:0.4px; margin-bottom:4px;">GEMINI ENTERPRISE REFERENCE STACK</div>
          <h1 style="font-family:var(--font-display); font-size:clamp(25px,3vw,33px); font-weight:800; margin:0 0 8px;">How the HR Agent Architecture Fits Together</h1>
          <p style="color:var(--text-secondary); margin:0 0 10px; line-height:1.5;">A 4-layer enterprise blueprint built so HR owns policy updates in No-Code Studio while Engineering wires multi-system connectors via Google Agent Development Kit (ADK) and Model Context Protocol (MCP) under strict India Digital Personal Data Protection (DPDP) Act controls.</p>
          <div id="archStackVisualHost">${renderPlatformStackHtml(activeArchTierFilter)}</div>
        </div>

        <div class="simple-arch-card">
          <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; margin:0 0 12px;">${esc(proof.title)}</h2>
          <div class="hero-kpi-strip" style="margin-top:0; margin-bottom:18px;">
            ${(proof.metrics || []).map(m => `
              <div class="hero-kpi-card" style="background:var(--bg-ice-blue);">
                <div class="hero-kpi-val">${esc(m.value)}</div>
                <div class="hero-kpi-lbl">${esc(m.label)}</div>
              </div>
            `).join('')}
          </div>
          <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:12px; margin-bottom:16px;">
            ${(proof.liveHrAgents || []).map(la => `
              <div style="padding:14px; border-radius:14px; background:var(--bg-surface-alt); border:1px solid var(--border-subtle); display:flex; flex-direction:column; gap:6px; align-items:flex-start;">
                ${tierBadgeHtml(la.tier)}
                <strong style="font-size:14.5px; color:var(--text-primary);">${esc(la.name)}</strong>
                <div style="font-size:13px; color:var(--text-secondary);">${esc(la.desc)}</div>
              </div>
            `).join('')}
          </div>
          <ul style="margin:0; padding-left:18px; color:var(--text-secondary); font-size:13.5px;">
            ${(proof.architectureLessons || []).map(l => `<li style="margin-bottom:5px;">${esc(l)}</li>`).join('')}
          </ul>
        </div>

        <div class="simple-arch-card">
          <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; margin:0 0 12px;">No-Code vs. Code-First Google ADK &amp; Dual-Retrieval Comparison</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>Architecture Dimension</th>
                <th>No-Code (Gemini Enterprise Studio)</th>
                <th>Low-Code Connectors</th>
                <th>High-Code (Google ADK + FastMCP)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>HR Examples in Portfolio</strong></td>
                <td>Policy Pilot, Job Description Harmonizer, Onboarding Buddy, Micro-Learning Studio</td>
                <td>Talent Magnet Outreach &amp; Interview Scheduler Connectors</td>
                <td>HR Concierge, Career Saathi, Blind Screening, Day-1 Provisioning, Pay Equity &amp; Rewards</td>
              </tr>
              <tr>
                <td><strong>Knowledge Grounding</strong></td>
                <td>Verified HR Policy Drives / Open Knowledge Format (OKF) Concepts</td>
                <td>Careers Portal + Google Workspace Calendar / Meet APIs</td>
                <td>Dual Retrieval (Vertex AI Search RAG + OKF Traversal) + BigQuery / Spanner</td>
              </tr>
              <tr>
                <td><strong>Cross-System Action</strong></td>
                <td>Read &amp; Draft Generation</td>
                <td>Scoped Calendar Booking &amp; FAQ Replies</td>
                <td>Atomic Read/Write across PeopleStrong, Workday &amp; ServiceNow via FastMCP</td>
              </tr>
              <tr>
                <td><strong>Safety &amp; India DPDP Controls</strong></td>
                <td>Grounded-Only Citations + Strict Refusal Prompts</td>
                <td>Employer Brand Guardrails + Calendar Free/Busy Only</td>
                <td>Model Armor Prompt Shield + Cloud DLP PII Redaction + Mandatory HITL Gates</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="simple-arch-card">
          <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; margin:0 0 14px;">Gemini Enterprise 3-Horizon Value Curve &amp; 4 Adoption Pillars</h2>
          <div style="display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin-bottom:20px;">
            ${(META.valueCurve || []).map(v => `
              <div style="padding:16px; border-radius:14px; background:var(--bg-surface-alt); border:1px solid var(--border-subtle); border-top:4px solid ${v.color};">
                <div style="font-size:11px; font-weight:800; color:${v.color};">${esc(v.stage)}</div>
                <div style="font-family:var(--font-display); font-size:16px; font-weight:800; margin:4px 0 8px;">${esc(v.headline)}</div>
                <ul style="margin:0; padding-left:16px; font-size:13px; color:var(--text-secondary);">
                  ${v.bullets.map(b => `<li style="margin-bottom:4px;">${esc(b)}</li>`).join('')}
                </ul>
              </div>
            `).join('')}
          </div>
          <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:12px;">
            ${(META.adoptionPillars || []).map((ap, i) => `
              <div style="padding:14px; border-radius:14px; background:var(--bg-surface-alt); border:1px solid var(--border-subtle);">
                <div style="font-size:11px; font-weight:800; color:${['#1a73e8','#185abc','#007b83','#1e8e3e'][i]};">ADOPTION PILLAR #${esc(ap.num)}</div>
                <div style="font-weight:800; margin:4px 0;">${esc(ap.title)}</div>
                <div style="font-size:13px; color:var(--text-secondary);">${esc(ap.desc)}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    function openMindMapPage(pushHash = true) {
      if (pushHash) history.pushState({ page: 'mindmap' }, '', '#mindmap');
      showActivePage('pageMindMap');
      renderMindMapPage();
    }

    function selectMindMapPillar(pid) {
      currentMindMapPillarId = pid;
      const p = PILLARS[pid];
      currentMindMapAgentId = p && p.agentIds.length ? p.agentIds[0] : null;
      renderMindMapPage();
    }

    function selectMindMapAgent(aid) {
      currentMindMapAgentId = aid;
      renderMindMapPage();
    }

    function renderMindMapPage() {
      const container = document.getElementById('mindMapPageContent');
      if (!container) return;
      const activePillar = PILLARS[currentMindMapPillarId] || Object.values(PILLARS)[0];
      const pAgents = activePillar.agentIds.map(id => AGENTS[id]).filter(Boolean);
      const activeAgent = AGENTS[currentMindMapAgentId] && AGENTS[currentMindMapAgentId].pillarId === activePillar.id
        ? AGENTS[currentMindMapAgentId]
        : pAgents[0];

      container.innerHTML = `
        <div class="back-bar">
          <button type="button" class="back-btn" onclick="goToOrgChart()">&larr; Back to Office of the CHRO</button>
          <button type="button" class="switch-pill" onclick="openSlidesPage(3, true)">📊 View Architecture Map Slide →</button>
        </div>
        <h1 style="font-family:var(--font-display); font-size:clamp(26px,3vw,34px); font-weight:800; margin:0 0 6px;">CHRO Click-Path &amp; Process Taxonomy Explorer</h1>
        <p style="color:var(--text-muted); margin:0 0 22px;">Trace how Office of the Chief Human Resources Officer (CHRO) strategy cascades into 6 HR Function Pillars &rarr; Processes &rarr; 14 Agents &rarr; Served Personas.</p>

        <div class="mindmap-columns">
          <div class="mindmap-col">
            <div style="font-size:11px; font-weight:800; color:var(--g-cobalt); margin-bottom:8px;">1. CHRO FUNCTION PILLARS</div>
            <div style="display:flex; flex-direction:column; gap:8px;">
              ${Object.values(PILLARS).map(p => `
                <button type="button" class="switch-pill ${p.id === activePillar.id ? 'active' : ''}" style="justify-content:space-between; width:100%; text-align:left; border-radius:12px;" onclick="selectMindMapPillar('${p.id}')">
                  <span>${esc(p.vNum)} · ${esc(p.shortName)}</span>
                  <span style="color:${p.color};">&rarr;</span>
                </button>
              `).join('')}
            </div>
          </div>

          <div class="mindmap-col">
            <div style="font-size:11px; font-weight:800; color:${activePillar.color}; margin-bottom:8px;">2. PROCESSES &amp; AGENTS (${pAgents.length})</div>
            <div style="display:flex; flex-direction:column; gap:8px;">
              ${pAgents.map(a => `
                <button type="button" class="switch-pill ${activeAgent && a.id === activeAgent.id ? 'active' : ''}" style="flex-direction:column; align-items:flex-start; width:100%; border-radius:12px;" onclick="selectMindMapAgent('${a.id}')">
                  <span style="font-weight:800;">${esc(a.name)}</span>
                  <span style="font-size:11px; color:var(--text-muted);">${esc(a.processName)} · ${esc(a.buildTier)}</span>
                </button>
              `).join('')}
            </div>
          </div>

          <div class="mindmap-col" style="border-top:4px solid ${activePillar.color};">
            ${activeAgent ? `
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
                <span style="font-size:11.5px; font-weight:800; color:${activePillar.color};">3. AGENT SPECIFICATION &amp; STAKEHOLDERS</span>
                ${tierBadgeHtml(activeAgent.buildTier)}
              </div>
              <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; margin:0 0 6px;">${esc(activeAgent.name)}</h2>
              <p style="font-size:14px; color:var(--text-secondary); margin:0 0 12px;">${esc(activeAgent.shortDesc)}</p>
              <div style="font-size:12px; font-weight:700; color:var(--text-muted); margin-bottom:6px;">Personas Served:</div>
              <div class="persona-chip-row" style="margin-bottom:14px;">
                ${activeAgent.personasServed.map(per => `<span class="persona-mini-chip">👤 ${esc(per)}</span>`).join('')}
              </div>
              <div style="padding:12px; border-radius:12px; background:var(--bg-surface-alt); margin-bottom:14px; font-size:13px;">
                <strong>Target Impact:</strong> ${esc(activeAgent.outcomeBadge)} (${esc(activeAgent.baselineVsTarget)})
              </div>
              <button type="button" class="hero-cta-btn hero-cta-primary" onclick="openAgentPage('${activeAgent.id}', true)">Inspect Full Agent Studio &rarr;</button>
            ` : ''}
          </div>
        </div>
      `;
    }

    /* =========================================================================
       10. HASH ROUTER & BOOTSTRAP
       ========================================================================= */
    function handleUrlHash() {
      const rawHash = (window.location.hash || '').trim();
      const h = rawHash.startsWith('#vc/') ? '#process/' + rawHash.slice(4) : rawHash;
      if (h === '#slides' || h === '#slides/v2') return openSlidesPage(currentSlideIdx, false, 'v2');
      if (h === '#slides/v1') return openSlidesPage(currentSlideIdx, false, 'v1');
      if (h.startsWith('#slide/v1/')) {
        const n = parseInt(h.slice('#slide/v1/'.length), 10);
        return openSlidesPage(!Number.isNaN(n) && n >= 1 ? n - 1 : 0, false, 'v1');
      }
      if (h.startsWith('#slide/v2/')) {
        const n = parseInt(h.slice('#slide/v2/'.length), 10);
        return openSlidesPage(!Number.isNaN(n) && n >= 1 ? n - 1 : 0, false, 'v2');
      }
      if (h.startsWith('#slide/')) {
        const n = parseInt(h.slice('#slide/'.length), 10);
        if (!Number.isNaN(n) && n >= 1) return openSlidesPage(n - 1, false);
        return openSlidesPage(0, false);
      }
      if (h === '#matrix') return openMatrixPage(false);
      if (h === '#architecture') return openArchitecturePage(false);
      if (h === '#mindmap') return openMindMapPage(false);
      if (h.startsWith('#agent/')) {
        const id = h.slice('#agent/'.length);
        if (AGENTS[id]) return openAgentPage(id, false);
      }
      if (h.startsWith('#process/')) {
        const id = h.slice('#process/'.length);
        if (VALUE_CHAINS[id]) return openValueChainPage(id, false);
      }
      if (h.startsWith('#pillar/')) {
        const id = h.slice('#pillar/'.length);
        if (PILLARS[id]) {
          selectedPillarId = id;
          showActivePage('pageHome');
          renderVerticalTabsBar();
          renderOrgChart();
          renderPillarShowcaseDrawer();
          const box = document.getElementById('deptShowcaseContainer');
          if (box) box.scrollIntoView({ behavior: 'auto', block: 'center' });
          return;
        }
      }
      showActivePage('pageHome');
      if (h === '#processes') {
        setTimeout(() => {
          const el = document.getElementById('processJourneysSection');
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 60);
      } else if (h === '#org') {
        setTimeout(() => {
          const el = document.getElementById('orgChartSection');
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 60);
      }
    }

    document.addEventListener('click', (ev) => {
      const menu = document.getElementById('navQuickMenu');
      const wrap = document.querySelector('.nav-actions');
      if (menu && wrap && !wrap.contains(ev.target)) {
        menu.classList.remove('open');
      }
    });

    document.addEventListener('keydown', (ev) => {
      const slidesPage = document.getElementById('pageSlides');
      if (!slidesPage || !slidesPage.classList.contains('active')) return;
      if (ev.key === 'ArrowRight') stepSlide(1);
      if (ev.key === 'ArrowLeft') stepSlide(-1);
    });

    window.addEventListener('popstate', handleUrlHash);

    window.addEventListener('DOMContentLoaded', () => {
      initThemeDefaultLight();
      renderHomeSections();
      initHeroHrCanvas();
      handleUrlHash();
    });
"""
