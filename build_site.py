#!/usr/bin/env python3
"""Build the Office of the CHRO HR Agentic Transformation Website & Keynote Portal.

Compiles single-source catalog (`data/hr_catalog.json`) + `portal_styles.py` + `portal_scripts.py` into:
  - index.html      (Main Executive Portal — opens in Light Theme by default)
  - slides.html     (16:9 Widescreen 20-Slide Keynote View + PDF & PPTX Export)
  - matrix.html     (Periodic Agent Matrix — 14 HR Agents across 6 Pillars)
  - mind_map.html   (Interactive CHRO -> Pillar -> Process -> Agent Mind Map)
"""

from __future__ import annotations

import json
import pathlib

from portal_scripts import PORTAL_JS
from portal_styles import PORTAL_CSS

ROOT = pathlib.Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "data" / "hr_catalog.json"
OUT_HTML = ROOT / "index.html"

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Gemini Enterprise — Agentic for The People (Office of the CHRO)</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%23ffffff' stroke='%234285f4' stroke-width='4'/%3E%3Ccircle cx='32' cy='22' r='8' fill='%234285f4'/%3E%3Ccircle cx='20' cy='42' r='6' fill='%2334a853'/%3E%3Ccircle cx='44' cy='42' r='6' fill='%23ea4335'/%3E%3Cpath d='M32 30 L20 36 M32 30 L44 36' stroke='%23185abc' stroke-width='2.5'/%3E%3C/svg%3E" />
  <style>
__PORTAL_CSS__
  </style>
