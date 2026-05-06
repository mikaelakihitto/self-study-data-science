from __future__ import annotations

from pathlib import Path
import re

from manim import *


BACKGROUND = "#0B1020"
PANEL_FILL = "#151B2F"
SURFACE_FILL = "#11182A"
SURFACE_ALT = "#16243A"

TEXT_MAIN = GREY_A
TEXT_MUTED = GREY_B
TITLE_COLOR = BLUE_B

ACCENT_BLUE = BLUE_C
ACCENT_CYAN = TEAL_C
ACCENT_GREEN = GREEN_C
ACCENT_YELLOW = YELLOW_C
ACCENT_ORANGE = ORANGE
ACCENT_RED = RED_C
ACCENT_PURPLE = PURPLE_B

DEFAULT_MATH_TOKENS = (
    "\\",
    "_",
    "^",
    "{",
    "}",
    "=",
    r"\cdots",
    r"\ldots",
    r"\tilde",
    r"\mathbb",
)


def configure_manim_output(
    file_path,
    *,
    media_subdir: str = "assets",
    pixel_width: int | None = None,
    pixel_height: int | None = None,
    background_color=None,
):
    base_dir = Path(file_path).resolve().parents[1]
    assets_dir = base_dir / media_subdir
    assets_dir.mkdir(parents=True, exist_ok=True)

    config.media_dir = str(assets_dir)
    if pixel_width is not None:
        config.pixel_width = pixel_width
    if pixel_height is not None:
        config.pixel_height = pixel_height
    if background_color is not None:
        config.background_color = background_color

    return base_dir, assets_dir


def configure_default_video_output(file_path):
    return configure_manim_output(
        file_path,
        pixel_width=1920,
        pixel_height=1080,
        background_color=BACKGROUND,
    )


def create_title(text: str, font_size: int = 40, color=TITLE_COLOR, edge=UP, buff: float = 0.35) -> Text:
    return Text(text, font_size=font_size, color=color).to_edge(edge, buff=buff)


def create_caption(text: str, color=TEXT_MUTED, font_size: int = 24) -> Text:
    return Text(text, font_size=font_size, color=color)


def create_auto_label(
    label: str,
    font_size: int = 28,
    color=WHITE,
    math_tokens=DEFAULT_MATH_TOKENS,
    text_scale: float = 0.72,
    min_text_font_size: int = 18,
):
    has_accented_text = re.search(r"[À-ÿ]", label) is not None
    has_layout_text = (" " in label) or ("\n" in label)
    uses_mathtex = not has_accented_text and not has_layout_text and any(token in label for token in math_tokens)

    if uses_mathtex:
        return MathTex(label, font_size=font_size, color=color)
    return Text(label, font_size=max(int(font_size * text_scale), min_text_font_size), color=color)


def create_chip(
    label: str,
    color=ACCENT_BLUE,
    font_size: int = 26,
    text_color=TEXT_MAIN,
    fill_color=SURFACE_FILL,
    fill_opacity: float = 0.98,
    stroke_width: float = 2.4,
    height: float = 0.78,
    horizontal_padding: float = 0.6,
    corner_radius: float = 0.18,
    label_factory=None,
):
    label_factory = label_factory or create_caption
    text = label_factory(label, font_size=font_size, color=text_color)
    frame = RoundedRectangle(
        corner_radius=corner_radius,
        width=text.width + horizontal_padding,
        height=height,
        stroke_color=color,
        stroke_width=stroke_width,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
    )
    text.move_to(frame.get_center())
    return VGroup(frame, text)


def create_box(
    title: str,
    subtitle: str = "",
    width: float = 3.1,
    height: float = 1.6,
    color=ACCENT_BLUE,
    fill_color=PANEL_FILL,
    fill_opacity: float = 0.96,
    title_size: int = 28,
    subtitle_size: int = 20,
    title_color=None,
    subtitle_color=TEXT_MAIN,
    content_buff: float = 0.1,
    corner_radius: float = 0.18,
    stroke_width: float = 2.8,
    title_factory=None,
    subtitle_factory=None,
):
    title_factory = title_factory or create_caption
    subtitle_factory = subtitle_factory or create_caption
    title_color = title_color or color

    frame = RoundedRectangle(
        corner_radius=corner_radius,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=stroke_width,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
    )
    title_mob = title_factory(title, font_size=title_size, color=title_color)
    if subtitle:
        subtitle_mob = subtitle_factory(subtitle, font_size=subtitle_size, color=subtitle_color)
        content = VGroup(title_mob, subtitle_mob).arrange(DOWN, buff=content_buff)
    else:
        content = title_mob
    content.move_to(frame.get_center())
    return VGroup(frame, content)


