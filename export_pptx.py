#!/usr/bin/env python3
"""Generate a rich, visual, editable 20-slide 16:9 Keynote PowerPoint deck from data/hr_catalog.json.

Embeds:
- 300-DPI Matplotlib data charts (HR Paradox Donut & Breakdown Bars, Enterprise Proof Bars, Value S-Curve)
- Official Google Cloud Category PNG Icons (Agents, AI/ML, Security & Identity, Databases, Collaboration, etc.)
- Custom antialiased vector medallion icons & editorial illustrations on pure white Simple Light canvas
- Flow chevrons, directional connector arrows, concise scannable headlines (<= 40 words/slide),
  and full narrative + example prompts preserved in Speaker Notes.
"""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Iterable

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = pathlib.Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "data" / "hr_catalog.json"
OUT_PPTX = ROOT / "CHRO_Agentic_Transformation_Keynote.pptx"
OUT_PPTX_V2 = ROOT / "CHRO_Agentic_Transformation_Keynote_v2.pptx"

ASSETS = ROOT / "assets"
BRAND = ASSETS / "branding"
CHARTS = ASSETS / "charts"
ICONS = ASSETS / "icons"
GCP = ASSETS / "gcp_icons"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

FONT_DISPLAY = "Google Sans"
FONT_BODY = "Google Sans Text"


def hex_rgb(hex_str: str) -> RGBColor:
    h = hex_str.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


C_WHITE = hex_rgb("#FFFFFF")
C_SURFACE = hex_rgb("#F8F9FA")
C_SURFACE_ALT = hex_rgb("#F1F3F4")
C_BORDER = hex_rgb("#E8EAED")
C_BORDER_BLUE = hex_rgb("#D2E3FC")
C_ICE_BLUE = hex_rgb("#E8F0FE")
C_INK = hex_rgb("#202124")
C_INK_2 = hex_rgb("#3C4043")
C_MUTED = hex_rgb("#5F6368")
C_BLUE = hex_rgb("#4285F4")
C_COBALT = hex_rgb("#185ABC")
C_RED = hex_rgb("#EA4335")
C_RED_BG = hex_rgb("#FCE8E6")
C_YELLOW = hex_rgb("#FBBC04")
C_AMBER = hex_rgb("#E37400")
C_AMBER_BG = hex_rgb("#FFF2CC")
C_GREEN = hex_rgb("#34A853")
C_GREEN_BG = hex_rgb("#CEEAD6")
C_TEAL = hex_rgb("#0097A7")
C_TEAL_BG = hex_rgb("#E0F7FA")
C_PURPLE = hex_rgb("#7E57C2")
C_PURPLE_BG = hex_rgb("#E6E7FB")

G_FOUR_COLORS = [C_BLUE, C_RED, C_YELLOW, C_GREEN]

PILLAR_ICON_MAP = {
    "requisition_screening": ICONS / "pillar_workforce.png",
    "candidate_hiring": ICONS / "pillar_attract.png",
    "onboarding": ICONS / "pillar_ops.png",
    "continuous_learning": ICONS / "pillar_develop.png",
    "people_ops": ICONS / "pillar_engage.png",
    "hr_strategy_rewards": ICONS / "pillar_perform.png",
}

PILLAR_GCP_MAP = {
    "requisition_screening": GCP / "Agents-512-color.png",
    "candidate_hiring": GCP / "Collaboration-512-color.png",
    "onboarding": GCP / "IntegrationServices-512-color.png",
    "continuous_learning": GCP / "AIMachineLearning-512-color.png",
    "people_ops": GCP / "Operations-512-color.png",
    "hr_strategy_rewards": GCP / "BusinessIntelligence-512-color.png",
}


def short_phrase(text: str, max_words: int = 8, keep_colon: bool = False, keep_dash: bool = False) -> str:
    clean = text.strip() if keep_dash else text.strip().split("—")[0].strip()
    if not keep_colon:
        clean = clean.split(":")[0].strip()
    else:
        clean = clean.replace(":", " —").strip()
    words = clean.split()
    if len(words) <= max_words:
        return clean.rstrip(".,;")
    return " ".join(words[:max_words]).rstrip(".,;") + "…"


def add_bg(slide, color: RGBColor = C_WHITE) -> None:
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()


def add_og_faded_bg(slide) -> None:
    bg_path = BRAND / "og_slide_bg_fade.png"
    if bg_path.exists():
        slide.shapes.add_picture(str(bg_path), Inches(0), Inches(0), width=SLIDE_W, height=SLIDE_H)
    else:
        add_bg(slide, C_WHITE)


def add_brand_footer(slide, slide_num: str, total_slides: int) -> None:
    gc_path = BRAND / "google_cloud_logo.png"
    gem_path = BRAND / "gemini_logo.png"
    cursor_x = 0.65
    if gc_path.exists():
        with Image.open(gc_path) as im:
            gw, gh = im.size
        logo_h = 0.21
        logo_w = logo_h * (gw / max(1, gh))
        slide.shapes.add_picture(str(gc_path), Inches(cursor_x), Inches(7.015), width=Inches(logo_w), height=Inches(logo_h))
        cursor_x += logo_w + 0.14
        add_rect(slide, cursor_x, 7.03, 0.014, 0.18, fill=hex_rgb("#DADCE0"), border=None, rounded=False)
        cursor_x += 0.14
    if gem_path.exists():
        with Image.open(gem_path) as im:
            mw, mh = im.size
        gem_h = 0.22
        gem_w = gem_h * (mw / max(1, mh))
        slide.shapes.add_picture(str(gem_path), Inches(cursor_x), Inches(7.005), width=Inches(gem_w), height=Inches(gem_h))
    add_textbox(
        slide,
        11.3,
        7.01,
        1.4,
        0.24,
        f"{slide_num} / {total_slides:02d}",
        font_size=10,
        bold=True,
        color=C_MUTED,
        align=PP_ALIGN.RIGHT,
        valign=MSO_ANCHOR.MIDDLE,
    )


def add_four_color_strip(slide, top: float = 7.38, height: float = 0.12) -> None:
    seg_w = 13.333 / 4.0
    for idx, col in enumerate(G_FOUR_COLORS):
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(idx * seg_w),
            Inches(top),
            Inches(seg_w + 0.01),
            Inches(height),
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()


def add_rect(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: RGBColor = C_SURFACE,
    border: RGBColor | None = C_BORDER,
    border_pt: float = 1.0,
    rounded: bool = True,
):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded and hasattr(shp, "adjustments") and len(shp.adjustments) > 0:
        shp.adjustments[0] = 0.06
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if border is not None:
        shp.line.color.rgb = border
        shp.line.width = Pt(border_pt)
    else:
        shp.line.fill.background()
    return shp


def add_chevron(slide, x: float, y: float, w: float, h: float, fill: RGBColor):
    shp = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(y), Inches(w), Inches(h))
    if hasattr(shp, "adjustments") and len(shp.adjustments) > 0:
        shp.adjustments[0] = 0.18
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.color.rgb = C_WHITE
    shp.line.width = Pt(1.5)
    return shp


def add_arrow(slide, x: float, y: float, w: float, h: float, fill: RGBColor = C_BLUE):
    shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.fill.background()
    return shp


def add_circle(slide, x: float, y: float, d: float, fill: RGBColor, border: RGBColor | None = None):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if border:
        shp.line.color.rgb = border
        shp.line.width = Pt(1.5)
    else:
        shp.line.fill.background()
    return shp


def add_picture_fit(slide, img_path: pathlib.Path, x: float, y: float, max_w: float, max_h: float):
    if not img_path.exists():
        return None
    with Image.open(img_path) as im:
        pw, ph = im.size
    ratio = pw / max(1, ph)
    w = max_w
    h = w / ratio
    if h > max_h:
        h = max_h
        w = h * ratio
    px = x + (max_w - w) / 2.0
    py = y + (max_h - h) / 2.0
    return slide.shapes.add_picture(str(img_path), Inches(px), Inches(py), width=Inches(w), height=Inches(h))


def add_textbox(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    font_size: float = 14,
    bold: bool = False,
    color: RGBColor = C_INK,
    font_name: str = FONT_BODY,
    align: PP_ALIGN = PP_ALIGN.LEFT,
    valign: MSO_ANCHOR = MSO_ANCHOR.TOP,
):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return tb


def add_bullets(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    items: Iterable[str],
    font_size: float = 13,
    color: RGBColor = C_INK_2,
    bullet_prefix: str = "•  ",
    space_after_pt: float = 8,
) -> None:
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    for idx, line in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(space_after_pt)
        run = p.add_run()
        run.text = f"{bullet_prefix}{line}"
        run.font.name = FONT_BODY
        run.font.size = Pt(font_size)
        run.font.color.rgb = color


