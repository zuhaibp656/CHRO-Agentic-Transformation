"""Complete CSS styling for the CHRO Office Agentic Transformation Portal.

Combines the structural hierarchy & layout geometry of our agentic portal architecture
with the Google Cloud (`Cloudstyle 2.0 / Simple Light`) palette,
plus 16:9 Slide Presentation Mode & Print-to-PDF `@media print` rules.
Opens in Light Theme by default; preserves full Dark Theme toggle.
"""

PORTAL_CSS = r"""
    /* =========================================================================
       1. THEME TOKENS — SIMPLE LIGHT (DEFAULT) + DARK MODE OVERRIDES
       ========================================================================= */
    :root, html[data-theme="light"] {
      --bg-canvas: #f8f9fa;
      --bg-surface: #ffffff;
      --bg-surface-alt: #f1f3f4;
      --bg-card: #ffffff;
      --bg-card-hover: #f8fbff;
      --bg-ice-blue: #e8f0fe;
      --border-subtle: #e8eaed;
      --border-strong: #d2e3fc;
      --text-primary: #202124;
      --text-secondary: #3c4043;
      --text-muted: #5f6368;

      --g-blue: #4285f4;
      --g-cobalt: #185abc;
      --g-cobalt-deep: #174ea6;
      --g-red: #ea4335;
      --g-red-bg: #fce8e6;
      --g-yellow: #fbbc04;
      --g-amber: #e37400;
      --g-amber-bg: #fff2cc;
      --g-green: #34a853;
      --g-green-bg: #ceead6;
      --g-teal: #0097a7;
      --g-teal-bg: #e0f7fa;
      --g-purple: #7e57c2;
      --g-lavender: #cdbff7;
      --g-purple-bg: #e6e7fb;

      --hero-bg: linear-gradient(180deg, #ffffff 0%, #f4f8ff 65%, #eef3fc 100%);
      --nav-bg: rgba(255, 255, 255, 0.94);
      --shadow-sm: 0 2px 8px rgba(32, 33, 36, 0.06);
      --shadow-md: 0 10px 28px rgba(24, 90, 188, 0.09), 0 2px 8px rgba(60, 64, 67, 0.05);
      --shadow-lg: 0 20px 48px rgba(24, 90, 188, 0.14), 0 6px 16px rgba(60, 64, 67, 0.06);
      --ease-spring: cubic-bezier(0.22, 1, 0.36, 1);

      --font-display: 'Google Sans Display', 'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-sans: 'Google Sans Text', 'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    }

    html[data-theme="dark"] {
      --bg-canvas: #050811;
      --bg-surface: #0b111e;
      --bg-surface-alt: #11192c;
      --bg-card: #0e1628;
      --bg-card-hover: #141f36;
      --bg-ice-blue: rgba(66, 133, 244, 0.15);
      --border-subtle: rgba(255, 255, 255, 0.12);
      --border-strong: rgba(66, 133, 244, 0.42);
      --text-primary: #f8fafc;
      --text-secondary: #e2e8f0;
      --text-muted: #94a3b8;

      --g-red-bg: rgba(234, 67, 53, 0.14);
      --g-amber-bg: rgba(251, 188, 4, 0.14);
      --g-green-bg: rgba(52, 168, 83, 0.14);
      --g-teal-bg: rgba(0, 151, 167, 0.16);
      --g-purple-bg: rgba(126, 87, 194, 0.18);

      --hero-bg: radial-gradient(ellipse 80% 70% at 50% 20%, rgba(24, 90, 188, 0.22), #050811 75%);
      --nav-bg: rgba(7, 11, 22, 0.90);
      --shadow-sm: 0 4px 14px rgba(0, 0, 0, 0.35);
      --shadow-md: 0 14px 34px rgba(0, 0, 0, 0.48);
      --shadow-lg: 0 24px 56px rgba(0, 0, 0, 0.65);
    }

    *, *::before, *::after { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font-family: var(--font-sans);
      background: var(--bg-canvas);
      color: var(--text-primary);
      line-height: 1.58;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }

    a { color: inherit; text-decoration: none; }
    button { font-family: inherit; cursor: pointer; }

    /* =========================================================================
       2. NAVBAR
       ========================================================================= */
    .navbar {
      position: sticky;
      top: 0;
      z-index: 200;
      background: var(--nav-bg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-subtle);
      box-shadow: var(--shadow-sm);
    }

    .navbar-inner {
      max-width: 1440px;
      margin: 0 auto;
      padding: 8px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: nowrap;
    }
    @media (max-width: 1160px) { .navbar-inner { flex-wrap: wrap; } }

    .nav-brand {
      display: flex;
      align-items: center;
      gap: 9px;
      cursor: pointer;
      flex-shrink: 0;
    }

    .nav-csco-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 999px;
      background: var(--bg-ice-blue);
      border: 1px solid var(--border-strong);
      color: var(--g-cobalt);
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 0.02em;
      white-space: nowrap;
    }
    html[data-theme="dark"] .nav-csco-badge { color: #8ab4f8; }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 4px;
      flex-wrap: nowrap;
    }
    @media (max-width: 1160px) { .nav-links { flex-wrap: wrap; } }

    .nav-pill-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-secondary);
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 12.5px;
      font-weight: 600;
      white-space: nowrap;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }

    .nav-pill-btn:hover,
    .nav-pill-btn.active {
      background: var(--bg-ice-blue);
      color: var(--g-cobalt);
      border-color: var(--border-strong);
    }
    html[data-theme="dark"] .nav-pill-btn:hover,
    html[data-theme="dark"] .nav-pill-btn.active { color: #8ab4f8; }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 6px;
      position: relative;
      flex-shrink: 0;
    }

    .theme-toggle-btn {
      padding: 6px 11px;
      border-radius: 999px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      color: var(--text-secondary);
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s ease;
    }
    .theme-toggle-btn:hover { border-color: var(--g-blue); color: var(--g-blue); }

    .pptx-download-btn {
      padding: 6px 12px;
      border-radius: 999px;
      border: 1px solid var(--g-cobalt);
      background: var(--g-cobalt);
      color: #ffffff;
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      box-shadow: 0 4px 12px rgba(24, 90, 188, 0.22);
      transition: transform 0.2s var(--ease-spring), background 0.2s ease;
    }
    .pptx-download-btn:hover { transform: translateY(-1px); background: var(--g-blue); border-color: var(--g-blue); }

    .nav-quick-menu {
      position: absolute;
      top: calc(100% + 10px);
      right: 0;
      width: 340px;
      max-height: 76vh;
      overflow-y: auto;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      border-radius: 18px;
      padding: 12px;
      box-shadow: var(--shadow-lg);
      display: none;
      z-index: 300;
    }
    .nav-quick-menu.open { display: block; animation: fluidPop 0.2s var(--ease-spring) both; }
    .nav-quick-group-title {
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
      padding: 10px 8px 6px;
      margin-top: 4px;
      border-top: 1px solid var(--border-subtle);
    }
    .nav-quick-group-title:first-child { border-top: none; margin-top: 0; }
    .nav-quick-item {
      width: 100%;
      text-align: left;
      background: transparent;
      border: none;
      color: var(--text-primary);
      padding: 8px 10px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .nav-quick-item:hover { background: var(--bg-ice-blue); color: var(--g-cobalt); }
    html[data-theme="dark"] .nav-quick-item:hover { color: #8ab4f8; }

    /* =========================================================================
       3. PAGE ISOLATION & TRANSITIONS
       ========================================================================= */
    .page-view { display: none; min-height: calc(100vh - 64px); }
    .page-view.active { display: block; animation: fluidPop 0.16s var(--ease-spring) both; }

    @keyframes fluidPop {
      from { opacity: 1; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @keyframes dashFlow {
      to { stroke-dashoffset: -36; }
    }

    /* =========================================================================
       4. HERO COMMAND CENTER (CLOUDSTYLE 2.0 SIMPLE LIGHT)
       ========================================================================= */
    .hero-section {
      position: relative;
      min-height: 76vh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 72px 24px 64px;
      background: var(--hero-bg);
      border-bottom: 1px solid var(--border-subtle);
      overflow: hidden;
    }

    .hero-aurora-backdrop {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 1;
      background:
        radial-gradient(circle 540px at 14% 24%, rgba(66, 133, 244, 0.14), transparent 72%),
        radial-gradient(circle 560px at 85% 28%, rgba(172, 135, 235, 0.16), transparent 72%),
        radial-gradient(circle 500px at 22% 80%, rgba(52, 168, 83, 0.11), transparent 70%),
        radial-gradient(circle 500px at 82% 80%, rgba(251, 188, 4, 0.11), transparent 72%);
    }

    #heroHrCanvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 2;
      pointer-events: none;
    }

    .hero-content {
      position: relative;
      z-index: 5;
      max-width: 1040px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .hero-logo-lockup {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 8px 20px;
      border-radius: 999px;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      box-shadow: var(--shadow-sm);
      margin-bottom: 24px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-secondary);
    }

    .hero-title {
      font-family: var(--font-display);
      font-size: clamp(38px, 5vw, 66px);
      font-weight: 800;
      line-height: 1.08;
      letter-spacing: -0.028em;
      color: var(--text-primary);
      margin: 0 0 18px 0;
    }

    .hero-title .gradient-word {
      background: linear-gradient(92deg, #185abc 0%, #4285f4 36%, #7e57c2 68%, #ea4335 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    html[data-theme="dark"] .hero-title .gradient-word {
      background: linear-gradient(92deg, #8ab4f8 0%, #cdbff7 48%, #81c995 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
      font-size: clamp(16.5px, 1.8vw, 20.5px);
      color: var(--text-secondary);
      max-width: 860px;
      line-height: 1.62;
      margin: 0 0 30px 0;
    }

    .hero-cta-row {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
      margin-bottom: 28px;
    }

    .hero-cta-btn {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 13px 26px;
      border-radius: 999px;
      font-size: 14.5px;
      font-weight: 700;
      border: 1px solid transparent;
      transition: transform 0.28s var(--ease-spring), box-shadow 0.28s ease;
    }
    .hero-cta-primary {
      background: var(--g-cobalt);
      color: #ffffff;
      box-shadow: 0 10px 26px rgba(24, 90, 188, 0.28);
    }
    .hero-cta-primary:hover { transform: translateY(-2px); background: var(--g-blue); }

    .hero-cta-secondary {
      background: var(--bg-surface);
      color: var(--text-primary);
      border-color: var(--border-strong);
      box-shadow: var(--shadow-sm);
    }
    .hero-cta-secondary:hover { transform: translateY(-2px); background: var(--bg-ice-blue); color: var(--g-cobalt); }
    html[data-theme="dark"] .hero-cta-secondary:hover { color: #8ab4f8; }

    .four-color-bar {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      width: 190px;
      height: 5px;
      border-radius: 999px;
      overflow: hidden;
      gap: 3px;
    }
    .four-color-bar span { display: block; height: 100%; border-radius: 999px; }

    .hero-kpi-strip {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      width: 100%;
      margin-top: 30px;
    }
    @media (max-width: 820px) { .hero-kpi-strip { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 480px) { .hero-kpi-strip { grid-template-columns: 1fr; } }

    .hero-kpi-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 14px 16px;
      text-align: left;
      box-shadow: var(--shadow-sm);
    }
    .hero-kpi-val {
      font-family: var(--font-display);
      font-size: clamp(19px, 1.75vw, 22px);
      font-weight: 800;
      color: var(--g-cobalt);
      white-space: nowrap;
    }
    html[data-theme="dark"] .hero-kpi-val { color: #8ab4f8; }
    .hero-kpi-lbl { font-size: 12.5px; color: var(--text-muted); font-weight: 600; margin-top: 2px; }

    /* =========================================================================
       5. SECTIONS, HR PARADOX BAND & CHRO ORG CHART TREE
       ========================================================================= */
    .org-section,
    .subpage-container {
      max-width: 1340px;
      margin: 0 auto;
      padding: 44px 24px 72px;
    }

    .section-header { text-align: center; max-width: 860px; margin: 0 auto 28px; }
    .section-title {
      font-family: var(--font-display);
      font-size: clamp(26px, 3vw, 36px);
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text-primary);
      margin: 0 0 8px 0;
    }
    .section-subtitle { font-size: 15.5px; color: var(--text-muted); margin: 0; }

    /* HR Paradox Proportional Split Panel */
    .paradox-panel {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 22px;
      padding: 26px 28px;
      box-shadow: var(--shadow-md);
      margin-bottom: 40px;
    }

    .paradox-bar-wrap {
      display: flex;
      height: 36px;
      border-radius: 12px;
      overflow: hidden;
      margin: 16px 0 18px;
      border: 1px solid var(--border-subtle);
    }
    .paradox-seg {
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-size: 11.5px;
      font-weight: 800;
      white-space: nowrap;
      overflow: hidden;
      padding: 0 6px;
      transition: filter 0.2s ease;
    }
    .paradox-seg:hover { filter: brightness(1.08); }

    .paradox-grid {
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 20px;
      margin-top: 12px;
    }
    @media (max-width: 880px) { .paradox-grid { grid-template-columns: 1fr; } }

    .paradox-col-card {
      padding: 18px 20px;
      border-radius: 16px;
      border: 1px solid var(--border-subtle);
    }

    /* 6-Pillar Master Tab Bar */
    .vertical-tabs-nav-bar {
      display: grid;
      grid-template-columns: repeat(7, minmax(0, 1fr));
      gap: 10px;
      padding: 12px;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      border-radius: 18px;
      box-shadow: var(--shadow-sm);
      margin-bottom: 28px;
    }
    @media (max-width: 1120px) { .vertical-tabs-nav-bar { grid-template-columns: repeat(4, 1fr); } }
    @media (max-width: 640px) { .vertical-tabs-nav-bar { grid-template-columns: repeat(2, 1fr); } }

    .v-tab-btn {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      text-align: left;
      gap: 3px;
      padding: 10px 12px;
      border-radius: 12px;
      background: var(--bg-surface-alt);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      transition: all 0.22s var(--ease-spring);
    }
    .v-tab-btn:hover {
      background: var(--bg-surface);
      border-color: var(--v-accent, var(--g-blue));
      transform: translateY(-2px);
    }
    .v-tab-btn.active {
      background: var(--bg-ice-blue);
      border-color: var(--v-accent, var(--g-blue));
      box-shadow: 0 6px 16px rgba(66, 133, 244, 0.16);
    }
    .v-tab-num { font-family: var(--font-mono); font-size: 10.5px; font-weight: 800; color: var(--v-accent, var(--g-blue)); }
    .v-tab-title { font-family: var(--font-display); font-size: 13px; font-weight: 800; color: var(--text-primary); line-height: 1.25; }
    .v-tab-tag { font-size: 11px; color: var(--text-muted); font-weight: 600; }

    /* CHRO Root Node */
    .cfo-root-wrapper { display: flex; flex-direction: column; align-items: center; }

    .cfo-box {
      display: flex;
      align-items: center;
      gap: 20px;
      padding: 20px 34px 20px 22px;
      border-radius: 22px;
      background: var(--bg-surface);
      border: 2px solid var(--g-blue);
      box-shadow: var(--shadow-md);
      max-width: 780px;
      width: 100%;
      transition: transform 0.3s var(--ease-spring), box-shadow 0.3s ease;
    }
    .cfo-box:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }

    .cfo-sc-emblem {
      width: 84px;
      height: 64px;
      border-radius: 14px;
      background: var(--bg-ice-blue);
      border: 1px solid var(--border-strong);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .cfo-box-title {
      font-family: var(--font-display);
      font-size: 22px;
      font-weight: 800;
      color: var(--text-primary);
    }
    .cfo-box-sub { font-size: 14.5px; color: var(--text-muted); margin-top: 3px; }

    .org-connectors { width: 100%; max-width: 1200px; height: 54px; display: block; }
    @media (max-width: 680px) { .org-connectors { display: none; } .cfo-box { margin-bottom: 22px; } }

    /* 6 Pillar Cards (3x2 Grid matching Supply Chain) */
    .dept-row {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 20px;
      width: 100%;
    }
    @media (max-width: 1060px) { .dept-row { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 680px) { .dept-row { grid-template-columns: 1fr; } }

    .dept-node {
      position: relative;
      padding: 22px 22px 20px;
      border-radius: 20px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-top: 4px solid var(--dept-accent, var(--g-blue));
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
      min-height: 290px;
      transition: transform 0.3s var(--ease-spring), box-shadow 0.3s ease, border-color 0.25s ease;
    }
    .dept-node:hover,
    .dept-node.active {
      transform: translateY(-4px);
      border-color: var(--dept-accent, var(--g-blue));
      box-shadow: var(--shadow-lg), 0 0 0 1.5px var(--dept-accent, var(--g-blue));
    }

    .dept-node-title {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 800;
      color: var(--text-primary);
      margin-bottom: 6px;
      line-height: 1.22;
    }
    .dept-node-sub { font-size: 13.5px; color: var(--text-muted); line-height: 1.5; }

    .dept-anim-stage {
      position: relative;
      height: 136px;
      border-radius: 14px;
      background: var(--bg-surface-alt);
      border: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      padding: 8px 10px 28px;
    }
    .dept-anim-stage svg { width: 100%; height: 100%; max-height: 112px; }

    .dept-anim-meta {
      position: absolute;
      left: 10px;
      bottom: 8px;
      font-size: 11px;
      font-weight: 700;
      color: var(--text-secondary);
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      padding: 3px 9px;
      border-radius: 999px;
    }
    .dept-anim-cta {
      position: absolute;
      right: 10px;
      bottom: 8px;
      font-size: 11px;
      font-weight: 800;
      color: var(--dept-accent, var(--g-blue));
      background: var(--bg-surface);
      border: 1px solid var(--dept-accent, var(--g-blue));
      padding: 3px 9px;
      border-radius: 999px;
    }
    .dept-node:hover .dept-anim-cta,
    .dept-node.active .dept-anim-cta {
      background: var(--dept-accent, var(--g-blue));
      color: #ffffff;
    }

    /* =========================================================================
       6. PROGRESSIVE PILLAR SHOWCASE DRAWER
       ========================================================================= */
    .dept-showcase-box {
      margin-top: 28px;
      border-radius: 22px;
      background: var(--bg-surface);
      border: 1.5px solid var(--dept-accent, var(--g-blue));
      padding: 30px;
      box-shadow: var(--shadow-lg);
      animation: fluidPop 0.34s var(--ease-spring) both;
    }

    .showcase-header {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      padding-bottom: 18px;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 20px;
    }
    .showcase-dept-name {
      font-family: var(--font-display);
      font-size: clamp(22px, 2.4vw, 28px);
      font-weight: 800;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .pillar-flow-strip {
      padding: 16px 18px;
      border-radius: 16px;
      background: var(--bg-surface-alt);
      border: 1px solid var(--border-subtle);
      margin-bottom: 22px;
    }
    .pillar-flow-steps {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 10px;
      margin-top: 10px;
    }
    @media (max-width: 960px) { .pillar-flow-steps { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 540px) { .pillar-flow-steps { grid-template-columns: 1fr; } }

    .flow-step-card {
      padding: 12px;
      border-radius: 12px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-top: 3px solid var(--dept-accent, var(--g-blue));
    }

    .showcase-compare-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
      margin-bottom: 24px;
    }
    @media (max-width: 820px) { .showcase-compare-grid { grid-template-columns: 1fr; } }

    .compare-card {
      padding: 20px;
      border-radius: 16px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface-alt);
    }

    .agent-cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 16px;
    }

    .agent-card {
      padding: 20px;
      border-radius: 18px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-left: 4px solid var(--dept-accent, var(--g-blue));
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      transition: transform 0.25s var(--ease-spring), box-shadow 0.25s ease, border-color 0.2s ease;
    }
    .agent-card:hover {
      transform: translateY(-3px);
      border-color: var(--dept-accent, var(--g-blue));
      box-shadow: var(--shadow-md);
    }

    .build-tier-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      white-space: nowrap;
    }
    .tier-nocode { background: var(--g-green-bg); color: #137333; border: 1px solid rgba(52, 168, 83, 0.45); }
    html[data-theme="dark"] .tier-nocode { color: #81c995; }
    .tier-lowcode { background: var(--bg-ice-blue); color: var(--g-cobalt); border: 1px solid rgba(66, 133, 244, 0.45); }
    html[data-theme="dark"] .tier-lowcode { color: #8ab4f8; }
    .tier-highcode { background: var(--g-purple-bg); color: #5e35b1; border: 1px solid rgba(126, 87, 194, 0.45); }
    html[data-theme="dark"] .tier-highcode { color: #cdbff7; }

    .persona-chip-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
    .persona-mini-chip {
      font-size: 11px;
      font-weight: 600;
      padding: 3px 9px;
      border-radius: 999px;
      background: var(--bg-surface-alt);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
    }

    /* =========================================================================
       7. END-TO-END VALUE CHAINS SECTION & AGENT DEEP-DIVE STUDIO
       ========================================================================= */
    .vc-home-block { margin-top: 56px; padding-top: 38px; border-top: 1px solid var(--border-subtle); }
    .vc-entry-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
    @media (max-width: 860px) { .vc-entry-grid { grid-template-columns: 1fr; } }

    .vc-entry-card {
      padding: 22px;
      border-radius: 20px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-top: 4px solid var(--vc-accent, var(--g-blue));
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
      transition: transform 0.28s var(--ease-spring), box-shadow 0.28s ease;
    }
    .vc-entry-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); border-color: var(--vc-accent, var(--g-blue)); }

    .vc-mini-pipeline { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-top: 8px; }
    .vc-mini-stage-pill {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 9px;
      border-radius: 8px;
      background: var(--bg-surface-alt);
      border: 1px solid var(--border-subtle);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-primary);
    }
    .st-idx { color: var(--vc-accent, var(--g-blue)); font-family: var(--font-mono); }

    .back-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 22px;
    }
    .back-btn,
    .switch-pill {
      padding: 8px 14px;
      border-radius: 999px;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      color: var(--text-primary);
      font-size: 12.5px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .back-btn:hover,
    .switch-pill:hover,
    .switch-pill.active {
      background: var(--bg-ice-blue);
      color: var(--g-cobalt);
      border-color: var(--g-blue);
    }
    html[data-theme="dark"] .switch-pill.active { color: #8ab4f8; }

    .simple-arch-card {
      padding: 24px 26px;
      border-radius: 20px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      box-shadow: var(--shadow-md);
      margin-bottom: 24px;
    }

    .vc-pipeline-strip-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }
    .vc-pipe-step-card {
      padding: 15px;
      border-radius: 14px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-top: 3.5px solid var(--st-color, var(--g-blue));
      cursor: pointer;
      transition: all 0.22s ease;
    }
    .vc-pipe-step-card:hover,
    .vc-pipe-step-card.active {
      background: var(--bg-ice-blue);
      border-color: var(--st-color, var(--g-blue));
      transform: translateY(-2px);
    }

    /* =========================================================================
       8. KEYNOTE SLIDES (16:9 PPTX-READY VIEW) & PRINT CSS
       ========================================================================= */
    .slides-toolbar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 14px 18px;
      border-radius: 16px;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      box-shadow: var(--shadow-sm);
      margin-bottom: 20px;
    }

    .keynote-stage-shell {
      display: grid;
      grid-template-columns: 240px minmax(0, 1fr);
      gap: 20px;
      align-items: start;
    }
    @media (max-width: 960px) { .keynote-stage-shell { grid-template-columns: 1fr; } }

    .slide-rail {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 10px;
      max-height: 700px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .slide-rail-item {
      width: 100%;
      text-align: left;
      padding: 8px 10px;
      border-radius: 10px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-secondary);
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: flex-start;
      gap: 8px;
    }
    .slide-rail-item:hover { background: var(--bg-surface-alt); }
    .slide-rail-item.active { background: var(--bg-ice-blue); border-color: var(--g-blue); color: var(--g-cobalt); font-weight: 700; }

    /* True 16:9 Slide Canvas (Always Crisp Light Theme Matching PPTX Deck) */
    .keynote-slide-frame {
      position: relative;
      width: 100%;
      aspect-ratio: 16 / 9;
      min-height: 550px;
      background: #ffffff;
      color: #202124;
      border-radius: 16px;
      border: 1px solid #d2e3fc;
      box-shadow: var(--shadow-lg);
      padding: 20px 26px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }

    .slide-chevron-strip {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 4px;
      margin-bottom: 10px;
    }
    .slide-chevron-step {
      padding: 8px 10px 8px 18px;
      color: #ffffff;
      clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 50%, calc(100% - 12px) 100%, 0 100%, 10px 50%);
      display: flex;
      flex-direction: column;
      justify-content: center;
      text-align: center;
      min-height: 40px;
    }
    .slide-chevron-step:first-child {
      padding-left: 12px;
      clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 50%, calc(100% - 12px) 100%, 0 100%);
      border-radius: 6px 0 0 6px;
    }
    .slide-img-card {
      background: #ffffff;
      border: 1px solid #e8eaed;
      border-radius: 12px;
      padding: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }
    .slide-img-card img {
      max-width: 100%;
      max-height: 100%;
      width: auto;
      height: auto;
      object-fit: contain;
      display: block;
    }
    .slide-flow-arrow {
      display: flex;
      align-items: center;
      justify-content: center;
      color: #185abc;
      font-weight: 900;
      font-size: 20px;
    }

    .slide-four-bar {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 8px;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
    }

    .slides-overview-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(520px, 1fr));
      gap: 24px;
    }
    @media (max-width: 600px) { .slides-overview-grid { grid-template-columns: 1fr; } }

    .speaker-notes-box {
      margin-top: 14px;
      padding: 14px 18px;
      border-radius: 12px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      font-size: 13.5px;
    }

    /* =========================================================================
       9. PERIODIC AGENT MATRIX & PLATFORM PROOF TABLES
       ========================================================================= */
    .matrix-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
      gap: 14px;
    }
    .matrix-cell {
      padding: 16px;
      border-radius: 16px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-top: 4px solid var(--cell-accent, var(--g-blue));
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
      transition: transform 0.22s var(--ease-spring), box-shadow 0.22s ease;
    }
    .matrix-cell:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); border-color: var(--cell-accent, var(--g-blue)); }

    .data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
      background: var(--bg-surface);
      border-radius: 14px;
      overflow: hidden;
      border: 1px solid var(--border-subtle);
    }
    .data-table th {
      background: var(--bg-surface-alt);
      color: var(--text-primary);
      font-weight: 700;
      text-align: left;
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-subtle);
    }
    .data-table td {
      padding: 11px 14px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      vertical-align: top;
    }

    /* Mind Map Flow */
    .mindmap-columns {
      display: grid;
      grid-template-columns: 240px 280px minmax(0, 1fr);
      gap: 18px;
      align-items: start;
    }
    @media (max-width: 980px) { .mindmap-columns { grid-template-columns: 1fr; } }

    .mindmap-col {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 18px;
      box-shadow: var(--shadow-sm);
    }

    /* =========================================================================
       10. PRINT TO PDF 16:9 SLIDE EXPORT MODE
       ========================================================================= */
    @page {
      size: 13.333in 7.5in landscape;
      margin: 0;
    }
    @media print {
      .navbar, .slides-toolbar, .slide-rail, .speaker-notes-box, .no-print { display: none !important; }
      body, html { background: #ffffff !important; margin: 0 !important; padding: 0 !important; }
      .subpage-container { max-width: none !important; padding: 0 !important; margin: 0 !important; }
      .keynote-stage-shell { display: block !important; }
      .slides-overview-grid { display: block !important; }
      .keynote-slide-frame {
        width: 13.333in !important;
        height: 7.5in !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        page-break-after: always !important;
        break-after: page !important;
      }
    }

    /* =========================================================================
       CLOUDSTYLE 2.0 / SIMPLE LIGHT ALIGNMENT + ARCHITECTURE SUITE
       ========================================================================= */
    :root {
      --bg-canvas: #f8f9fa;
      --bg-surface: #ffffff;
      --bg-surface-alt: #f1f3f4;
      --bg-ice-blue: #e8f0fe;
      --border-subtle: #e8eaed;
      --border-strong: #d2e3fc;
      --g-blue: #4285f4;
      --g-cobalt: #185abc;
      --g-purple: #5e35b1;
      --g-lavender: #e6e7fb;
      --shadow-sm: 0 2px 6px rgba(60,64,67,0.06);
      --shadow-md: 0 8px 24px rgba(60,64,67,0.08);
      --shadow-lg: 0 16px 40px rgba(24,90,188,0.12);
    }

    html[data-theme="dark"] {
      --bg-canvas: #11161f;
      --bg-surface: #18202c;
      --bg-surface-alt: #1f2937;
      --bg-ice-blue: rgba(66,133,244,0.16);
      --border-subtle: rgba(255,255,255,0.10);
      --border-strong: rgba(138,180,248,0.34);
    }

    .hero {
      background:
        radial-gradient(circle at 12% 16%, rgba(232,240,254,0.95) 0%, transparent 46%),
        radial-gradient(circle at 86% 18%, rgba(230,231,251,0.72) 0%, transparent 44%),
        linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
    }

    html[data-theme="dark"] .hero {
      background:
        radial-gradient(circle at 12% 16%, rgba(66,133,244,0.18) 0%, transparent 46%),
        radial-gradient(circle at 86% 18%, rgba(172,135,235,0.14) 0%, transparent 44%),
        linear-gradient(180deg, #11161f 0%, #161d28 100%);
    }

    .hero-title .gradient-word {
      background: linear-gradient(135deg, #185abc 0%, #4285f4 58%, #5e35b1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    html[data-theme="dark"] .hero-title .gradient-word {
      background: linear-gradient(135deg, #8ab4f8 0%, #669df6 58%, #cdbff7 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .org-root-box {
      background: linear-gradient(135deg, #ffffff 0%, #e8f0fe 100%);
      border: 1.5px solid #d2e3fc;
      box-shadow: var(--shadow-md);
    }

    html[data-theme="dark"] .org-root-box {
      background: linear-gradient(135deg, #18202c 0%, rgba(66,133,244,0.18) 100%);
      border-color: rgba(138,180,248,0.36);
    }

    /* Calm Cloudstyle Pillar Cards */
    .dept-node.cs-pillar-card {
      background: var(--bg-surface);
      border: 1.5px solid var(--border-subtle);
      border-top: 3px solid var(--dept-accent, #4285f4);
      box-shadow: var(--shadow-sm);
    }

    .dept-node.cs-pillar-card:hover {
      border-color: #aecbfa;
      border-top-color: var(--dept-accent, #4285f4);
      box-shadow: var(--shadow-md);
    }

    .dept-node.cs-pillar-card.active {
      background: linear-gradient(180deg, var(--bg-ice-blue) 0%, var(--bg-surface) 100%);
      border-color: #4285f4;
      border-top-color: var(--dept-accent, #4285f4);
      box-shadow: 0 0 0 3px rgba(66,133,244,0.14), var(--shadow-md);
    }

    .dept-node.cs-pillar-card .dept-anim-cta {
      color: var(--g-cobalt);
    }

    html[data-theme="dark"] .dept-node.cs-pillar-card .dept-anim-cta {
      color: #8ab4f8;
    }

    .dept-node.cs-pillar-card.active .dept-anim-cta,
    .dept-node.cs-pillar-card:hover .dept-anim-cta {
      color: #ffffff !important;
    }

    /* Ultra-Clean Expanded Pillar Drawer */
    .simple-drawer-box {
      background: var(--bg-surface);
      border: 1.5px solid #d2e3fc;
      border-top: 4px solid var(--dept-accent, #4285f4);
      box-shadow: var(--shadow-md);
    }

    .drawer-count-pill {
      font-size: 12px;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 999px;
    }

    .agent-cards-simple {
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 14px;
    }

    .agent-card-simple {
      min-height: 122px;
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      background: var(--bg-surface);
      border: 1.5px solid var(--border-subtle);
      border-radius: 14px;
      transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
    }

    .agent-card-simple:hover {
      transform: translateY(-2px);
      border-color: #4285f4;
      box-shadow: var(--shadow-md);
    }

    .agent-card-simple-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .agent-num-chip {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 999px;
      letter-spacing: 0.3px;
    }

    .agent-card-simple-title {
      font-family: var(--font-display);
      font-size: 17.5px;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1.28;
    }

    .agent-card-simple-foot {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-top: 10px;
      border-top: 1px solid var(--border-subtle);
    }

    .agent-outcome-mini {
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-muted);
    }

    .agent-open-link {
      font-size: 12px;
      font-weight: 800;
      color: var(--g-cobalt);
      white-space: nowrap;
    }

    html[data-theme="dark"] .agent-open-link { color: #8ab4f8; }

    /* Agent Hero & Runtime Architecture 4-Stage Pipeline */
    .agent-hero-card {
      border-top: 4px solid var(--g-blue);
    }

    .agent-value-callout {
      padding: 16px 20px;
      border-radius: 14px;
      background: var(--bg-ice-blue);
      border: 1.5px solid var(--border-strong);
      min-width: 265px;
      max-width: 340px;
    }

    .arch-pipeline {
      display: grid;
      grid-template-columns: minmax(180px, 1fr) 26px minmax(210px, 1.12fr) 26px minmax(250px, 1.32fr) 26px minmax(200px, 1.05fr);
      gap: 8px;
      align-items: stretch;
      margin-bottom: 18px;
    }

    @media (max-width: 1080px) {
      .arch-pipeline {
        grid-template-columns: 1fr;
        gap: 10px;
      }
      .arch-flow-arrow {
        transform: rotate(90deg);
        padding: 4px 0;
      }
    }

    .arch-flow-arrow {
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      font-weight: 800;
      color: #4285f4;
    }

    .arch-stage-card {
      background: var(--bg-surface-alt);
      border: 1.5px solid var(--border-subtle);
      border-radius: 14px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .arch-stage-intake { border-top: 3px solid #4285f4; background: var(--bg-surface); }
    .arch-stage-brain {
      border-top: 3px solid #5e35b1;
      border-color: #d2e3fc;
      background: linear-gradient(180deg, #e8f0fe 0%, #f5f3ff 100%);
    }
    html[data-theme="dark"] .arch-stage-brain {
      background: linear-gradient(180deg, rgba(66,133,244,0.16) 0%, rgba(172,135,235,0.14) 100%);
      border-color: rgba(172,135,235,0.35);
    }
    .arch-stage-tools { border-top: 3px solid #007b83; background: var(--bg-surface); }
    .arch-stage-outcome { border-top: 3px solid #1e8e3e; background: var(--bg-surface); }

    .arch-stage-kicker {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 800;
      letter-spacing: 0.4px;
      color: var(--g-cobalt);
    }

    html[data-theme="dark"] .arch-stage-kicker { color: #8ab4f8; }

    .arch-stage-title {
      font-family: var(--font-display);
      font-size: 15.5px;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1.3;
    }

    .arch-node-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11.5px;
      font-weight: 700;
      padding: 6px 10px;
      border-radius: 8px;
      background: var(--bg-ice-blue);
      color: var(--g-cobalt);
      border: 1px solid var(--border-strong);
      line-height: 1.3;
    }

    html[data-theme="dark"] .arch-node-pill { color: #aecbfa; }

    .arch-pill-gemini {
      background: #e6e7fb;
      color: #4527a0;
      border-color: #cdbff7;
    }

    html[data-theme="dark"] .arch-pill-gemini {
      background: rgba(172,135,235,0.20);
      color: #e2d9ff;
      border-color: rgba(172,135,235,0.40);
    }

    .arch-pill-trust {
      background: #fef7e0;
      color: #b06000;
      border-color: #fad265;
    }

    html[data-theme="dark"] .arch-pill-trust {
      background: rgba(251,188,4,0.16);
      color: #fde293;
      border-color: rgba(251,188,4,0.35);
    }

    .arch-node-meta {
      font-size: 12.5px;
      color: var(--text-secondary);
      line-height: 1.45;
    }

    .arch-sub-label {
      font-size: 10.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.35px;
      color: var(--text-muted);
    }

    .arch-chip-stack {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }

    .arch-chip-item {
      display: flex;
      align-items: flex-start;
      gap: 6px;
      padding: 6px 8px;
      border-radius: 8px;
      background: var(--bg-surface-alt);
      border: 1px solid var(--border-subtle);
      font-size: 12px;
      font-weight: 600;
      color: var(--text-primary);
      line-height: 1.3;
    }

    .arch-chip-conn {
      background: #e4f7fb;
      border-color: #b2ebf2;
      color: #005b62;
    }

    html[data-theme="dark"] .arch-chip-conn {
      background: rgba(0,151,167,0.16);
      border-color: rgba(0,151,167,0.36);
      color: #80deea;
    }

    .arch-chip-idx {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 800;
      color: var(--g-cobalt);
      background: var(--bg-ice-blue);
      padding: 1px 5px;
      border-radius: 4px;
    }

    /* Plain English 3-Card Explainer + Execution Stepper */
    .plain-explainer-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }

    @media (max-width: 900px) {
      .plain-explainer-grid { grid-template-columns: 1fr; }
    }

    .plain-explainer-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 14px 16px;
    }

    .plain-explainer-num {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 800;
      color: var(--g-cobalt);
      margin-bottom: 4px;
      letter-spacing: 0.35px;
    }

    html[data-theme="dark"] .plain-explainer-num { color: #8ab4f8; }

    .plain-explainer-title {
      font-family: var(--font-display);
      font-size: 14.5px;
      font-weight: 800;
      color: var(--text-primary);
      margin-bottom: 4px;
    }

    .plain-explainer-card p {
      margin: 0;
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.48;
    }

    .tool-code-pill {
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 7px 11px;
      border-radius: 8px;
      background: var(--bg-surface-alt);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
    }

    .sample-prompt-box {
      padding: 12px 14px;
      border-radius: 12px;
      background: var(--bg-ice-blue);
      border: 1px solid var(--border-strong);
      font-size: 13.5px;
      color: var(--text-primary);
      margin-bottom: 14px;
      line-height: 1.5;
    }

    .trace-steps-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .trace-step-row {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      padding: 10px 12px;
      border-radius: 10px;
      background: var(--bg-surface-alt);
      border: 1px solid var(--border-subtle);
    }

    .trace-step-badge {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 6px;
      background: #e6f4ea;
      color: #137333;
      flex-shrink: 0;
      margin-top: 1px;
    }

    html[data-theme="dark"] .trace-step-badge {
      background: rgba(52,168,83,0.22);
      color: #81c995;
    }

    .trace-step-text {
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.45;
    }

    /* Platform 4-Layer Gemini Enterprise Reference Architecture (#architecture) */
    .stack-arch-layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 275px;
      gap: 16px;
      align-items: stretch;
      margin-top: 14px;
    }

    @media (max-width: 960px) {
      .stack-arch-layout { grid-template-columns: 1fr; }
    }

    .stack-layers-col {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .stack-layer-box {
      padding: 14px 18px;
      border-radius: 14px;
      border: 1.5px solid var(--border-strong);
      background: var(--bg-surface);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .stack-layer-top { background: #e8f0fe; border-color: #aecbfa; }
    .stack-layer-workbench { background: #ffffff; border-color: #4285f4; box-shadow: var(--shadow-sm); }
    .stack-layer-context { background: #e4f7fb; border-color: #b2ebf2; }
    .stack-layer-brains { background: #e6e7fb; border-color: #cdbff7; }

    html[data-theme="dark"] .stack-layer-top { background: rgba(66,133,244,0.16); border-color: rgba(138,180,248,0.35); }
    html[data-theme="dark"] .stack-layer-workbench { background: #18202c; border-color: #4285f4; }
    html[data-theme="dark"] .stack-layer-context { background: rgba(0,151,167,0.15); border-color: rgba(0,188,212,0.32); }
    html[data-theme="dark"] .stack-layer-brains { background: rgba(126,87,194,0.18); border-color: rgba(179,157,219,0.35); }

    .stack-layer-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
    }

    .stack-layer-title {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 800;
      color: var(--text-primary);
    }

    .stack-layer-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 999px;
      background: rgba(255,255,255,0.85);
      color: var(--g-cobalt);
    }

    html[data-theme="dark"] .stack-layer-tag {
      background: rgba(17,22,31,0.7);
      color: #aecbfa;
    }

    .stack-layer-desc {
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.45;
    }

    .stack-tier-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 6px;
    }

    .stack-tier-agents {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
    }

    .stack-agent-link {
      font-size: 12px;
      font-weight: 700;
      padding: 5px 10px;
      border-radius: 999px;
      background: var(--bg-surface-alt);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      cursor: pointer;
    }

    .stack-agent-link:hover {
      border-color: #4285f4;
      color: var(--g-cobalt);
      background: var(--bg-ice-blue);
    }

    .stack-shield-col {
      background: linear-gradient(180deg, #fef7e0 0%, #fffdf5 100%);
      border: 1.5px solid #fad265;
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
    }

    html[data-theme="dark"] .stack-shield-col {
      background: linear-gradient(180deg, rgba(251,188,4,0.16) 0%, rgba(251,188,4,0.08) 100%);
      border-color: rgba(251,188,4,0.38);
    }

    .stack-shield-item {
      background: var(--bg-surface);
      border: 1px solid #f5d67b;
      border-radius: 10px;
      padding: 10px 12px;
    }

    html[data-theme="dark"] .stack-shield-item {
      background: rgba(17,22,31,0.65);
      border-color: rgba(251,188,4,0.28);
    }

    .stack-shield-item strong {
      display: block;
      font-size: 12.5px;
      color: var(--text-primary);
      margin-bottom: 2px;
    }

    .stack-shield-item span {
      display: block;
      font-size: 11.5px;
      color: var(--text-secondary);
      line-height: 1.38;
    }

    /* ==============================================================
       HOW-IT-WORKS AGENT ARCHITECTURE UPGRADE (CLOUDSTYLE 2.0)
       ============================================================== */
    .hw-trigger-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px 14px;
      padding: 12px 16px;
      margin-bottom: 14px;
      border-radius: 12px;
      background: #E8F0FE;
      border: 1px solid #C5DAF8;
      border-left: 4px solid #4285F4;
    }
    .hw-trigger-badge {
      font-size: 10.5px;
      font-weight: 800;
      letter-spacing: 0.06em;
      color: #185ABC;
      background: #FFFFFF;
      border: 1px solid #C5DAF8;
      padding: 4px 9px;
      border-radius: 999px;
      white-space: nowrap;
    }
    .hw-trigger-text {
      flex: 1 1 320px;
      font-size: 13px;
      font-weight: 600;
      color: #202124;
      line-height: 1.4;
    }
    .hw-tier-tag {
      font-size: 11px;
      font-weight: 700;
      color: #5E35B1;
      background: #E6E7FB;
      border: 1px solid #D2D5F8;
      padding: 4px 10px;
      border-radius: 999px;
      white-space: nowrap;
    }
    .hw-pipeline {
      align-items: stretch;
    }
    .hw-stage-card {
      display: flex;
      flex-direction: column;
      gap: 8px;
      min-width: 0;
    }
    .hw-input-list,
    .hw-output-list {
      list-style: none;
      margin: 2px 0 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      gap: 7px;
    }
    .hw-input-list li,
    .hw-output-list li {
      display: flex;
      align-items: flex-start;
      gap: 7px;
      font-size: 12px;
      line-height: 1.42;
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 7px 9px;
    }
    .hw-bullet-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #4285F4;
      flex-shrink: 0;
      margin-top: 5px;
    }
    .hw-check-icon {
      color: #137333;
      font-weight: 800;
      font-size: 12px;
      flex-shrink: 0;
      margin-top: 1px;
    }
    .hw-mini-shield {
      margin-top: auto;
      font-size: 11px;
      line-height: 1.38;
      color: #185ABC;
      background: #E8F0FE;
      border: 1px solid #D2E3FC;
      border-radius: 8px;
      padding: 7px 9px;
      font-weight: 600;
    }
    .hw-steps-stack {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .hw-step-card {
      display: flex;
      align-items: flex-start;
      gap: 9px;
      background: #FFFFFF;
      border: 1px solid #D2D5F8;
      border-radius: 9px;
      padding: 8px 10px;
    }
    .hw-step-num {
      flex-shrink: 0;
      font-size: 10.5px;
      font-weight: 800;
      color: #FFFFFF;
      background: #5E35B1;
      border-radius: 6px;
      padding: 2px 6px;
      line-height: 1.4;
      margin-top: 1px;
    }
    .hw-step-body {
      min-width: 0;
    }
    .hw-step-title {
      font-size: 12px;
      font-weight: 700;
      color: #202124;
      margin-bottom: 2px;
      line-height: 1.3;
    }
    .hw-step-detail {
      font-size: 11.5px;
      color: #5F6368;
      line-height: 1.4;
    }
    .hw-io-split {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 2px;
    }
    .hw-io-group {
      background: rgba(255, 255, 255, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 9px;
      padding: 8px 9px;
    }
    .hw-io-label {
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }
    .hw-io-read-label {
      color: #185ABC;
    }
    .hw-io-write-label {
      color: #137333;
    }
    .hw-chip-group {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .hw-read-chip,
    .hw-write-chip {
      display: block;
      font-size: 11.5px;
      line-height: 1.36;
      padding: 5px 8px;
      border-radius: 6px;
      font-weight: 600;
    }
    .hw-read-chip {
      background: #E8F0FE;
      color: #174EA6;
      border: 1px solid #C5DAF8;
    }
    .hw-write-chip {
      background: #E6F4EA;
      color: #0D652D;
      border: 1px solid #CEEAD6;
    }
    .hw-human-box {
      margin-top: auto;
      background: #FEF7E0;
      border: 1px solid #F9DF96;
      border-left: 4px solid #F9AB00;
      border-radius: 8px;
      padding: 8px 10px;
    }
    .hw-human-title {
      font-size: 11px;
      font-weight: 800;
      color: #B06000;
      margin-bottom: 3px;
    }
    .hw-human-text {
      font-size: 11.5px;
      line-height: 1.4;
      color: #4A3800;
    }
    .hw-before-after-strip {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      gap: 12px;
      align-items: stretch;
      margin-top: 14px;
      margin-bottom: 14px;
    }
    .hw-ba-col {
      padding: 12px 14px;
      border-radius: 11px;
      border: 1px solid var(--border-subtle);
    }
    .hw-ba-before {
      background: #F8F9FA;
      border-left: 4px solid #5F6368;
    }
    .hw-ba-after {
      background: #E6F4EA;
      border-color: #CEEAD6;
      border-left: 4px solid #137333;
    }
    .hw-ba-kicker {
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.06em;
      margin-bottom: 5px;
      color: #5F6368;
    }
    .hw-ba-after .hw-ba-kicker {
      color: #0D652D;
    }
    .hw-ba-text {
      font-size: 12.5px;
      line-height: 1.45;
      color: #202124;
      font-weight: 500;
    }
    .hw-ba-arrow {
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      color: #4285F4;
      background: #E8F0FE;
      border: 1px solid #C5DAF8;
      width: 34px;
      height: 34px;
      align-self: center;
      border-radius: 50%;
    }
    @media (max-width: 960px) {
      .hw-before-after-strip {
        grid-template-columns: 1fr;
      }
      .hw-ba-arrow {
        margin: 0 auto;
        transform: rotate(90deg);
      }
    }
    html[data-theme="dark"] .hw-trigger-bar {
      background: rgba(66, 133, 244, 0.14);
      border-color: rgba(138, 180, 248, 0.35);
    }
    html[data-theme="dark"] .hw-trigger-badge {
      background: #1B2432;
      color: #8AB4F8;
      border-color: rgba(138, 180, 248, 0.35);
    }
    html[data-theme="dark"] .hw-trigger-text,
    html[data-theme="dark"] .hw-step-title,
    html[data-theme="dark"] .hw-ba-text {
      color: #E8EAED;
    }
    html[data-theme="dark"] .hw-tier-tag {
      background: rgba(167, 139, 250, 0.18);
      color: #D2C4FA;
      border-color: rgba(167, 139, 250, 0.35);
    }
    html[data-theme="dark"] .hw-input-list li,
    html[data-theme="dark"] .hw-output-list li,
    html[data-theme="dark"] .hw-step-card,
    html[data-theme="dark"] .hw-io-group {
      background: #1A222E;
      border-color: rgba(255, 255, 255, 0.12);
    }
    html[data-theme="dark"] .hw-step-detail {
      color: #B4BECB;
    }
    html[data-theme="dark"] .hw-mini-shield,
    html[data-theme="dark"] .hw-read-chip {
      background: rgba(66, 133, 244, 0.16);
      color: #AECBFA;
      border-color: rgba(138, 180, 248, 0.32);
    }
    html[data-theme="dark"] .hw-write-chip {
      background: rgba(52, 168, 83, 0.16);
      color: #A8DAB5;
      border-color: rgba(129, 201, 149, 0.32);
    }
    html[data-theme="dark"] .hw-io-read-label {
      color: #8AB4F8;
    }
    html[data-theme="dark"] .hw-io-write-label,
    html[data-theme="dark"] .hw-check-icon,
    html[data-theme="dark"] .hw-ba-after .hw-ba-kicker {
      color: #81C995;
    }
    html[data-theme="dark"] .hw-human-box {
      background: rgba(251, 188, 4, 0.14);
      border-color: rgba(253, 214, 99, 0.35);
    }
    html[data-theme="dark"] .hw-human-title {
      color: #FDD663;
    }
    html[data-theme="dark"] .hw-human-text {
      color: #FCE8B2;
    }
    html[data-theme="dark"] .hw-ba-before {
      background: #1A222E;
      border-color: rgba(255, 255, 255, 0.14);
      border-left-color: #9AA0A6;
    }
    html[data-theme="dark"] .hw-ba-after {
      background: rgba(52, 168, 83, 0.14);
      border-color: rgba(129, 201, 149, 0.35);
      border-left-color: #81C995;
    }
    html[data-theme="dark"] .hw-ba-kicker {
      color: #9AA0A6;
    }
    html[data-theme="dark"] .hw-ba-arrow {
      background: rgba(66, 133, 244, 0.18);
      color: #8AB4F8;
      border-color: rgba(138, 180, 248, 0.35);
    }

    /* =========================================================================
       KEYNOTE DECK VERSION SWITCHER & v2 SLIDE LAYOUTS
       ========================================================================= */
    .deck-version-switcher {
      display: inline-flex;
      align-items: center;
      padding: 4px;
      border-radius: 999px;
      background: var(--bg-surface-alt);
      border: 1px solid var(--border-strong);
      gap: 4px;
    }
    .deck-ver-pill {
      border: none;
      background: transparent;
      color: var(--text-secondary);
      font-size: 12px;
      font-weight: 700;
      padding: 7px 14px;
      border-radius: 999px;
      cursor: pointer;
      transition: all 0.18s ease;
      white-space: nowrap;
    }
    .deck-ver-pill:hover { color: var(--g-cobalt); }
    .deck-ver-pill.active {
      background: #1a73e8;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(26, 115, 232, 0.28);
    }
    html[data-theme="dark"] .deck-ver-pill.active {
      background: #8ab4f8;
      color: #0b1426;
    }

    /* Mind Map Slide Layout (v2 Slides 07 & 08) */
    .mm-slide-grid {
      display: grid;
      grid-template-columns: 162px 24px minmax(0, 1fr);
      gap: 6px;
      flex: 1;
      min-height: 0;
      align-items: stretch;
    }
    .mm-hub-card {
      border-radius: 14px;
      background: linear-gradient(160deg, #e8f0fe 0%, #f8f9fa 100%);
      border: 1.5px solid #4285f4;
      padding: 12px 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      text-align: center;
    }
    .mm-branches-col {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
      min-height: 0;
    }
    .mm-branch-row {
      flex: 1;
      display: grid;
      grid-template-columns: 185px 22px minmax(0, 1fr);
      align-items: stretch;
      gap: 6px;
      min-height: 0;
    }
    .mm-pillar-node {
      border-radius: 12px;
      padding: 8px 10px;
      display: flex;
      align-items: center;
      gap: 8px;
      background: #f8f9fa;
      border: 1.5px solid #d2e3fc;
    }
    .mm-agents-row {
      display: grid;
      gap: 8px;
      min-height: 0;
    }
    .mm-agent-node {
      border-radius: 11px;
      padding: 8px 10px;
      background: #ffffff;
      border: 1px solid #d2e3fc;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 8px;
      cursor: pointer;
      transition: transform 0.16s ease, box-shadow 0.16s ease;
    }
    .mm-agent-node:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 10px rgba(26, 115, 232, 0.14);
    }
    .mm-persona-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }
    .mm-persona-chip {
      font-size: 9px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 999px;
      background: #f1f3f4;
      color: #3c4043;
      border: 1px solid #e0e3e7;
      line-height: 1.2;
    }

    /* v2 Business Value & Pillars Layouts (Slides 05, 06, 07-09, 16) */
    .tp-levers-bar {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 10px;
    }
    .tp-lever-pill {
      padding: 8px 10px;
      border-radius: 10px;
      background: #f8f9fa;
      border: 1px solid #e8eaed;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .tp-grid-4x2 {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      flex: 1;
      min-height: 0;
    }
    .tp-card {
      padding: 13px 14px;
      border-radius: 12px;
      background: #ffffff;
      border: 1px solid #d2e3fc;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 10px;
    }
    .pf-grid-3x2 {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 11px;
      flex: 1;
      min-height: 0;
    }
    .pf-card {
      padding: 11px 12px;
      border-radius: 12px;
      background: #f8f9fa;
      border: 1px solid #d2e3fc;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 7px;
      cursor: pointer;
    }
    .pf-fn-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 5px;
    }
    .pf-fn-pill {
      padding: 4px 6px;
      border-radius: 7px;
      background: #ffffff;
      border: 1px solid #e0e3e7;
      font-size: 9.5px;
      font-weight: 700;
      color: #3c4043;
      text-align: center;
      line-height: 1.2;
    }
    .pv-pair-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      flex: 1;
      min-height: 0;
    }
    .pv-col-card {
      padding: 14px 15px;
      border-radius: 14px;
      background: #ffffff;
      border: 1.5px solid #d2e3fc;
      display: flex;
      flex-direction: column;
      gap: 11px;
    }
    .pv-strip {
      flex: 1;
      display: flex;
      align-items: center;
      padding: 10px 13px;
      border-radius: 10px;
      font-size: 11.5px;
      color: #202124;
      line-height: 1.4;
    }
"""