def create_panel(
    body,
    title: str | None = None,
    color=ACCENT_BLUE,
    padding: float = 0.24,
    min_width: float = 0.0,
    min_height: float = 0.0,
    fill_color=PANEL_FILL,
    fill_opacity: float = 0.92,
    corner_radius: float = 0.18,
    stroke_width: float = 2.6,
    title_font_size: int = 30,
    title_buff: float = 0.18,
    title_factory=None,
):
    content = body
    if title:
        title_factory = title_factory or create_caption
        title_mob = title_factory(title, font_size=title_font_size, color=color)
        content = VGroup(title_mob, body).arrange(DOWN, buff=title_buff)

    frame = RoundedRectangle(
        corner_radius=corner_radius,
        width=max(content.width + 2 * padding, min_width),
        height=max(content.height + 2 * padding, min_height),
        stroke_color=color,
        stroke_width=stroke_width,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
    )
    content.move_to(frame.get_center())
    return VGroup(frame, content)


def vector_tex(values) -> str:
    parts = []
    for value in values:
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, int):
            parts.append(str(value))
        else:
            parts.append(f"{value:.2f}")
    return r"[" + r",\,".join(parts) + r"]"


def create_vector_visual(
    label: str,
    values,
    color=ACCENT_GREEN,
    width: float = 4.6,
    height: float = 1.45,
    fill_color=PANEL_FILL,
    fill_opacity: float = 0.96,
    label_font_size: int = 28,
    vector_font_size: int = 34,
    label_buff: float = 0.14,
    corner_radius: float = 0.18,
    stroke_width: float = 2.8,
    horizontal_padding: float = 0.55,
    vertical_padding: float = 0.38,
):
    label_mob = Text(label, font_size=label_font_size, color=color)
    vector_mob = MathTex(vector_tex(values), font_size=vector_font_size, color=TEXT_MAIN)
    content = VGroup(label_mob, vector_mob).arrange(DOWN, buff=label_buff)
    frame = RoundedRectangle(
        corner_radius=corner_radius,
        width=max(width, content.width + horizontal_padding),
        height=max(height, content.height + vertical_padding),
        stroke_color=color,
        stroke_width=stroke_width,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
    )
    content.move_to(frame.get_center())
    return VGroup(frame, content)


def create_arrow(start, end, color=TEXT_MUTED, buff: float = 0.14, stroke_width: float = 4, tip_ratio: float = 0.14):
    return Arrow(
        start,
        end,
        buff=buff,
        stroke_width=stroke_width,
        color=color,
        max_tip_length_to_length_ratio=tip_ratio,
    )


def create_arrow_between(
    source,
    target,
    color=TEXT_MUTED,
    buff: float = 0.14,
    stroke_width: float = 4,
    from_edge=RIGHT,
    to_edge=LEFT,
    tip_ratio: float = 0.14,
):
    return create_arrow(
        source.get_edge_center(from_edge),
        target.get_edge_center(to_edge),
        color=color,
        buff=buff,
        stroke_width=stroke_width,
        tip_ratio=tip_ratio,
    )


def create_vertical_arrow_between(source, target, color=TEXT_MUTED, buff: float = 0.14, stroke_width: float = 4):
    return create_arrow_between(
        source,
        target,
        color=color,
        buff=buff,
        stroke_width=stroke_width,
        from_edge=DOWN,
        to_edge=UP,
    )


def clear_scene(scene: Scene, *keep, run_time: float = 0.8):
    fade_targets = []
    for mob in list(scene.mobjects):
        if not any(mob is item for item in keep):
            fade_targets.append(mob)
    if fade_targets:
        scene.play(*[FadeOut(mob) for mob in fade_targets], run_time=run_time)