def add_slide_chrome(
    slide,
    eyebrow: str,
    title: str,
    subtitle: str,
    slide_num: str,
    accent: RGBColor = C_BLUE,
    total_slides: int = 22,
    icon_path: pathlib.Path | None = None,
) -> None:
    add_og_faded_bg(slide)
    add_rect(slide, 0.0, 0.0, 13.333, 0.07, fill=accent, border=None, rounded=False)
    add_rect(slide, 0.65, 0.30, 5.2, 0.30, fill=C_ICE_BLUE, border=C_BORDER_BLUE, border_pt=0.75)
    add_textbox(
        slide, 0.75, 0.31, 5.0, 0.28, eyebrow, font_size=9.5, bold=True, color=accent, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE
    )
    if icon_path and icon_path.exists():
        add_picture_fit(slide, icon_path, 12.10, 0.30, 0.58, 0.58)
    title_w = 11.2 if (icon_path and icon_path.exists()) else 12.0
    title_fs = 18.0 if len(title) > 74 else (20.5 if len(title) > 64 else 24)
    sub_y = 1.24 if len(title) > 64 else 1.20
    add_textbox(slide, 0.65, 0.64, title_w, 0.54, title, font_size=title_fs, bold=True, color=C_INK, font_name=FONT_DISPLAY)
    if subtitle:
        add_textbox(slide, 0.65, sub_y, 11.8, 0.36, subtitle, font_size=12.5, color=C_MUTED)
    add_brand_footer(slide, slide_num, total_slides)
    add_four_color_strip(slide)


def set_notes(slide, notes_text: str) -> None:
    if not notes_text:
        return
    ns = slide.notes_slide
    ns.notes_text_frame.text = notes_text