</head>
<body>

  <!-- STICKY NAVIGATION BAR -->
  <header class="navbar no-print">
    <div class="navbar-inner">
      <div class="nav-brand" onclick="goToHome(true)">
        <svg width="28" height="28" viewBox="0 0 32 32" aria-hidden="true">
          <defs>
            <linearGradient id="sparkBrand" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#4285f4" />
              <stop offset="50%" stop-color="#ac87eb" />
              <stop offset="100%" stop-color="#ea4335" />
            </linearGradient>
          </defs>
          <path d="M16 2 C17.6 10.5 21.5 14.4 30 16 C21.5 17.6 17.6 21.5 16 30 C14.4 21.5 10.5 17.6 2 16 C10.5 14.4 14.4 10.5 16 2 Z" fill="url(#sparkBrand)" />
        </svg>
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:nowrap;">
          <span style="font-family:var(--font-display); font-weight:800; font-size:15.5px; color:var(--text-primary); white-space:nowrap;">Gemini Enterprise</span>
          <span class="nav-csco-badge">CHRO Office</span>
        </div>
      </div>

      <nav class="nav-links" aria-label="Primary sections">
        <button type="button" class="nav-pill-btn" data-nav="pageHome" onclick="goToOrgChart()">6 Pillars</button>
        <button type="button" class="nav-pill-btn" data-nav="pageValueChain" onclick="scrollToProcessJourneys()">4 E2E Flows</button>
        <button type="button" class="nav-pill-btn" data-nav="pageSlides" onclick="openSlidesPage(null, true)">Slides (v3 &middot; v2 &middot; v1)</button>
        <button type="button" class="nav-pill-btn" data-nav="pageMatrix" onclick="openMatrixPage(true)">Matrix (14)</button>
        <button type="button" class="nav-pill-btn" data-nav="pageArchitecture" onclick="openArchitecturePage(true)">Stack &amp; Proof</button>
        <button type="button" class="nav-pill-btn" data-nav="pageMindMap" onclick="openMindMapPage(true)">Mind Map</button>
      </nav>

      <div class="nav-actions">
        <button type="button" class="theme-toggle-btn" onclick="toggleQuickJumpMenu(event)">Jump &#9662;</button>
        <button type="button" id="themeToggleBtn" class="theme-toggle-btn" onclick="togglePortalTheme()"><span>🌙</span><span>Dark Theme</span></button>
        <a href="CHRO_Agentic_Transformation_Keynote_v3.pptx?v=1" download="CHRO_Agentic_Transformation_Keynote_v3.pptx" class="pptx-download-btn">📊 v3 .pptx</a>
        <div id="navQuickMenu" class="nav-quick-menu"></div>
      </div>
    </div>
  </header>

  <!-- 1. MAIN PORTAL VIEW -->
  <main id="pageHome" class="page-view active">
    <section class="hero-section">
      <div class="hero-aurora-backdrop"></div>
      <canvas id="heroHrCanvas"></canvas>
      <div class="hero-content">
        <div class="hero-logo-lockup">
          <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#34a853;"></span>
          <span>PeopleStrong Xponential 2026 · Chief Human Resources Officer (CHRO) Executive Blueprint</span>
        </div>

        <h1 class="hero-title">
          Agentic Transformation for <span class="gradient-word">The People &amp; HR</span>
        </h1>

        <p class="hero-subtitle">
          Turn the <strong>~75% HR Coordination Tax</strong> into strategic talent leadership. Explore <strong>6 Human Resources Pillars</strong> and <strong>14 Process-Led Agents</strong> — blending <strong>No-Code Gemini Enterprise</strong> speedsters with <strong>High-Code Google Agent Development Kit (ADK)</strong> orchestrators ready for Keynote conversion.
        </p>

        <div class="hero-cta-row">
          <button type="button" class="hero-cta-btn hero-cta-primary" onclick="goToOrgChart()">
            <span>Explore Office of the CHRO (6 Pillars)</span>
            <span>&darr;</span>
          </button>
          <button type="button" class="hero-cta-btn hero-cta-secondary" onclick="openSlidesPage(0, true, 'v3')">
            <span>Launch Keynote v3 &middot; v2 &middot; v1</span>
            <span>&rarr;</span>
          </button>
          <a href="https://docs.google.com/presentation/d/1PkW9mPtL3Tta4s5xVUgxiXTlWO2FdInVRp7Hnyng6qU/edit" target="_blank" rel="noopener" class="hero-cta-btn hero-cta-secondary">
            <span>Open in Google Slides &nearr;</span>
          </a>
          <a href="CHRO_Agentic_Transformation_Keynote_v3.pptx?v=1" download="CHRO_Agentic_Transformation_Keynote_v3.pptx" class="hero-cta-btn hero-cta-secondary">
            <span>Download v3 .pptx</span>
          </a>
        </div>

        <div class="four-color-bar">
          <span style="background:var(--g-blue);"></span>
          <span style="background:var(--g-red);"></span>
          <span style="background:var(--g-yellow);"></span>
          <span style="background:var(--g-green);"></span>
        </div>

        <div class="hero-kpi-strip">
          <div class="hero-kpi-card">
            <div class="hero-kpi-val" style="color:var(--g-cobalt);">~75% &rarr; Strategy</div>
            <div class="hero-kpi-lbl">Reclaim Administrative Coordination Tax</div>
          </div>
          <div class="hero-kpi-card">
            <div class="hero-kpi-val" style="color:var(--g-blue);">4 Days &rarr; &lt;1 Hr</div>
            <div class="hero-kpi-lbl">Zero-Touch Interview Scheduling</div>
          </div>
          <div class="hero-kpi-card">
            <div class="hero-kpi-val" style="color:#1e8e3e;">60%–75% Deflect</div>
            <div class="hero-kpi-lbl">Tier-1 HR Concierge Resolution</div>
          </div>
          <div class="hero-kpi-card">
            <div class="hero-kpi-val" style="color:var(--g-purple);">14 Agents &middot; v2 &amp; v1</div>
            <div class="hero-kpi-lbl">16-Slide Keynote + 20-Slide Arch Deck</div>
          </div>
        </div>
      </div>
    </section>

    <section id="orgChartSection" class="org-section">
      <!-- Core Thesis: HR Paradox 75/25 Split -->
      <div id="hrParadoxBand"></div>

      <div class="section-header">
        <div style="display:inline-flex; align-items:center; gap:6px; padding:4px 12px; border-radius:999px; background:var(--bg-ice-blue); border:1px solid var(--border-strong); color:var(--g-cobalt); font-size:11.5px; font-weight:800; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:10px;">
          SLIDE 17 ARCHITECTURE · APQC PCF 7.0 &amp; GEMINI ENTERPRISE
        </div>
        <h2 class="section-title">Office of the CHRO — 6 HR Function Pillars</h2>
        <p class="section-subtitle">Process- and function-led navigation: click any HR Pillar below to inspect its 5-stage process chain, bottleneck vs. agentic value, and assigned No-Code &amp; High-Code AI agents (with served personas mapped inside each agent).</p>
      </div>

      <!-- Master 6-Pillar Tabs -->
      <div id="verticalTabsNavBar" class="vertical-tabs-nav-bar"></div>

      <!-- CHRO Root Box + Animated SVG Connectors + 3x2 Pillar Grid -->
      <div class="cfo-root-wrapper">
        <div class="cfo-box">
          <div class="cfo-sc-emblem" aria-hidden="true">
            <svg viewBox="0 0 84 64" width="84" height="64">
              <circle cx="42" cy="18" r="9" fill="#4285f4" />
              <circle cx="18" cy="48" r="6.5" fill="#ea4335" />
              <circle cx="42" cy="50" r="6.5" fill="#34a853" />
              <circle cx="66" cy="48" r="6.5" fill="#7e57c2" />
              <path d="M42 27 L18 41 M42 27 L42 43 M42 27 L66 41" stroke="#185abc" stroke-width="2" stroke-dasharray="4 2" />
            </svg>
          </div>
          <div>
            <div class="cfo-box-title">Office of the Chief Human Resources Officer (CHRO)</div>
            <div class="cfo-box-sub">6 HR Pillars (Slide 17 Framework) &middot; 4 End-to-End Processes &middot; 14 Process-Led Agents (6 No/Low-Code + 8 High-Code ADK)</div>
          </div>
        </div>

        <svg class="org-connectors" viewBox="0 0 1000 54" preserveAspectRatio="none" aria-hidden="true">
          <defs>
            <linearGradient id="orgTreeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#aecbfa" />
              <stop offset="50%" stop-color="#4285f4" />
              <stop offset="100%" stop-color="#185abc" />
            </linearGradient>
          </defs>
          <path d="M500,0 L500,24 M166,24 L834,24 M166,24 L166,54 M500,24 L500,54 M834,24 L834,54" stroke="#d2e3fc" stroke-width="2" fill="none" />
          <path d="M500,0 L500,24 M166,24 L834,24 M166,24 L166,54 M500,24 L500,54 M834,24 L834,54" stroke="url(#orgTreeGrad)" stroke-width="2.4" stroke-dasharray="8 8" fill="none" style="animation: dashFlow 2.2s linear infinite;" />
        </svg>

        <div id="deptRowContainer" class="dept-row"></div>
      </div>

      <!-- Progressive Showcase Drawer -->
      <div id="deptShowcaseContainer"></div>

      <!-- 4 End-to-End Hire-to-Retire Process Flows -->
      <div id="processJourneysSection" class="vc-home-block">
        <div class="section-header">
          <div style="display:inline-flex; align-items:center; gap:6px; padding:4px 12px; border-radius:999px; background:var(--g-green-bg); color:#137333; font-size:11.5px; font-weight:800; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:10px;">
            🔗 4 END-TO-END HIRE-TO-RETIRE VALUE STREAMS
          </div>
          <h2 class="section-title">End-to-End HR Process Flows</h2>
          <p class="section-subtitle">See how No-Code and High-Code agents collaborate across departments from Requisition-to-Hire through Onboarding, Internal Mobility, and Employee Service.</p>
        </div>
        <div id="valueChainEntryContainer" class="vc-entry-grid"></div>
      </div>
    </section>
  </main>

  <!-- 2. AGENT DEEP-DIVE STUDIO VIEW -->
  <section id="pageAgent" class="page-view">
    <div id="agentPageContent" class="subpage-container"></div>
  </section>

  <!-- 3. END-TO-END PROCESS VALUE CHAIN VIEW -->
  <section id="pageValueChain" class="page-view">
    <div id="valueChainPageContent" class="subpage-container"></div>
  </section>

  <!-- 4. KEYNOTE 16:9 SLIDE PRESENTATION & PPTX VIEW -->
  <section id="pageSlides" class="page-view">
    <div id="slidesPageContent" class="subpage-container"></div>
  </section>

  <!-- 5. PERIODIC MATRIX OF 14 HR AGENTS -->
  <section id="pageMatrix" class="page-view">
    <div id="matrixPageContent" class="subpage-container"></div>
  </section>

  <!-- 6. PLATFORM ARCHITECTURE, ENTERPRISE PROOF & GOVERNANCE VIEW -->
  <section id="pageArchitecture" class="page-view">
    <div id="architecturePageContent" class="subpage-container"></div>
  </section>

  <!-- 7. CHRO MIND MAP & CLICK-PATH EXPLORER -->
  <section id="pageMindMap" class="page-view">
    <div id="mindMapPageContent" class="subpage-container"></div>
  </section>

  <script>
