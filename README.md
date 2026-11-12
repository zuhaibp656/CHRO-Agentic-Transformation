# Gemini Enterprise — Agentic for The People (Office of the CHRO)

Interactive executive portal, dual-version keynote presenter (`v2` Stage Business Edition + `v1` Technical Architecture Deck), and editable PowerPoint (`.pptx`) generator for HR Transformation at enterprise scale.

**Live Website (GitHub Pages):** https://zuhaibp656.github.io/CHRO-Agentic-Transformation/

## Interactive Portals & Keynotes

| Deliverable | Live Path | Description |
| :--- | :--- | :--- |
| **Main Executive Portal** | [`index.html`](index.html) | Light-default Office of the CHRO hub: 6 HR Pillars, 14 Process-Led AI Agents with step-by-step architecture diagrams, and 4 End-to-End Hire-to-Retire Value Streams. |
| **Stage Keynote (`v2`, 16 Slides)** | [`slides.html#slides/v2`](slides.html#slides/v2) | Non-technical CHRO keynote focused on business value, the Zero-UI workplace, all 6 HR Pillars & 25 Business Functions, 8 Employee Touchpoints, Tier-3 employee journey, and a concise 2-slide 14-Agent Mind Map. |
| **Architecture Deck (`v1`, 20 Slides)** | [`slides.html#slides/v1`](slides.html#slides/v1) | Full 20-slide technical architecture edition with Pillar deep-dives, 4 flagship Agent Spotlights, and ADK/FastMCP stack specs. |
| **Editable `v2` PowerPoint** | [`CHRO_Agentic_Transformation_Keynote_v2.pptx`](CHRO_Agentic_Transformation_Keynote_v2.pptx) | Native 16-slide editable `16:9` `.pptx` with embedded custom illustrations, Google Cloud icons, charts, and speaker notes. |
| **Editable `v1` PowerPoint** | [`CHRO_Agentic_Transformation_Keynote.pptx`](CHRO_Agentic_Transformation_Keynote.pptx) | Native 20-slide editable `16:9` `.pptx` full architecture deck. |
| **Periodic Agent Matrix** | [`matrix.html`](matrix.html) | Interactive 14-agent directory filterable across No-Code Studio, Low-Code Hybrid, and High-Code Google ADK. |
| **CHRO Mind Map Explorer** | [`mind_map.html`](mind_map.html) | Click-path visualizer linking CHRO Strategy -> 6 HR Pillars -> Processes -> 14 Agents. |

## Rebuild Locally

```bash
# Regenerate index.html, slides.html, matrix.html, and mind_map.html from data/hr_catalog.json
python3 build_site.py

# Regenerate editable PowerPoint decks (v1 and v2)
uv run --with python-pptx --with pillow python3 export_pptx.py --version both
```