def build_single_deck(cat: dict, slides_cfg: list[dict], out_path: pathlib.Path, footer_label: str = "") -> None:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank_layout = prs.slide_layouts[6]

    pillars_map = cat["pillars"]
    pillars = list(pillars_map.values())
    agents = cat["agents"]
    meta = cat["metadata"]
    total = len(slides_cfg)

    for sc in slides_cfg:
        slide = prs.slides.add_slide(blank_layout)
        layout = sc["layout"]
        base_notes = sc.get("notes", "")

        if layout == "hero":
            add_og_faded_bg(slide)
            add_rect(slide, 0.0, 0.0, 13.333, 0.12, fill=C_BLUE, border=None, rounded=False)
            add_rect(slide, 0.72, 0.88, 5.2, 0.36, fill=C_ICE_BLUE, border=C_BORDER_BLUE)
            add_textbox(slide, 0.84, 0.91, 4.96, 0.3, sc["eyebrow"], font_size=10.5, bold=True, color=C_COBALT, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
            add_textbox(slide, 0.72, 1.46, 6.85, 1.3, sc["title"], font_size=42, bold=True, color=C_INK, font_name=FONT_DISPLAY)
            add_textbox(slide, 0.72, 2.74, 6.65, 0.9, sc["subtitle"], font_size=18, color=C_MUTED)

            hl_colors = [C_BLUE, C_RED, C_GREEN]
            hl_bgs = [C_ICE_BLUE, C_RED_BG, C_GREEN_BG]
            hl_icons = [ICONS / "badge_sparkle.png", ICONS / "pillar_attract.png", GCP / "Agents-512-color.png"]
            for idx, item in enumerate(sc.get("highlights", [])):
                cy = 3.92 + idx * 0.82
                add_rect(slide, 0.72, cy, 6.55, 0.68, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, 0.72, cy, 0.08, 0.68, fill=hl_colors[idx % 3], border=None, rounded=False)
                add_picture_fit(slide, hl_icons[idx], 0.92, cy + 0.12, 0.44, 0.44)
                add_textbox(slide, 1.48, cy + 0.16, 5.65, 0.36, item, font_size=13.5, bold=True, color=C_INK, valign=MSO_ANCHOR.MIDDLE)

            add_textbox(slide, 0.72, 6.55, 7.0, 0.32, meta["eventMeta"], font_size=11.5, color=C_MUTED)
            # Hero Illustration Visual (Right 42%)
            add_picture_fit(slide, ASSETS / "hero_chro_keynote.jpg", 7.55, 0.82, 5.35, 5.65)
            add_brand_footer(slide, sc["num"], total)
            add_four_color_strip(slide)
            set_notes(slide, base_notes)

        elif layout == "split_metrics":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_RED, total, ICONS / "badge_clock.png")
            # Visual Charts Row: Left Donut + Center Bars
            add_rect(slide, 0.65, 1.76, 3.85, 3.62, fill=C_WHITE, border=C_BORDER)
            add_picture_fit(slide, CHARTS / "hr_paradox_donut.png", 0.75, 1.84, 3.65, 3.45)

            add_rect(slide, 4.65, 1.76, 4.60, 3.62, fill=C_WHITE, border=C_BORDER)
            add_picture_fit(slide, CHARTS / "hr_paradox_bars.png", 4.75, 1.88, 4.40, 3.40)

            # Right Contrast KPI Cards
            add_rect(slide, 9.42, 1.76, 3.26, 1.72, fill=C_RED_BG, border=C_RED, border_pt=1.2)
            add_picture_fit(slide, ICONS / "badge_clock.png", 9.58, 1.90, 0.46, 0.46)
            add_textbox(slide, 10.14, 1.92, 2.4, 0.42, "~75% ADMIN TAX", font_size=16, bold=True, color=C_RED, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
            add_bullets(slide, 9.58, 2.42, 2.95, 1.00, [short_phrase(it, 10, keep_colon=True, keep_dash=True) for it in sc["leftItems"][:2]], font_size=11.8, color=C_INK, space_after_pt=5)

            add_rect(slide, 9.42, 3.66, 3.26, 1.72, fill=C_GREEN_BG, border=C_GREEN, border_pt=1.2)
            add_picture_fit(slide, GCP / "Collaboration-512-color.png", 9.58, 3.80, 0.46, 0.46)
            add_textbox(slide, 10.14, 3.82, 2.4, 0.42, "~25% STRATEGY", font_size=16, bold=True, color=C_GREEN, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
            add_bullets(slide, 9.58, 4.32, 2.95, 1.00, [short_phrase(it, 10, keep_colon=True, keep_dash=True) for it in sc["rightItems"][:2]], font_size=11.8, color=C_INK, space_after_pt=5)

            # Bottom Executive Callout Pill
            add_rect(slide, 0.65, 5.56, 12.03, 1.22, fill=C_ICE_BLUE, border=C_BORDER_BLUE)
            add_picture_fit(slide, ICONS / "badge_sparkle.png", 0.85, 5.88, 0.56, 0.56)
            add_textbox(
                slide,
                1.56,
                5.72,
                10.9,
                0.88,
                "Keynote Thesis: Agentic AI eliminates the ~75% administrative coordination tax — flipping HR from ticket handler to enterprise talent strategist.",
                font_size=14.5,
                bold=True,
                color=C_COBALT,
                valign=MSO_ANCHOR.MIDDLE,
            )
            full_notes = base_notes + "\n\nFull Time-Allocation Details:\n- Admin Tax: " + "; ".join(sc["leftItems"]) + "\n- Strategic Value: " + "; ".join(sc["rightItems"])
            set_notes(slide, full_notes)

        elif layout == "pillars4":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_BLUE, total, ICONS / "badge_sparkle.png")
            # Left Large Transformation Illustration
            add_rect(slide, 0.65, 1.78, 6.85, 4.98, fill=C_WHITE, border=C_BORDER)
            add_textbox(slide, 0.88, 1.94, 3.0, 0.28, "SILOED DOER", font_size=10.5, bold=True, color=C_RED)
            add_textbox(slide, 4.5, 1.94, 2.8, 0.28, "STRATEGIC ORCHESTRATOR", font_size=10.5, bold=True, color=C_GREEN, align=PP_ALIGN.RIGHT)
            add_picture_fit(slide, ASSETS / "orchestrator_shift.jpg", 0.80, 2.30, 6.55, 3.68)
            add_rect(slide, 0.85, 6.10, 6.45, 0.50, fill=C_SURFACE, border=C_BORDER)
            add_textbox(slide, 1.0, 6.14, 6.15, 0.42, "Gemini Enterprise acts as the bridge — never replacing human empathy.", font_size=12, bold=True, color=C_COBALT, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

            # Right 2x2 Breathable Lever Grid (No truncation)
            lever_icons = [
                GCP / "Agents-512-color.png",
                GCP / "Operations-512-color.png",
                GCP / "Collaboration-512-color.png",
                GCP / "AIMachineLearning-512-color.png",
            ]
            pillar_cards = sc.get("cards") or meta.get("fourValueLevers", [])
            for idx, c in enumerate(pillar_cards):
                col_idx = idx % 2
                row_idx = idx // 2
                col_rgb = hex_rgb(c["color"])
                cx = 7.72 + col_idx * 2.54
                cy = 1.78 + row_idx * 2.58
                add_rect(slide, cx, cy, 2.40, 2.40, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, cx, cy, 2.40, 0.09, fill=col_rgb, border=None, rounded=False)
                add_picture_fit(slide, lever_icons[idx % 4], cx + 0.18, cy + 0.24, 0.48, 0.48)
                add_textbox(slide, cx + 0.74, cy + 0.24, 1.52, 0.48, c["title"], font_size=15, bold=True, color=C_INK, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
                add_rect(slide, cx + 0.18, cy + 0.88, 2.04, 0.42, fill=C_WHITE, border=col_rgb, border_pt=1.0)
                add_textbox(slide, cx + 0.22, cy + 0.91, 1.96, 0.36, c["metric"], font_size=11.5, bold=True, color=col_rgb, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
                add_textbox(slide, cx + 0.18, cy + 1.44, 2.04, 0.80, c["desc"], font_size=12, color=C_INK_2)
            set_notes(slide, base_notes + "\n\nValue Levers: " + " | ".join(f"{c['title']}: {c['desc']}" for c in pillar_cards))

        elif layout == "section_break":
            acc = hex_rgb(sc.get("accent", "#4285F4"))
            add_og_faded_bg(slide)
            add_rect(slide, 0.0, 0.0, 13.333, 0.14, fill=acc, border=None, rounded=False)
            add_rect(slide, 0.85, 1.45, 4.9, 0.40, fill=C_ICE_BLUE, border=C_BORDER_BLUE)
            add_textbox(slide, 0.98, 1.48, 4.64, 0.34, sc["eyebrow"], font_size=11, bold=True, color=acc, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
            add_picture_fit(slide, ICONS / "badge_sparkle.png", 11.15, 1.35, 1.15, 1.15)
            add_textbox(slide, 0.85, 2.15, 9.8, 1.25, sc["title"], font_size=38, bold=True, color=C_INK, font_name=FONT_DISPLAY)
            add_textbox(slide, 0.85, 3.35, 9.6, 0.85, sc.get("subtitle", ""), font_size=17, color=C_MUTED)

            chips = sc.get("chips", [])
            if chips:
                n = len(chips)
                gap = 0.18
                total_w = 11.63
                cw = (total_w - gap * (n - 1)) / n
                for idx, ch in enumerate(chips):
                    cx = 0.85 + idx * (cw + gap)
                    c_col = hex_rgb(ch["color"])
                    add_rect(slide, cx, 4.75, cw, 1.18, fill=C_SURFACE, border=c_col, border_pt=1.2)
                    add_rect(slide, cx, 4.75, cw, 0.08, fill=c_col, border=None, rounded=False)
                    add_textbox(slide, cx + 0.12, 4.94, cw - 0.24, 0.34, ch["num"], font_size=13, bold=True, color=c_col, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER)
                    add_textbox(slide, cx + 0.10, 5.30, cw - 0.20, 0.48, ch["label"], font_size=14, bold=True, color=C_INK, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

            add_brand_footer(slide, sc["num"], total)
            add_four_color_strip(slide)
            set_notes(slide, base_notes)

        elif layout == "pillar_map":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_COBALT, total, GCP / "Agents-512-color.png")
            # CHRO Root Hub + Visual Tree Connectors
            add_rect(slide, 3.05, 1.76, 7.23, 0.62, fill=C_ICE_BLUE, border=C_BLUE, border_pt=1.75)
            add_picture_fit(slide, ICONS / "badge_sparkle.png", 3.22, 1.86, 0.42, 0.42)
            add_picture_fit(slide, GCP / "Agents-512-color.png", 9.68, 1.86, 0.42, 0.42)
            add_textbox(
                slide,
                3.72,
                1.80,
                5.90,
                0.54,
                "OFFICE OF THE CHRO · 6 PILLARS · 14 PROCESS AGENTS",
                font_size=13.5,
                bold=True,
                color=C_COBALT,
                font_name=FONT_DISPLAY,
                align=PP_ALIGN.CENTER,
                valign=MSO_ANCHOR.MIDDLE,
            )
            add_rect(slide, 6.65, 2.38, 0.03, 0.22, fill=C_BORDER_BLUE, border=None, rounded=False)
            add_rect(slide, 2.59, 2.58, 8.16, 0.03, fill=C_BORDER_BLUE, border=None, rounded=False)

            for idx, p in enumerate(pillars):
                row = idx // 3
                col = idx % 3
                px = 0.65 + col * 4.08
                py = 2.74 + row * 2.08
                p_rgb = hex_rgb(p["color"])
                p_icon = PILLAR_ICON_MAP.get(p["id"], ICONS / "badge_sparkle.png")
                add_rect(slide, px, py, 3.88, 1.88, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, px, py, 3.88, 0.09, fill=p_rgb, border=None, rounded=False)
                add_picture_fit(slide, p_icon, px + 0.18, py + 0.22, 0.56, 0.56)
                add_textbox(slide, px + 0.84, py + 0.20, 2.86, 0.24, p["apqcBadge"], font_size=9.5, bold=True, color=p_rgb, font_name=FONT_DISPLAY)
                add_textbox(slide, px + 0.84, py + 0.44, 2.86, 0.44, p.get("shortName", p["name"]), font_size=14, bold=True, color=C_INK, font_name=FONT_DISPLAY)
                add_textbox(slide, px + 0.18, py + 0.96, 3.52, 0.38, p.get("slideMetric", p["impactMetric"]), font_size=15, bold=True, color=p_rgb, font_name=FONT_DISPLAY)
                add_rect(slide, px + 0.18, py + 1.40, 3.52, 0.34, fill=C_WHITE, border=C_BORDER_BLUE)
                add_textbox(slide, px + 0.24, py + 1.43, 3.40, 0.28, p.get("slideMixPill", f"{len(p['agentIds'])} Process Agents"), font_size=10, bold=True, color=C_INK_2, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
            set_notes(slide, base_notes)

        elif layout == "pillar_deepdive":
            p = cat["pillars"][sc["pillarId"]]
            p_rgb = hex_rgb(p["color"])
            p_icon = PILLAR_ICON_MAP.get(p["id"], ICONS / "badge_sparkle.png")
            g_icon = PILLAR_GCP_MAP.get(p["id"], GCP / "Agents-512-color.png")
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], p["coreQuestion"], sc["num"], p_rgb, total, p_icon)

            # 1. Breathable 5-Stage Process Chevrons (1 clean phrase each)
            chevron_shades = [p_rgb, C_COBALT, C_BLUE, C_TEAL, C_GREEN]
            short_stages = p.get("slideShortStages", [s["name"] for s in p["processStages"]])
            for idx, st_label in enumerate(short_stages):
                sx = 0.65 + idx * 2.40
                add_chevron(slide, sx, 1.76, 2.46, 0.60, chevron_shades[idx % len(chevron_shades)])
                add_textbox(slide, sx + 0.16, 1.82, 2.08, 0.48, st_label, font_size=11.5, bold=True, color=C_WHITE, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

            # 2. Left Breathable Outcome Hero Card (no redundant 3-bullet box)
            add_rect(slide, 0.65, 2.64, 4.45, 4.10, fill=C_ICE_BLUE, border=p_rgb, border_pt=1.5)
            add_picture_fit(slide, p_icon, 0.90, 2.92, 0.86, 0.86)
            add_picture_fit(slide, g_icon, 4.10, 2.98, 0.72, 0.72)
            add_textbox(slide, 0.90, 4.02, 3.95, 0.30, "BENCHMARK OUTCOME", font_size=10, bold=True, color=p_rgb, font_name=FONT_DISPLAY)
            add_textbox(slide, 0.90, 4.32, 3.95, 0.58, p.get("slideMetric", p["impactMetric"]), font_size=26, bold=True, color=C_INK, font_name=FONT_DISPLAY)
            add_textbox(slide, 0.90, 4.94, 3.95, 0.56, p.get("slideMetricSub", ""), font_size=13.5, bold=True, color=C_COBALT)
            add_rect(slide, 0.90, 5.66, 3.95, 0.84, fill=C_WHITE, border=C_BORDER)
            add_textbox(slide, 1.04, 5.74, 3.67, 0.68, f"Solves: {p.get('slideChallenge', '')}", font_size=11.5, color=C_INK_2, valign=MSO_ANCHOR.MIDDLE)

            # 3. Right Spacious Agent Cards Roster
            p_agents = [agents[aid] for aid in p["agentIds"]]
            gap_y = 0.22 if len(p_agents) == 2 else 0.18
            total_agent_h = 4.10
            card_h = (total_agent_h - gap_y * max(0, len(p_agents) - 1)) / len(p_agents)
            for idx, ag in enumerate(p_agents):
                ay = 2.64 + idx * (card_h + gap_y)
                tier_col = C_GREEN if ag["buildTier"] == "No-Code" else (C_BLUE if ag["buildTier"] == "Low-Code" else C_PURPLE)
                tier_icon = ICONS / ("badge_nocode.png" if ag["buildTier"] == "No-Code" else ("badge_adk.png" if ag["buildTier"] == "High-Code" else "badge_sparkle.png"))
                add_rect(slide, 5.34, ay, 7.34, card_h, fill=C_WHITE, border=C_BORDER_BLUE if idx == 0 else C_BORDER, border_pt=1.25)
                add_rect(slide, 5.34, ay, 0.10, card_h, fill=tier_col, border=None, rounded=False)
                add_picture_fit(slide, tier_icon, 5.62, ay + (card_h - 0.58) / 2, 0.58, 0.58)
                add_textbox(
                    slide,
                    6.38,
                    ay + (card_h * 0.20),
                    4.30,
                    0.38,
                    ag["name"],
                    font_size=15 if len(p_agents) <= 2 else 13.5,
                    bold=True,
                    color=C_INK,
                    font_name=FONT_DISPLAY,
                )
                add_rect(slide, 10.76, ay + (card_h * 0.20), 1.68, 0.32, fill=C_SURFACE_ALT, border=tier_col, border_pt=0.9)
                add_textbox(slide, 10.78, ay + (card_h * 0.21), 1.64, 0.30, ag["buildTier"].upper(), font_size=9.5, bold=True, color=tier_col, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
                add_textbox(
                    slide,
                    6.38,
                    ay + (card_h * 0.56),
                    6.06,
                    0.42,
                    ag.get("slideOutcome", ag["outcomeBadge"]),
                    font_size=13 if len(p_agents) <= 2 else 12,
                    color=C_INK_2,
                    valign=MSO_ANCHOR.MIDDLE,
                )

            rich_notes = (
                base_notes
                + "\n\nFull Pillar Toil & Impact Details:\n- "
                + "\n- ".join(p["toilBullets"] + p["impactBullets"])
                + "\n\nAgents:\n- "
                + "\n- ".join(f"{ag['name']} ({ag['buildTier']}): {ag['shortDesc']} | Personas: {', '.join(ag['personasServed'])}" for ag in p_agents)
            )
            set_notes(slide, rich_notes)

        elif layout == "agent_spotlight":
            ag = agents[sc["agentId"]]
            p_rgb = hex_rgb(ag["pillarColor"])
            tier_col = C_GREEN if ag["buildTier"] == "No-Code" else (C_BLUE if ag["buildTier"] == "Low-Code" else C_PURPLE)
            tier_icon = ICONS / ("badge_nocode.png" if ag["buildTier"] == "No-Code" else ("badge_adk.png" if ag["buildTier"] == "High-Code" else "badge_sparkle.png"))
            add_slide_chrome(
                slide,
                sc["eyebrow"],
                sc["title"],
                f"{ag['pillarName']}  ·  {ag.get('slideProcessShort', ag['processName'])}  ·  {ag['buildTier']}",
                sc["num"],
                p_rgb,
                total,
                tier_icon,
            )
            # 1. Crisp Single-Line Before -> After Banner
            add_rect(slide, 0.65, 1.80, 5.55, 0.82, fill=C_RED_BG, border=C_RED, border_pt=1.0)
            add_picture_fit(slide, ICONS / "badge_clock.png", 0.82, 1.99, 0.44, 0.44)
            add_textbox(slide, 1.38, 1.86, 4.68, 0.22, "BEFORE", font_size=9.5, bold=True, color=C_RED)
            add_textbox(slide, 1.38, 2.08, 4.68, 0.44, ag.get("slideBefore", ag["problem"]), font_size=13, bold=True, color=C_INK, valign=MSO_ANCHOR.MIDDLE)

            add_arrow(slide, 6.32, 2.04, 0.68, 0.34, C_BLUE)

            add_rect(slide, 7.12, 1.80, 5.56, 0.82, fill=C_GREEN_BG, border=C_GREEN, border_pt=1.0)
            add_picture_fit(slide, ICONS / "badge_check.png", 7.29, 1.99, 0.44, 0.44)
            add_textbox(slide, 7.85, 1.86, 4.68, 0.22, "AFTER", font_size=9.5, bold=True, color=C_GREEN)
            add_textbox(slide, 7.85, 2.08, 4.68, 0.44, ag.get("slideAfter", ag["outcomeBadge"]), font_size=13, bold=True, color=C_INK, valign=MSO_ANCHOR.MIDDLE)

            # 2. Spacious 3-Node Visual Architecture Flow (Max 2 chips per box)
            add_rect(slide, 0.65, 2.90, 3.60, 2.74, fill=C_ICE_BLUE, border=tier_col, border_pt=1.4)
            add_picture_fit(slide, GCP / "Agents-512-color.png", 2.09, 3.12, 0.72, 0.72)
            add_textbox(slide, 0.82, 3.92, 3.26, 0.26, "1. AGENT ORCHESTRATOR", font_size=10, bold=True, color=tier_col, align=PP_ALIGN.CENTER)
            add_textbox(slide, 0.82, 4.22, 3.26, 0.56, ag.get("slideOrch", ag["name"]), font_size=14.5, bold=True, color=C_INK, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
            add_rect(slide, 0.92, 4.96, 3.06, 0.40, fill=C_WHITE, border=C_BORDER_BLUE)
            add_textbox(slide, 1.0, 5.00, 2.90, 0.32, f"For: {ag['personasServed'][0]}", font_size=11.5, bold=True, color=C_COBALT, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

            add_arrow(slide, 4.34, 4.10, 0.48, 0.34, C_BLUE)

            add_rect(slide, 4.92, 2.90, 3.60, 2.74, fill=C_SURFACE, border=C_BORDER)
            add_picture_fit(slide, GCP / "AIMachineLearning-512-color.png", 6.36, 3.12, 0.72, 0.72)
            add_textbox(slide, 5.08, 3.92, 3.28, 0.26, "2. KEY CAPABILITIES", font_size=10, bold=True, color=C_BLUE, align=PP_ALIGN.CENTER)
            for sidx, sp in enumerate(ag.get("slideSpecs", ag["architectureNodes"]["specialists"][:2])):
                sy_chip = 4.34 + sidx * 0.56
                add_rect(slide, 5.14, sy_chip, 3.16, 0.44, fill=C_WHITE, border=C_BORDER_BLUE)
                add_textbox(slide, 5.24, sy_chip + 0.04, 2.96, 0.36, sp, font_size=12, bold=True, color=C_INK, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

            add_arrow(slide, 8.61, 4.10, 0.48, 0.34, C_TEAL)

            sys_icon = GCP / ("IntegrationServices-512-color.png" if ag["buildTier"] == "Low-Code" else "Databases-512-color.png")
            add_rect(slide, 9.19, 2.90, 3.49, 2.74, fill=C_SURFACE, border=C_BORDER)
            add_picture_fit(slide, sys_icon, 10.57, 3.12, 0.72, 0.72)
            add_textbox(slide, 9.34, 3.92, 3.19, 0.26, "3. CONNECTED SYSTEMS", font_size=10, bold=True, color=C_TEAL, align=PP_ALIGN.CENTER)
            for cidx, cn in enumerate(ag.get("slideSystems", ag["architectureNodes"]["connectors"][:2])):
                cy_chip = 4.34 + cidx * 0.56
                add_rect(slide, 9.40, cy_chip, 3.07, 0.44, fill=C_TEAL_BG, border=C_TEAL, border_pt=0.8)
                add_textbox(slide, 9.50, cy_chip + 0.04, 2.87, 0.36, cn, font_size=12, bold=True, color=C_TEAL, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

            # 3. Single-Line DPDP Guardrail Strip
            add_rect(slide, 0.65, 5.90, 12.03, 0.80, fill=C_AMBER_BG, border=C_AMBER, border_pt=1.0)
            add_picture_fit(slide, GCP / "SecurityIdentity-512-color.png", 0.85, 6.04, 0.52, 0.52)
            add_textbox(slide, 1.52, 6.00, 3.3, 0.60, "INDIA DPDP & HITL LOCK:", font_size=11, bold=True, color=C_AMBER, valign=MSO_ANCHOR.MIDDLE)
            add_textbox(slide, 4.45, 6.00, 8.0, 0.60, ag.get("slideGuardrail", ag["guardrails"]), font_size=13, bold=True, color=C_INK, valign=MSO_ANCHOR.MIDDLE)

            full_agent_notes = (
                f"{base_notes}\n\n"
                f"Full Problem: {ag['problem']}\n"
                f"Outcome: {ag['outcomeBadge']} ({ag['baselineVsTarget']})\n"
                f"MCP Tools: {', '.join(ag['mcpTools'])}\n"
                f"Guardrail: {ag['guardrails']}\n"
                f"Demo Prompt: \"{ag['samplePrompt']}\""
            )
            set_notes(slide, full_agent_notes)

        elif layout == "enterprise_proof":
            proof = meta["enterpriseProofPoint"]
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], proof["subtitle"], sc["num"], C_GREEN, total, ICONS / "badge_check.png")
            kpi_icons = [GCP / "Agents-512-color.png", GCP / "BusinessIntelligence-512-color.png", ICONS / "badge_nocode.png", GCP / "SecurityIdentity-512-color.png"]
            for idx, m in enumerate(proof["metrics"]):
                mx = 0.65 + idx * 3.06
                add_rect(slide, mx, 1.76, 2.86, 1.08, fill=C_ICE_BLUE if idx % 2 == 0 else C_GREEN_BG, border=C_BORDER_BLUE)
                add_picture_fit(slide, kpi_icons[idx], mx + 0.16, 1.98, 0.54, 0.54)
                add_textbox(slide, mx + 0.80, 1.82, 1.92, 0.46, m["value"], font_size=26, bold=True, color=C_COBALT, font_name=FONT_DISPLAY)
                add_textbox(slide, mx + 0.80, 2.30, 1.94, 0.46, m["label"], font_size=11.5, bold=True, color=C_INK_2)

            # Bottom Left Bar Chart
            add_rect(slide, 0.65, 3.02, 6.45, 3.74, fill=C_WHITE, border=C_BORDER)
            add_picture_fit(slide, CHARTS / "enterprise_proof_bars.png", 0.78, 3.12, 6.20, 3.52)

            # Bottom Right 2x2 Micro-Agent Cards (Vertically balanced, no voids)
            for idx, la in enumerate(proof["liveHrAgents"]):
                lx = 7.32 + (idx % 2) * 2.74
                ly = 3.02 + (idx // 2) * 1.94
                add_rect(slide, lx, ly, 2.60, 1.78, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, lx, ly, 2.60, 0.08, fill=G_FOUR_COLORS[idx], border=None, rounded=False)
                add_picture_fit(slide, ICONS / "badge_nocode.png", lx + 0.16, ly + 0.24, 0.36, 0.36)
                add_textbox(slide, lx + 0.60, ly + 0.22, 1.88, 0.40, la["name"], font_size=13.5, bold=True, color=C_INK, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
                add_textbox(slide, lx + 0.16, ly + 0.72, 2.28, 0.90, la.get("slideDesc", la["desc"]), font_size=12, color=C_INK_2, valign=MSO_ANCHOR.MIDDLE)

            set_notes(slide, base_notes + "\n\nLearnings:\n- " + "\n- ".join(proof["architectureLessons"]))

        elif layout == "architecture_layers":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_PURPLE, total, GCP / "Storage-512-color.png")
            layers = [
                ("1. THE TASKFORCE (HR Experiences)", "14 Process Agents + PeopleStrong / Workday / ServiceNow", C_BLUE, C_ICE_BLUE, GCP / "Agents-512-color.png", GCP / "Collaboration-512-color.png"),
                ("2. THE WORKBENCH (Dual Build Tier)", "6 No/Low-Code Studio Agents + 8 Code-First ADK Agents", C_GREEN, C_GREEN_BG, GCP / "Developer_Tools-512-color.png", GCP / "IntegrationServices-512-color.png"),
                ("3. THE CONTEXT (Enterprise Memory)", "Open Knowledge Format (OKF) + Vertex AI RAG + FastMCP", C_TEAL, C_TEAL_BG, GCP / "Storage-512-color.png", GCP / "Databases-512-color.png"),
                ("4. THE BRAINS (Model Tiering)", "Gemini Flash (Sub-Second FAQ) + Gemini Pro (Deep Reasoning)", C_PURPLE, C_PURPLE_BG, GCP / "AIMachineLearning-512-color.png", GCP / "BusinessIntelligence-512-color.png"),
            ]
            for idx, (lt, ld, bcol, bgc, icon_a, icon_b) in enumerate(layers):
                ly = 1.82 + idx * 1.26
                add_rect(slide, 0.65, ly, 9.25, 1.10, fill=bgc, border=bcol, border_pt=1.25)
                add_picture_fit(slide, icon_a, 0.85, ly + 0.24, 0.60, 0.60)
                add_textbox(slide, 1.62, ly + 0.16, 6.75, 0.34, lt, font_size=14.5, bold=True, color=bcol, font_name=FONT_DISPLAY)
                add_textbox(slide, 1.62, ly + 0.54, 6.75, 0.40, ld, font_size=13, color=C_INK)
                add_picture_fit(slide, icon_b, 9.08, ly + 0.24, 0.60, 0.60)

            # Vertical Security & India DPDP Shield Pillar
            add_rect(slide, 10.12, 1.82, 2.56, 4.88, fill=C_AMBER_BG, border=C_AMBER, border_pt=1.5)
            add_picture_fit(slide, GCP / "SecurityIdentity-512-color.png", 10.96, 2.04, 0.86, 0.86)
            add_textbox(slide, 10.28, 3.00, 2.24, 0.54, "TRUST & INDIA\nDPDP SHIELD", font_size=13.5, bold=True, color=C_AMBER, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER)
            shields = ["Model Armor Guard", "Cloud DLP Redaction", "Consent Ledger", "Least Privilege IAM"]
            for sidx, sh in enumerate(shields):
                sy = 3.74 + sidx * 0.66
                add_rect(slide, 10.30, sy, 2.20, 0.50, fill=C_WHITE, border=C_AMBER, border_pt=0.9)
                add_textbox(slide, 10.36, sy + 0.05, 2.08, 0.40, sh, font_size=11.5, bold=True, color=C_INK, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

            set_notes(slide, base_notes)

        elif layout == "adoption_curve":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_BLUE, total, GCP / "BusinessIntelligence-512-color.png")
            add_rect(slide, 0.65, 1.74, 12.03, 3.16, fill=C_WHITE, border=C_BORDER)
            add_picture_fit(slide, CHARTS / "value_scurve.png", 0.82, 1.82, 11.70, 3.00)

            ad_icons = [
                GCP / "Collaboration-512-color.png",
                GCP / "SecurityIdentity-512-color.png",
                GCP / "Operations-512-color.png",
                GCP / "AIMachineLearning-512-color.png",
            ]
            for idx, ap in enumerate(meta["adoptionPillars"]):
                ax = 0.65 + idx * 3.06
                add_rect(slide, ax, 5.06, 2.86, 1.72, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, ax, 5.06, 2.86, 0.08, fill=G_FOUR_COLORS[idx], border=None, rounded=False)
                add_picture_fit(slide, ad_icons[idx], ax + 0.16, 5.22, 0.44, 0.44)
                add_textbox(slide, ax + 0.68, 5.24, 2.02, 0.24, f"PILLAR #{ap['num']}", font_size=9.5, bold=True, color=G_FOUR_COLORS[idx])
                add_textbox(slide, ax + 0.16, 5.72, 2.54, 0.40, ap["title"], font_size=12.5, bold=True, color=C_INK, font_name=FONT_DISPLAY)
                add_textbox(slide, ax + 0.16, 6.14, 2.54, 0.52, ap.get("slideDesc", ap["desc"]), font_size=11, color=C_INK_2)
            set_notes(slide, base_notes + "\n\nValue Curve Stages:\n- " + "\n- ".join(f"{v['stage']}: {v['headline']} ({'; '.join(v['bullets'])})" for v in meta["valueCurve"]))

        elif layout == "macro_shift":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_BLUE, total, GCP / "Agents-512-color.png")
            add_rect(slide, 0.65, 1.78, 6.25, 4.18, fill=C_WHITE, border=C_BORDER_BLUE, border_pt=1.25)
            hero_p = ROOT / sc.get("heroImage", "assets/zero_ui_workplace.jpg")
            add_picture_fit(slide, hero_p, 0.78, 1.88, 5.99, 3.98)

            for idx, c in enumerate(sc.get("cards", [])):
                cy = 1.78 + idx * 1.45
                col_rgb = hex_rgb(c["accent"])
                add_rect(slide, 7.12, cy, 5.56, 1.28, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, 7.12, cy, 0.08, 1.28, fill=col_rgb, border=None, rounded=False)
                add_picture_fit(slide, ROOT / c["icon"], 7.32, cy + 0.36, 0.54, 0.54)
                add_textbox(slide, 7.98, cy + 0.16, 4.54, 0.32, c["title"], font_size=14, bold=True, color=C_INK, font_name=FONT_DISPLAY)
                add_textbox(slide, 7.98, cy + 0.50, 4.54, 0.66, c["desc"], font_size=11.5, color=C_INK_2)

            if sc.get("statBanner"):
                add_rect(slide, 0.65, 6.14, 12.03, 0.70, fill=C_ICE_BLUE, border=C_BORDER_BLUE)
                add_picture_fit(slide, ICONS / "badge_sparkle.png", 0.85, 6.27, 0.44, 0.44)
                add_textbox(slide, 1.42, 6.20, 11.1, 0.58, sc["statBanner"], font_size=13, bold=True, color=C_COBALT, valign=MSO_ANCHOR.MIDDLE)
            set_notes(slide, base_notes)

        elif layout == "human_premium":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_GREEN, total, ICONS / "pillar_engage.png")
            add_rect(slide, 0.65, 1.78, 6.15, 4.18, fill=C_WHITE, border=hex_rgb("#CEEAD6"), border_pt=1.25)
            add_picture_fit(slide, ROOT / sc.get("heroImage", "assets/human_premium.jpg"), 0.78, 1.88, 5.89, 3.98)

            for idx, pitem in enumerate(sc.get("pillars", [])):
                cy = 1.78 + idx * 1.45
                col_rgb = hex_rgb(pitem["color"])
                add_rect(slide, 7.02, cy, 5.66, 1.28, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, 7.02, cy, 5.66, 0.08, fill=col_rgb, border=None, rounded=False)
                add_picture_fit(slide, ROOT / pitem["icon"], 7.22, cy + 0.38, 0.52, 0.52)
                add_textbox(slide, 7.88, cy + 0.20, 4.64, 0.32, pitem["title"], font_size=14, bold=True, color=C_INK, font_name=FONT_DISPLAY)
                add_textbox(slide, 7.88, cy + 0.54, 4.64, 0.62, pitem["desc"], font_size=11.5, color=C_INK_2)

            if sc.get("quote"):
                add_rect(slide, 0.65, 6.14, 12.03, 0.70, fill=C_ICE_BLUE, border=C_BORDER_BLUE)
                add_textbox(slide, 0.85, 6.20, 11.63, 0.58, sc["quote"], font_size=13.5, bold=True, color=C_COBALT, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
            set_notes(slide, base_notes)

        elif layout == "moments_matter":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_BLUE, total, ICONS / "badge_sparkle.png")
            add_rect(slide, 0.65, 1.74, 12.03, 2.26, fill=C_WHITE, border=C_BORDER_BLUE)
            add_picture_fit(slide, ROOT / sc.get("heroImage", "assets/moments_matter.jpg"), 0.80, 1.80, 11.73, 2.14)

            moments = sc.get("moments", [])
            for idx, m in enumerate(moments):
                mx = 0.65 + idx * 2.445
                mcol = hex_rgb(m["color"])
                add_rect(slide, mx, 4.18, 2.25, 2.64, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, mx, 4.18, 2.25, 0.08, fill=mcol, border=None, rounded=False)
                add_textbox(slide, mx + 0.14, 4.34, 0.55, 0.30, m["step"], font_size=11, bold=True, color=mcol, font_name=FONT_DISPLAY)
                add_picture_fit(slide, ROOT / m["icon"], mx + 1.65, 4.30, 0.42, 0.42)
                add_textbox(slide, mx + 0.14, 4.74, 1.97, 0.32, m["title"], font_size=14, bold=True, color=C_INK, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER)
                add_textbox(slide, mx + 0.14, 5.08, 1.97, 0.44, m["metric"], font_size=21, bold=True, color=mcol, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER)
                add_textbox(slide, mx + 0.14, 5.52, 1.97, 0.24, m["metricLbl"].upper(), font_size=8.5, bold=True, color=C_MUTED, align=PP_ALIGN.CENTER)
                add_rect(slide, mx + 0.28, 5.84, 1.69, 0.02, fill=C_BORDER, border=None, rounded=False)
                add_textbox(slide, mx + 0.14, 5.92, 1.97, 0.80, m["desc"], font_size=10.5, color=C_INK_2, align=PP_ALIGN.CENTER)
            set_notes(slide, base_notes)

        elif layout == "mindmap_agents":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_COBALT, total, GCP / "Agents-512-color.png")
            # Left Central Mind Map Hub
            add_rect(slide, 0.65, 1.82, 2.24, 4.98, fill=C_ICE_BLUE, border=C_BLUE, border_pt=1.5)
            add_picture_fit(slide, GCP / "Agents-512-color.png", 1.38, 2.04, 0.78, 0.78)
            add_textbox(slide, 0.78, 2.94, 1.98, 0.26, f"MIND MAP · {sc.get('part', '')}".upper(), font_size=9.5, bold=True, color=C_COBALT, align=PP_ALIGN.CENTER)
            add_textbox(slide, 0.78, 3.24, 1.98, 0.68, sc.get("hubTitle", "Agent Ecosystem"), font_size=15.5, bold=True, color=C_INK, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER)
            add_textbox(slide, 0.78, 3.96, 1.98, 0.34, sc.get("hubSub", ""), font_size=11, bold=True, color=C_BLUE, align=PP_ALIGN.CENTER)

            # Tier Legend Box at bottom of Hub
            is_v2_deck = "v2" in (footer_label or "").lower()
            add_rect(slide, 0.80, 5.42, 1.94, 1.20, fill=C_WHITE, border=C_BORDER_BLUE)
            add_textbox(slide, 0.90, 5.48, 1.74, 0.22, "SOLUTION TYPE" if is_v2_deck else "BUILD TIER KEY", font_size=8.5, bold=True, color=C_MUTED)
            add_circle(slide, 0.92, 5.80, 0.14, C_GREEN)
            add_textbox(slide, 1.12, 5.75, 1.54, 0.26, "HR Team Studio" if is_v2_deck else "No / Low-Code", font_size=9.5, bold=True, color=C_INK)
            add_circle(slide, 0.92, 6.18, 0.14, C_PURPLE)
            add_textbox(slide, 1.12, 6.13, 1.54, 0.26, "Cross-System Sync" if is_v2_deck else "Google ADK + MCP", font_size=9.5, bold=True, color=C_INK)

            # Vertical Trunk line connecting Hub to 3 Pillar branches
            add_rect(slide, 2.89, 4.29, 0.18, 0.03, fill=hex_rgb("#AECBFA"), border=None, rounded=False)
            add_rect(slide, 3.06, 2.57, 0.03, 3.47, fill=hex_rgb("#AECBFA"), border=None, rounded=False)

            branch_ids = sc.get("pillarIds", [])
            for r_idx, pid in enumerate(branch_ids):
                p_obj = pillars_map[pid]
                p_col = hex_rgb(p_obj["color"])
                p_icon = PILLAR_ICON_MAP.get(pid, ICONS / "badge_sparkle.png")
                row_y = 1.82 + r_idx * 1.72
                row_h = 1.54
                mid_y = row_y + row_h / 2.0

                # Branch line from vertical trunk into Pillar Node
                add_rect(slide, 3.06, mid_y - 0.015, 0.18, 0.03, fill=p_col, border=None, rounded=False)

                # Pillar Box (Clean Icon + Short Pillar Title)
                add_rect(slide, 3.24, row_y, 2.38, row_h, fill=C_SURFACE, border=p_col, border_pt=1.25)
                add_rect(slide, 3.24, row_y, 0.08, row_h, fill=p_col, border=None, rounded=False)
                add_picture_fit(slide, p_icon, 3.42, row_y + 0.52, 0.48, 0.48)
                add_textbox(slide, 4.00, row_y + 0.24, 1.52, 0.24, p_obj.get("apqcBadge", f"PILLAR 0{p_obj['vNum']}"), font_size=8.8, bold=True, color=p_col)
                add_textbox(slide, 4.00, row_y + 0.52, 1.52, 0.78, p_obj.get("shortName", p_obj["name"]), font_size=12.5, bold=True, color=C_INK, font_name=FONT_DISPLAY)

                # Connector into Agent Nodes
                add_rect(slide, 5.62, mid_y - 0.015, 0.24, 0.03, fill=p_col, border=None, rounded=False)

                p_agents = [agents[aid] for aid in p_obj["agentIds"]]
                n_ag = len(p_agents)
                avail_w = 6.82
                gap = 0.14
                ag_w = (avail_w - (n_ag - 1) * gap) / max(1, n_ag)

                for a_idx, ag in enumerate(p_agents):
                    ax = 5.86 + a_idx * (ag_w + gap)
                    is_adk = ag["buildTier"] == "High-Code"
                    t_col = C_PURPLE if is_adk else C_GREEN
                    t_bg = C_PURPLE_BG if is_adk else C_GREEN_BG
                    t_label = ("Connected" if is_adk else "HR Studio") if is_v2_deck else ("ADK" if is_adk else ("Low-Code" if ag["buildTier"] == "Low-Code" else "No-Code"))

                    add_rect(slide, ax, row_y, ag_w, row_h, fill=C_WHITE, border=C_BORDER_BLUE, border_pt=1.0)
                    add_rect(slide, ax, row_y, ag_w, 0.07, fill=t_col, border=None, rounded=False)

                    # Simple Agent Name + Tier Pill
                    name_fs = 12.8 if n_ag == 2 else 11.2
                    add_textbox(slide, ax + 0.12, row_y + 0.14, ag_w - 0.92, 0.44, ag.get("simpleName", ag["name"]), font_size=name_fs, bold=True, color=C_INK, font_name=FONT_DISPLAY)
                    add_rect(slide, ax + ag_w - 0.80, row_y + 0.16, 0.68, 0.24, fill=t_bg, border=t_col, border_pt=0.6)
                    add_textbox(slide, ax + ag_w - 0.80, row_y + 0.16, 0.68, 0.24, t_label, font_size=8.2, bold=True, color=t_col, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

                    # Clean Persona List Only (concise pills)
                    personas = ag.get("personasServed", [])[:3]
                    add_bullets(slide, ax + 0.10, row_y + 0.62, ag_w - 0.20, row_h - 0.68, personas, font_size=9.8 if n_ag == 2 else 9.0, color=C_INK_2, bullet_prefix="👤 ", space_after_pt=3.0)

            set_notes(slide, base_notes)

        elif layout == "governance_dpdp":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_COBALT, total, GCP / "SecurityIdentity-512-color.png")
            add_rect(slide, 0.65, 1.78, 5.15, 5.02, fill=C_WHITE, border=C_BORDER_BLUE, border_pt=1.25)
            add_picture_fit(slide, ROOT / sc.get("heroImage", "assets/governance_dpdp.jpg"), 0.80, 1.90, 4.85, 4.78)

            for idx, c in enumerate(sc.get("cards", [])):
                cx = 6.02 + (idx % 2) * 3.42
                cy = 1.78 + (idx // 2) * 2.60
                col_rgb = hex_rgb(c["color"])
                add_rect(slide, cx, cy, 3.24, 2.42, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, cx, cy, 3.24, 0.08, fill=col_rgb, border=None, rounded=False)
                add_picture_fit(slide, ROOT / c["icon"], cx + 0.18, cy + 0.28, 0.50, 0.50)
                add_textbox(slide, cx + 0.78, cy + 0.24, 2.32, 0.58, c["title"], font_size=14.5, bold=True, color=C_INK, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
                add_textbox(slide, cx + 0.18, cy + 0.94, 2.88, 1.28, c["desc"], font_size=12.5, color=C_INK_2, valign=MSO_ANCHOR.MIDDLE)
            set_notes(slide, base_notes)

        elif layout == "workforce_readiness":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_GREEN, total, ICONS / "pillar_develop.png")
            add_rect(slide, 0.65, 1.78, 7.15, 5.02, fill=C_WHITE, border=C_BORDER_BLUE)
            add_picture_fit(slide, ROOT / sc.get("chartImage", "assets/charts/workforce_readiness_chart.png"), 0.78, 1.90, 6.89, 4.78)

            for idx, per in enumerate(sc.get("personas", [])):
                py = 1.78 + idx * 1.29
                col_rgb = hex_rgb(per["color"])
                add_rect(slide, 8.02, py, 4.66, 1.14, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, 8.02, py, 0.08, 1.14, fill=col_rgb, border=None, rounded=False)
                add_picture_fit(slide, ROOT / per["icon"], 8.20, py + 0.34, 0.46, 0.46)
                add_textbox(slide, 8.76, py + 0.12, 2.46, 0.38, per["role"], font_size=12, bold=True, color=C_INK, font_name=FONT_DISPLAY)
                add_rect(slide, 11.24, py + 0.14, 1.32, 0.28, fill=C_ICE_BLUE, border=col_rgb, border_pt=0.6)
                add_textbox(slide, 11.24, py + 0.14, 1.32, 0.28, per["lift"], font_size=9.0, bold=True, color=col_rgb, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
                add_textbox(slide, 8.76, py + 0.50, 3.78, 0.56, per["action"], font_size=10.8, color=C_INK_2, valign=MSO_ANCHOR.MIDDLE)
            set_notes(slide, base_notes)

        elif layout == "touchpoints_grid":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_BLUE, total, ICONS / "badge_sparkle.png")
            for idx, lv in enumerate(sc.get("levers", [])):
                lx = 0.65 + idx * 3.06
                lcol = hex_rgb(lv["color"])
                add_rect(slide, lx, 1.74, 2.84, 0.74, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, lx, 1.74, 2.84, 0.07, fill=lcol, border=None, rounded=False)
                add_textbox(slide, lx + 0.12, 1.84, 2.60, 0.26, lv["title"], font_size=12.2, bold=True, color=lcol, font_name=FONT_DISPLAY)
                add_textbox(slide, lx + 0.12, 2.11, 2.60, 0.32, lv["desc"], font_size=10.4, color=C_INK_2)

            for idx, tp in enumerate(sc.get("touchpoints", [])):
                row = idx // 4
                col = idx % 4
                tx = 0.65 + col * 3.06
                ty = 2.66 + row * 2.12
                tcol = hex_rgb(tp["color"])
                add_rect(slide, tx, ty, 2.84, 1.94, fill=C_WHITE, border=C_BORDER_BLUE)
                add_rect(slide, tx, ty, 2.84, 0.08, fill=tcol, border=None, rounded=False)
                add_picture_fit(slide, ROOT / tp["icon"], tx + 0.16, ty + 0.24, 0.46, 0.46)
                add_textbox(slide, tx + 0.72, ty + 0.22, 1.96, 0.50, tp["title"], font_size=13.5, bold=True, color=C_INK, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
                add_textbox(slide, tx + 0.16, ty + 0.80, 2.52, 1.00, tp["desc"], font_size=11.8, color=C_INK_2, valign=MSO_ANCHOR.MIDDLE)
            set_notes(slide, base_notes)

        elif layout == "pillar_functions_map":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_COBALT, total, ICONS / "pillar_workforce.png")
            add_rect(slide, 0.65, 1.72, 12.03, 0.48, fill=C_ICE_BLUE, border=C_BLUE, border_pt=1.25)
            add_picture_fit(slide, ICONS / "badge_sparkle.png", 0.84, 1.80, 0.32, 0.32)
            add_textbox(slide, 1.24, 1.76, 11.2, 0.40, sc.get("banner", "OFFICE OF THE CHRO · 6 PILLARS · 25 BUSINESS FUNCTIONS"), font_size=12.4, bold=True, color=C_COBALT, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

            for idx, item in enumerate(sc.get("pillarsData", [])):
                p = pillars_map[item["pillarId"]]
                p_rgb = hex_rgb(p["color"])
                p_icon = PILLAR_ICON_MAP.get(p["id"], ICONS / "badge_sparkle.png")
                row = idx // 3
                col = idx % 3
                px = 0.65 + col * 4.08
                py = 2.36 + row * 2.28
                add_rect(slide, px, py, 3.88, 2.12, fill=C_SURFACE, border=C_BORDER_BLUE)
                add_rect(slide, px, py, 3.88, 0.08, fill=p_rgb, border=None, rounded=False)
                add_picture_fit(slide, p_icon, px + 0.16, py + 0.18, 0.44, 0.44)
                add_textbox(slide, px + 0.68, py + 0.15, 3.04, 0.22, p["apqcBadge"], font_size=9.2, bold=True, color=p_rgb, font_name=FONT_DISPLAY)
                add_textbox(slide, px + 0.68, py + 0.36, 3.04, 0.34, p.get("shortName", p["name"]), font_size=13.2, bold=True, color=C_INK, font_name=FONT_DISPLAY)

                add_rect(slide, px + 0.16, py + 0.76, 3.56, 0.34, fill=C_WHITE, border=p_rgb, border_pt=0.8)
                add_textbox(slide, px + 0.22, py + 0.78, 3.44, 0.30, item["outcome"], font_size=11.4, bold=True, color=p_rgb, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

                for f_idx, fn_lbl in enumerate(item.get("functions", [])[:4]):
                    fr = f_idx // 2
                    fc = f_idx % 2
                    fx = px + 0.16 + fc * 1.81
                    fy = py + 1.20 + fr * 0.42
                    add_rect(slide, fx, fy, 1.75, 0.36, fill=C_WHITE, border=C_BORDER, border_pt=0.75)
                    add_textbox(slide, fx + 0.05, fy + 0.03, 1.65, 0.30, fn_lbl, font_size=10.2, bold=True, color=C_INK_2, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
            set_notes(slide, base_notes)

        elif layout == "pillar_value_pair":
            add_slide_chrome(slide, sc["eyebrow"], sc["title"], sc["subtitle"], sc["num"], C_BLUE, total, ICONS / "pillar_perform.png")
            if sc.get("topBanner"):
                add_rect(slide, 0.65, 1.72, 12.03, 0.50, fill=C_ICE_BLUE, border=C_BORDER_BLUE)
                add_picture_fit(slide, ICONS / "badge_sparkle.png", 0.82, 1.82, 0.30, 0.30)
                add_textbox(slide, 1.20, 1.76, 11.30, 0.42, sc["topBanner"], font_size=12, bold=True, color=C_COBALT, valign=MSO_ANCHOR.MIDDLE)

            for idx, c in enumerate(sc.get("cards", [])):
                cx = 0.65 + idx * 6.17
                cy = 2.38
                cw = 5.86
                ch = 4.44
                ccol = hex_rgb(c["color"])
                add_rect(slide, cx, cy, cw, ch, fill=C_WHITE, border=C_BORDER_BLUE, border_pt=1.35)
                add_rect(slide, cx, cy, cw, 0.09, fill=ccol, border=None, rounded=False)
                add_picture_fit(slide, ROOT / c["icon"], cx + 0.20, cy + 0.24, 0.56, 0.56)
                add_textbox(slide, cx + 0.84, cy + 0.20, 3.25, 0.24, c["badge"], font_size=9.5, bold=True, color=ccol, font_name=FONT_DISPLAY)
                add_textbox(slide, cx + 0.84, cy + 0.43, 3.25, 0.54, c["title"], font_size=14, bold=True, color=C_INK, font_name=FONT_DISPLAY)

                add_rect(slide, cx + 4.16, cy + 0.20, 1.50, 0.78, fill=C_SURFACE, border=ccol, border_pt=1.0)
                add_textbox(slide, cx + 4.20, cy + 0.24, 1.42, 0.42, c["metric"], font_size=18.5, bold=True, color=ccol, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER)
                add_textbox(slide, cx + 4.20, cy + 0.67, 1.42, 0.24, c["metricLbl"], font_size=7.8, bold=True, color=C_MUTED, align=PP_ALIGN.CENTER)

                strips = [
                    ("TODAY'S FRICTION", c["problem"], C_RED_BG, C_RED, ICONS / "badge_clock.png"),
                    ("AI SOLUTION", c["solution"], C_ICE_BLUE, ccol, ICONS / "badge_sparkle.png"),
                    ("BUSINESS OUTCOME", c["value"], C_GREEN_BG, C_GREEN, ICONS / "badge_check.png"),
                ]
                for s_idx, (st_lbl, st_txt, st_bg, st_col, st_icon) in enumerate(strips):
                    sy = cy + 1.12 + s_idx * 1.08
                    add_rect(slide, cx + 0.20, sy, cw - 0.40, 0.96, fill=st_bg, border=st_col, border_pt=0.8)
                    add_rect(slide, cx + 0.20, sy, 0.08, 0.96, fill=st_col, border=None, rounded=False)
                    add_picture_fit(slide, st_icon, cx + 0.36, sy + 0.10, 0.22, 0.22)
                    add_textbox(slide, cx + 0.64, sy + 0.09, cw - 0.96, 0.24, st_lbl, font_size=9.5, bold=True, color=st_col, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
                    add_textbox(slide, cx + 0.36, sy + 0.35, cw - 0.68, 0.56, st_txt, font_size=11.6, color=C_INK, valign=MSO_ANCHOR.MIDDLE)
            set_notes(slide, base_notes)

        elif layout == "adoption_close":
            add_og_faded_bg(slide)
            add_rect(slide, 0.0, 0.0, 13.333, 0.12, fill=C_BLUE, border=None, rounded=False)
            add_rect(slide, 0.65, 0.42, 5.4, 0.32, fill=C_ICE_BLUE, border=C_BORDER_BLUE)
            add_textbox(slide, 0.78, 0.44, 5.14, 0.28, sc["eyebrow"], font_size=9.5, bold=True, color=C_COBALT, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
            add_textbox(slide, 0.65, 0.82, 7.60, 0.72, sc["title"], font_size=23, bold=True, color=C_INK, font_name=FONT_DISPLAY)
            add_textbox(slide, 0.65, 1.56, 7.50, 0.46, sc["subtitle"], font_size=12.5, color=C_MUTED)

            for idx, ap in enumerate(sc.get("adoptionPillars", [])):
                ax = 0.65 + (idx % 2) * 3.84
                ay = 2.16 + (idx // 2) * 1.12
                acol = hex_rgb(ap["color"])
                add_rect(slide, ax, ay, 3.68, 0.98, fill=C_SURFACE, border=C_BORDER)
                add_rect(slide, ax, ay, 3.68, 0.07, fill=acol, border=None, rounded=False)
                add_picture_fit(slide, ROOT / ap["icon"], ax + 0.14, ay + 0.24, 0.44, 0.44)
                add_textbox(slide, ax + 0.64, ay + 0.15, 2.92, 0.24, f"{ap['num']} · {ap['title']}", font_size=11.8, bold=True, color=acol, font_name=FONT_DISPLAY)
                add_textbox(slide, ax + 0.64, ay + 0.42, 2.92, 0.50, ap["desc"], font_size=10.4, color=C_INK_2, valign=MSO_ANCHOR.MIDDLE)

            for idx, st in enumerate(sc.get("ctaBoxes", [])):
                sy = 4.48 + idx * 0.80
                scol = hex_rgb(st["color"])
                add_rect(slide, 0.65, sy, 7.52, 0.68, fill=C_WHITE, border=scol, border_pt=1.25)
                add_circle(slide, 0.80, sy + 0.14, 0.40, scol)
                add_textbox(slide, 0.80, sy + 0.14, 0.40, 0.40, st["num"], font_size=11.5, bold=True, color=C_WHITE, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
                add_textbox(slide, 1.32, sy + 0.07, 5.45, 0.25, st["title"], font_size=12, bold=True, color=scol, font_name=FONT_DISPLAY)
                add_textbox(slide, 1.32, sy + 0.34, 5.45, 0.28, st["desc"], font_size=10.6, color=C_INK_2)
                add_picture_fit(slide, ROOT / st["icon"], 6.95, sy + 0.14, 0.40, 0.40)

            roadmap_img = ROOT / sc.get("heroImage", "assets/roadmap_launch.jpg")
            add_picture_fit(slide, roadmap_img, 8.38, 1.05, 4.35, 5.60)
            add_brand_footer(slide, sc["num"], total)
            add_four_color_strip(slide)
            set_notes(slide, base_notes)

        elif layout == "closing":
            add_og_faded_bg(slide)
            add_rect(slide, 0.0, 0.0, 13.333, 0.12, fill=C_BLUE, border=None, rounded=False)
            add_rect(slide, 0.72, 0.62, 5.2, 0.34, fill=C_ICE_BLUE, border=C_BORDER_BLUE)
            add_textbox(slide, 0.84, 0.64, 4.96, 0.30, sc["eyebrow"], font_size=10, bold=True, color=C_COBALT, font_name=FONT_DISPLAY, valign=MSO_ANCHOR.MIDDLE)
            add_textbox(slide, 0.72, 1.08, 7.25, 0.92, sc["title"], font_size=28, bold=True, color=C_INK, font_name=FONT_DISPLAY)
            add_textbox(slide, 0.72, 2.08, 7.15, 0.66, sc["subtitle"], font_size=14.5, color=C_MUTED)

            raw_cta = sc.get("ctaBoxes")
            if raw_cta:
                cta_boxes = [
                    (b["num"], b["title"], b["desc"], hex_rgb(b["color"]), ROOT / b["icon"])
                    for b in raw_cta
                ]
            else:
                cta_boxes = [
                    ("01", "Today's Builder Lab", "Policy Agent: Vertex AI RAG vs. OKF + MCP", C_BLUE, GCP / "Developer_Tools-512-color.png"),
                    ("02", "Week 1 Quick Wins", "Ship No-Code Policy Pilot & Onboarding Guide", C_GREEN, ICONS / "badge_nocode.png"),
                    ("03", "Quarter 1 Scale", "Deploy ADK Concierge & Career Saathi Mobility", C_PURPLE, GCP / "Agents-512-color.png"),
                ]
            for idx, (num, ct, cd, ccol, cicon) in enumerate(cta_boxes):
                cy = 2.94 + idx * 1.28
                add_rect(slide, 0.72, cy, 7.15, 1.04, fill=C_SURFACE, border=ccol, border_pt=1.35)
                add_circle(slide, 0.90, cy + 0.24, 0.56, ccol)
                add_textbox(slide, 0.90, cy + 0.24, 0.56, 0.56, num, font_size=15, bold=True, color=C_WHITE, font_name=FONT_DISPLAY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
                add_textbox(slide, 1.62, cy + 0.16, 5.2, 0.34, ct, font_size=15, bold=True, color=ccol, font_name=FONT_DISPLAY)
                add_textbox(slide, 1.62, cy + 0.52, 5.2, 0.38, cd, font_size=12.5, color=C_INK_2)
                add_picture_fit(slide, cicon, 7.05, cy + 0.22, 0.60, 0.60)

            roadmap_img = ASSETS / "roadmap_launch.jpg"
            add_picture_fit(slide, roadmap_img if roadmap_img.exists() else ASSETS / "hero_chro_keynote.jpg", 8.10, 1.15, 4.65, 5.45)
            add_brand_footer(slide, sc["num"], total)
            add_four_color_strip(slide)
            set_notes(slide, base_notes)

    prs.save(out_path)
    print(f"Generated visual PPTX ({version_tag_label(footer_label)}): {out_path} ({len(prs.slides)} slides, 16:9 Simple Light theme)")


def version_tag_label(label: str) -> str:
    return label or "Keynote"


def build_deck(version: str = "both") -> None:
    cat = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    if version in ("v1", "both"):
        build_single_deck(cat, cat["keynoteSlides"], OUT_PPTX, "v1 Architecture Deck")
    if version in ("v2", "both") and cat.get("keynoteSlidesV2"):
        build_single_deck(cat, cat["keynoteSlidesV2"], OUT_PPTX_V2, "v2 Stage Keynote")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build CHRO Keynote PPTX v1 and/or v2 decks.")
    parser.add_argument("--version", choices=("v1", "v2", "both"), default="both")
    args = parser.parse_args()
    build_deck(args.version)