__PORTAL_JS__
  </script>
</body>
</html>
"""


def build_all() -> None:
    cat_raw = CATALOG_PATH.read_text(encoding="utf-8")
    # Ensure JSON parses cleanly and never accidentally closes a <script> tag inside HTML
    cat_obj = json.loads(cat_raw)
    safe_json = json.dumps(cat_obj, indent=2, ensure_ascii=False).replace("</", "<\\/")

    js_injected = PORTAL_JS.replace("__EMBEDDED_CATALOG_JSON__", safe_json)
    html = HTML_TEMPLATE.replace("__PORTAL_CSS__", PORTAL_CSS).replace("__PORTAL_JS__", js_injected)

    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_HTML} ({len(html) // 1024} KB)")

    subpages = {
        "slides.html": "#slides",
        "matrix.html": "#matrix",
        "mind_map.html": "#mindmap",
    }
    for fname, hash_target in subpages.items():
        sub_html = html.replace(
            "handleUrlHash();",
            f"if (!window.location.hash) {{ window.location.hash = '{hash_target}'; }} handleUrlHash();",
        )
        p = ROOT / fname
        p.write_text(sub_html, encoding="utf-8")
        print(f"Wrote {p} ({len(sub_html) // 1024} KB)")


if __name__ == "__main__":
    build_all()
