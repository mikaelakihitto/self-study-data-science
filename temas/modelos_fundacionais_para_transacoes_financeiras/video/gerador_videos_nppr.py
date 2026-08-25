from pathlib import Path
import sys

from manim import *

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from temas.utils.manim_utils import (
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_PURPLE,
    ACCENT_RED,
    ACCENT_YELLOW,
    PANEL_FILL,
    SURFACE_FILL,
    TEXT_MAIN,
    TEXT_MUTED,
    TITLE_COLOR,
    configure_default_video_output,
    create_arrow,
    create_arrow_between,
    create_auto_label,
    create_panel as build_panel,
    create_title as build_title,
)


BASE_DIR, ASSETS_DIR = configure_default_video_output(__file__)


"""
Render examples:
  manim -pqh temas/modelos_fundacionais_para_transacoes_financeiras/video/gerador_videos_nppr.py Scene1Intuition
  manim -pqh temas/modelos_fundacionais_para_transacoes_financeiras/video/gerador_videos_nppr.py Scene4NumericalLoss
  manim -pqh temas/modelos_fundacionais_para_transacoes_financeiras/video/gerador_videos_nppr.py Scene7FinalIntuition
"""


BACKGROUND_FILL = PANEL_FILL


def create_title(text: str) -> Text:
    return build_title(text, font_size=38)


create_label_mobject = create_auto_label


def create_event_box(
    label: str,
    width: float = 1.2,
    height: float = 0.86,
    color=ACCENT_BLUE,
    font_size: int = 28,
):
    frame = RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.8,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.95,
    )
    text = create_label_mobject(label, font_size=font_size, color=color).move_to(frame.get_center())
    return VGroup(frame, text)


def create_transaction_box(
    label: str,
    subtitle: str,
    width: float = 2.05,
    height: float = 1.05,
    accent_color=ACCENT_BLUE,
    label_font_size: int = 26,
    subtitle_font_size: int = 18,
):
    frame = RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=height,
        stroke_color=accent_color,
        stroke_width=2.8,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.96,
    )
    title = create_label_mobject(label, font_size=label_font_size, color=accent_color)
    subtitle_mob = Text(subtitle, font_size=subtitle_font_size, color=TEXT_MAIN)
    content = VGroup(title, subtitle_mob).arrange(DOWN, buff=0.08).move_to(frame.get_center())
    return VGroup(frame, content)


def create_feature_chip(
    title: str,
    value: str,
    width: float = 2.2,
    height: float = 0.72,
    color=ACCENT_BLUE,
):
    frame = RoundedRectangle(
        corner_radius=0.14,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.2,
        fill_color=SURFACE_FILL,
        fill_opacity=0.98,
    )
    title_text = create_label_mobject(title, font_size=22, color=color)
    value_text = create_label_mobject(value, font_size=24, color=TEXT_MAIN)
    content = VGroup(title_text, value_text).arrange(RIGHT, buff=0.14).move_to(frame.get_center())
    return VGroup(frame, content)


def create_panel(body, title: str | None = None, color=ACCENT_BLUE, padding: float = 0.24, min_width: float = 0.0, min_height: float = 0.0):
    return build_panel(
        body,
        title=title,
        color=color,
        padding=padding,
        min_width=min_width,
        min_height=min_height,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.92,
        title_font_size=30,
        title_factory=create_label_mobject,
    )


def create_timeline(
    labels,
    widths=None,
    colors=None,
    font_size: int = 28,
    height: float = 0.86,
    gap: float = 0.46,
):
    widths = widths or [1.2] * len(labels)
    colors = colors or [ACCENT_BLUE] * len(labels)
    boxes = VGroup(
        *[
            create_event_box(
                labels[index],
                width=widths[index],
                height=height,
                color=colors[index],
                font_size=font_size,
            )
            for index in range(len(labels))
        ]
    )
    boxes.arrange(RIGHT, buff=gap)
    arrows = VGroup(
        *[
            Arrow(
                boxes[index].get_right(),
                boxes[index + 1].get_left(),
                buff=0.08,
                stroke_width=3,
                color=TEXT_MUTED,
                max_tip_length_to_length_ratio=0.14,
            )
            for index in range(len(boxes) - 1)
        ]
    )
    return {"group": VGroup(boxes, arrows), "boxes": boxes, "arrows": arrows}


def create_vertical_arrow(start, end, color=TEXT_MUTED, buff: float = 0.12, stroke_width: float = 4):
    return create_arrow(
        start,
        end,
        color=color,
        buff=buff,
        stroke_width=stroke_width,
        tip_ratio=0.16,
    )


def create_encoder_block(label: str = "Encoder", width: float = 2.5, height: float = 1.75):
    frame = RoundedRectangle(
        corner_radius=0.22,
        width=width,
        height=height,
        stroke_color=ACCENT_GREEN,
        stroke_width=3,
        fill_color=SURFACE_FILL,
        fill_opacity=0.98,
    )
    bars = VGroup(
        *[
            RoundedRectangle(
                corner_radius=0.08,
                width=0.26,
                height=0.82,
                stroke_width=0,
                fill_color=ACCENT_GREEN,
                fill_opacity=opacity,
            )
            for opacity in (0.35, 0.6, 0.85)
        ]
    ).arrange(RIGHT, buff=0.12)
    bars.move_to(frame.get_center()).shift(0.22 * UP)
    text = Text(label, font_size=23, color=TEXT_MAIN).next_to(bars, DOWN, buff=0.16)
    return VGroup(frame, bars, text)


def create_decoder_block(label: str = "D", subtitle: str = "decoder", width: float = 2.15, height: float = 1.55, color=ACCENT_RED):
    frame = RoundedRectangle(
        corner_radius=0.22,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=3,
        fill_color=SURFACE_FILL,
        fill_opacity=0.98,
    )
    circles = VGroup(
        *[
            Circle(radius=0.1, stroke_width=0, fill_color=color, fill_opacity=opacity)
            for opacity in (0.4, 0.7, 1.0)
        ]
    ).arrange(RIGHT, buff=0.14)
    circles.move_to(frame.get_center()).shift(0.2 * UP)
    label_mob = create_label_mobject(label, font_size=28, color=color)
    subtitle_mob = Text(subtitle, font_size=17, color=TEXT_MAIN)
    text_group = VGroup(label_mob, subtitle_mob).arrange(DOWN, buff=0.06)
    text_group.move_to(frame.get_center() + 0.18 * DOWN)
    return VGroup(frame, circles, text_group)


def create_embedding_vector(
    tex: str = r"e_t = [0.12,\,-0.45,\,0.88,\,\ldots,\,0.31]",
    width: float = 4.2,
    height: float = 1.18,
    color=ACCENT_YELLOW,
    font_size: int = 28,
):
    frame = RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.8,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.95,
    )
    label = MathTex(tex, font_size=font_size, color=TEXT_MAIN).move_to(frame.get_center())
    return VGroup(frame, label)


def create_probability_bars(
    categories,
    probs,
    highlight_index: int = 0,
    bar_width: float = 1.7,
    row_gap: float = 0.18,
):
    rows = VGroup()
    for index, (category, prob) in enumerate(zip(categories, probs)):
        label = Text(category, font_size=17, color=TEXT_MAIN)
        background = RoundedRectangle(
            corner_radius=0.06,
            width=bar_width,
            height=0.18,
            stroke_width=0,
            fill_color=GREY_E,
            fill_opacity=0.28,
        )
        fill = RoundedRectangle(
            corner_radius=0.06,
            width=max(bar_width * prob, 0.08),
            height=0.18,
            stroke_width=0,
            fill_color=ACCENT_YELLOW if index == highlight_index else ACCENT_BLUE,
            fill_opacity=0.95 if index == highlight_index else 0.65,
        )
        fill.align_to(background, LEFT)
        value = Text(f"{int(prob * 100)}%", font_size=16, color=TEXT_MUTED)
        bar_group = VGroup(background, fill)
        row = VGroup(label, bar_group, value).arrange(RIGHT, buff=0.16)
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=row_gap)
    return rows


def create_loss_box(
    title: str,
    subtitle: str,
    width: float = 1.95,
    height: float = 0.95,
    color=ACCENT_RED,
):
    frame = RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.4,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.95,
    )
    title_mob = create_label_mobject(title, font_size=28, color=color)
    subtitle_mob = Text(subtitle, font_size=16, color=TEXT_MAIN)
    content = VGroup(title_mob, subtitle_mob).arrange(DOWN, buff=0.05).move_to(frame.get_center())
    return VGroup(frame, content)


def create_task_card(
    title: str,
    subtitle: str,
    width: float = 2.35,
    height: float = 0.95,
    color=ACCENT_BLUE,
):
    frame = RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.95,
    )
    title_mob = Text(title, font_size=21, color=color)
    subtitle_mob = Text(subtitle, font_size=15, color=TEXT_MAIN)
    content = VGroup(title_mob, subtitle_mob).arrange(DOWN, buff=0.06).move_to(frame.get_center())
    return VGroup(frame, content)


class Scene01NPPROverview(Scene):
    def construct(self):
        title = create_title("NPPR: aprendendo com o futuro e com o passado")

        timeline = create_timeline(
            [r"x_0", r"x_1", r"x_2", r"x_3", r"x_t", r"x_{t+1}"],
            widths=[1.05, 1.05, 1.05, 1.05, 1.1, 1.35],
            colors=[ACCENT_BLUE, ACCENT_BLUE, ACCENT_BLUE, ACCENT_BLUE, ACCENT_YELLOW, ACCENT_RED],
            font_size=28,
        )
        timeline["group"].move_to(1.55 * UP)
        focus = SurroundingRectangle(timeline["boxes"][4], color=ACCENT_YELLOW, buff=0.08, corner_radius=0.1)
        history_brace = Brace(VGroup(*timeline["boxes"][:5]), DOWN, color=ACCENT_BLUE, buff=0.16)
        history_label = Text("histórico até x_t", font_size=22, color=ACCENT_BLUE).next_to(history_brace, DOWN, buff=0.12)

        encoder = create_encoder_block("Encoder", width=2.25, height=1.55).move_to(3.2 * LEFT + 0.95 * DOWN)
        to_encoder = create_vertical_arrow(
            timeline["boxes"][4].get_bottom(),
            encoder.get_top(),
            color=TEXT_MUTED,
            buff=0.12,
            stroke_width=3,
        )
        embedding = create_embedding_vector(tex=r"e_t", width=2.0, height=0.9, font_size=32).move_to(0.65 * DOWN)
        to_embedding = create_arrow_between(encoder, embedding, buff=0.18, color=TEXT_MUTED, stroke_width=3)

        np_block = create_decoder_block(r"D_{NP}", "prever o\npróximo", width=2.45, height=1.7, color=ACCENT_RED)
        np_block.move_to(3.55 * RIGHT + 0.15 * UP)
        pr_block = create_decoder_block(r"D_{PR}", "reconstruir\no passado", width=2.45, height=1.7, color=ACCENT_PURPLE)
        pr_block.move_to(3.55 * RIGHT + 1.95 * DOWN)

        branch_np = Arrow(
            embedding.get_right(),
            np_block.get_left(),
            buff=0.16,
            stroke_width=3,
            color=TEXT_MUTED,
            max_tip_length_to_length_ratio=0.14,
        )
        branch_pr = Arrow(
            embedding.get_right(),
            pr_block.get_left(),
            buff=0.16,
            stroke_width=3,
            color=TEXT_MUTED,
            max_tip_length_to_length_ratio=0.14,
        )

        next_hint = create_transaction_box(
            r"\tilde{x}_{t+1}",
            "evento futuro",
            width=2.15,
            height=0.95,
            accent_color=ACCENT_RED,
            label_font_size=28,
        ).next_to(np_block, RIGHT, buff=0.25)
        past_hint = VGroup(
            create_event_box(r"\tilde{x}_{t-1}", width=1.25, color=ACCENT_PURPLE, font_size=26),
            create_event_box(r"\tilde{x}_{t-2}", width=1.25, color=ACCENT_PURPLE, font_size=26),
        ).arrange(RIGHT, buff=0.16).next_to(pr_block, RIGHT, buff=0.22)

        closing = Text(
            "O embedding e_t é treinado com dois objetivos complementares.",
            font_size=28,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.45)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(box, scale=0.9) for box in timeline["boxes"]], lag_ratio=0.12, run_time=1.5))
        self.play(LaggedStart(*[Create(arrow) for arrow in timeline["arrows"]], lag_ratio=0.1, run_time=1.0))
        self.play(Create(focus))
        self.play(FadeIn(history_brace), FadeIn(history_label, shift=0.1 * UP))

        background_events = VGroup(*timeline["boxes"][:4], *timeline["arrows"][:4], timeline["boxes"][5], timeline["arrows"][4])
        self.play(
            FadeOut(history_brace),
            FadeOut(history_label),
            background_events.animate.set_opacity(0.2),
            run_time=0.8,
        )

        self.play(FadeIn(encoder, scale=0.92), Create(to_encoder))
        self.play(Create(to_embedding), FadeIn(embedding, shift=0.18 * RIGHT))
        self.play(
            LaggedStart(
                Create(branch_np),
                FadeIn(np_block, shift=0.15 * RIGHT),
                FadeIn(next_hint, shift=0.15 * RIGHT),
                Create(branch_pr),
                FadeIn(pr_block, shift=0.15 * RIGHT),
                FadeIn(past_hint, shift=0.15 * RIGHT),
                lag_ratio=0.16,
                run_time=1.8,
            )
        )
        self.play(FadeOut(background_events), run_time=0.6)
        self.play(FadeIn(closing, shift=0.15 * UP))
        self.wait(1.0)


class Scene02NextEventPrediction(Scene):
    def construct(self):
        title = create_title("Next Event Prediction")

        timeline = create_timeline(
            [r"x_0", r"x_1", r"x_2", r"x_t", r"x_{t+1}"],
            widths=[1.05, 1.05, 1.05, 1.1, 1.35],
            colors=[ACCENT_BLUE, ACCENT_BLUE, ACCENT_BLUE, ACCENT_YELLOW, ACCENT_RED],
            font_size=28,
        )
        timeline["group"].move_to(2.15 * UP)
        focus = SurroundingRectangle(timeline["boxes"][3], color=ACCENT_YELLOW, buff=0.08, corner_radius=0.1)

        encoder = create_encoder_block("Encoder", width=2.2, height=1.55).move_to(4.8 * LEFT + 0.25 * DOWN)
        embedding = create_embedding_vector(tex=r"e_t", width=2.0, height=0.9, font_size=32).move_to(2.4 * LEFT + 0.25 * DOWN)
        decoder = create_decoder_block(r"D_{NP}", "decoder do\npróximo evento", width=2.4, height=1.75, color=ACCENT_RED)
        decoder.move_to(0.3 * RIGHT + 0.25 * DOWN)

        to_encoder = create_vertical_arrow(
            timeline["boxes"][3].get_bottom(),
            encoder.get_top(),
            color=TEXT_MUTED,
            buff=0.12,
            stroke_width=3,
        )
        to_embedding = create_arrow_between(encoder, embedding, buff=0.18, color=TEXT_MUTED, stroke_width=3)
        to_decoder = create_arrow_between(embedding, decoder, buff=0.18, color=TEXT_MUTED, stroke_width=3)

        pred_title = create_transaction_box(
            r"\tilde{x}_{t+1}",
            "evento previsto",
            width=2.55,
            height=1.0,
            accent_color=ACCENT_RED,
            label_font_size=30,
        )
        pred_value = create_feature_chip("Valor", "R$120", width=1.9, color=ACCENT_YELLOW)
        pred_time = create_feature_chip("Horário", "20:30", width=1.9, color=ACCENT_BLUE)
        pred_bars = create_probability_bars(
            ["Restaurante", "Mercado", "Hotel"],
            [0.72, 0.18, 0.10],
            highlight_index=0,
        )
        pred_body = VGroup(
            pred_title,
            VGroup(pred_value, pred_time).arrange(RIGHT, buff=0.16),
            pred_bars,
        ).arrange(DOWN, buff=0.18)
        predicted_panel = create_panel(pred_body, title="Saida do decoder NP", color=ACCENT_RED, min_width=3.8, min_height=3.25)
        predicted_panel.move_to(4.45 * RIGHT + 0.55 * DOWN)

        true_event = create_panel(
            VGroup(
                create_feature_chip("Valor", "R$120", width=1.75, color=ACCENT_YELLOW),
                create_feature_chip("Categoria", "Restaurante", width=2.55, color=ACCENT_RED),
                create_feature_chip("Horário", "20:30", width=1.75, color=ACCENT_BLUE),
            ).arrange(DOWN, buff=0.15),
            title="Evento verdadeiro",
            color=ACCENT_GREEN,
            min_width=3.35,
            min_height=2.2,
        )
        true_event.next_to(predicted_panel, DOWN, buff=0.3)

        formula_one = MathTex(r"D_{NP}: \mathbb{R}^{d} \to X", font_size=32, color=TEXT_MUTED).move_to(4.7 * LEFT + 2.75 * DOWN)
        formula_two = MathTex(r"\tilde{x}_{t+1} = D_{NP}(e_t)", font_size=32, color=TEXT_MUTED).next_to(
            formula_one, DOWN, buff=0.22
        )
        closing = Text(
            "NP ensina o modelo a prever o próximo evento.",
            font_size=28,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.42)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(box, scale=0.9) for box in timeline["boxes"][:-1]], lag_ratio=0.14, run_time=1.2))
        self.play(LaggedStart(*[Create(arrow) for arrow in timeline["arrows"][:-1]], lag_ratio=0.12, run_time=0.7))
        self.play(Create(focus))
        self.play(FadeIn(encoder, scale=0.92), Create(to_encoder))
        self.play(Create(to_embedding), FadeIn(embedding, shift=0.15 * RIGHT))
        self.play(Create(to_decoder), FadeIn(decoder, scale=0.92))
        self.play(FadeIn(predicted_panel, shift=0.18 * RIGHT))
        self.play(FadeIn(timeline["boxes"][-1], scale=0.92), Create(timeline["arrows"][-1]))
        self.play(FadeIn(true_event, shift=0.15 * UP))
        self.play(FadeIn(formula_one, shift=0.12 * UP), FadeIn(formula_two, shift=0.12 * UP))
        self.play(FadeIn(closing, shift=0.15 * UP))
        self.wait(1.0)


NP_REAL_COLOR = ACCENT_BLUE
NP_PRED_COLOR = ORANGE
NP_LOSS_COLOR = ACCENT_RED
NP_MODEL_COLOR = ACCENT_GREEN
NP_HIGHLIGHT_COLOR = ACCENT_YELLOW


def create_np_feature_card(
    title: str,
    value: str,
    color=NP_REAL_COLOR,
    width: float = 3.0,
    height: float = 0.9,
    title_font_size: int = 20,
    value_font_size: int = 26,
):
    frame = RoundedRectangle(
        corner_radius=0.14,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.4,
        fill_color=SURFACE_FILL,
        fill_opacity=0.98,
    )
    title_mob = Text(title, font_size=title_font_size, color=color)
    value_mob = Text(value, font_size=value_font_size, color=TEXT_MAIN)
    content = VGroup(title_mob, value_mob).arrange(RIGHT, buff=0.18).move_to(frame.get_center())
    return VGroup(frame, content)


def create_np_metric_card(
    title: str,
    metric: str,
    value: str,
    color=NP_LOSS_COLOR,
    width: float = 2.45,
    height: float = 1.55,
):
    frame = RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.6,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.96,
    )
    title_mob = Text(title, font_size=22, color=TEXT_MAIN)
    metric_mob = Text(metric, font_size=18, color=color)
    value_mob = Text(value, font_size=32, color=color)
    content = VGroup(title_mob, metric_mob, value_mob).arrange(DOWN, buff=0.08).move_to(frame.get_center())
    return VGroup(frame, content)


def create_np_step_card(
    title: str,
    subtitle: str,
    color,
    width: float = 2.8,
    height: float = 1.2,
):
    frame = RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.6,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.96,
    )
    title_mob = Text(title, font_size=22, color=color)
    subtitle_mob = Text(subtitle, font_size=16, color=TEXT_MAIN)
    content = VGroup(title_mob, subtitle_mob).arrange(DOWN, buff=0.08).move_to(frame.get_center())
    return VGroup(frame, content)


def create_np_probability_rows(
    labels,
    probs,
    correct_index: int | None = None,
    bar_width: float = 2.3,
):
    rows = VGroup()
    for index, (label_text, prob) in enumerate(zip(labels, probs)):
        is_correct = correct_index == index
        label = Text(label_text, font_size=20, color=NP_REAL_COLOR if is_correct else TEXT_MAIN)
        background = RoundedRectangle(
            corner_radius=0.06,
            width=bar_width,
            height=0.2,
            stroke_width=0,
            fill_color=GREY_E,
            fill_opacity=0.3,
        )
        fill = RoundedRectangle(
            corner_radius=0.06,
            width=max(bar_width * prob, 0.08),
            height=0.2,
            stroke_width=0,
            fill_color=NP_PRED_COLOR,
            fill_opacity=1.0 if is_correct else 0.72,
        )
        fill.align_to(background, LEFT)
        value = Text(f"{prob:.2f}", font_size=18, color=NP_PRED_COLOR if is_correct else TEXT_MUTED)
        parts = [label, VGroup(background, fill), value]
        if is_correct:
            parts.append(Text("correta", font_size=16, color=NP_REAL_COLOR))
        rows.add(VGroup(*parts).arrange(RIGHT, buff=0.14))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    return rows


class Scene1Intuition(Scene):
    # Cena 1: visão geral da tarefa de prever a próxima transação.
    def construct(self):
        title = create_title("Next Event Prediction: intuicao")

        timeline = create_timeline(
            [r"x_1", r"x_2", r"x_3", r"x_4"],
            widths=[1.15, 1.15, 1.15, 1.15],
            colors=[NP_REAL_COLOR, NP_REAL_COLOR, NP_REAL_COLOR, NP_PRED_COLOR],
            font_size=30,
        )
        timeline["group"].move_to(2.3 * UP)
        current_focus = SurroundingRectangle(timeline["boxes"][2], color=NP_MODEL_COLOR, buff=0.08, corner_radius=0.1)
        next_focus = SurroundingRectangle(timeline["boxes"][3], color=NP_PRED_COLOR, buff=0.08, corner_radius=0.1)
        current_label = Text("x_t = transacao atual", font_size=22, color=NP_MODEL_COLOR).next_to(
            timeline["boxes"][2], UP, buff=0.16
        )
        next_label = Text("proxima transacao", font_size=22, color=NP_PRED_COLOR).next_to(
            timeline["boxes"][3], UP, buff=0.16
        )
        history_brace = Brace(VGroup(*timeline["boxes"][:3]), DOWN, color=NP_REAL_COLOR, buff=0.14)
        history_label = Text("historico ate x_t", font_size=24, color=NP_REAL_COLOR).next_to(
            history_brace, DOWN, buff=0.1
        )

        encoder = create_encoder_block("Encoder", width=2.3, height=1.6).move_to(4.6 * LEFT + 0.35 * DOWN)
        embedding = create_embedding_vector(tex=r"e_t", width=1.85, height=0.95, color=NP_MODEL_COLOR, font_size=36).move_to(
            2.0 * LEFT + 0.35 * DOWN
        )
        decoder = create_decoder_block(
            r"D_{NP}",
            "prever a\nproxima transacao",
            width=2.55,
            height=1.8,
            color=NP_MODEL_COLOR,
        ).move_to(0.75 * RIGHT + 0.35 * DOWN)
        prediction = create_panel(
            VGroup(
                create_np_feature_card("valor", "120", color=NP_PRED_COLOR, width=2.0),
                create_np_feature_card("categoria", "Supermercado", color=NP_PRED_COLOR, width=3.35),
            ).arrange(DOWN, buff=0.16),
            title=r"\hat{x}_{t+1}",
            color=NP_PRED_COLOR,
            min_width=3.8,
            min_height=2.5,
        ).move_to(4.65 * RIGHT + 0.35 * DOWN)

        to_encoder = create_vertical_arrow(
            timeline["boxes"][2].get_bottom(),
            encoder.get_top(),
            color=TEXT_MUTED,
            buff=0.12,
            stroke_width=3,
        )
        to_embedding = create_arrow_between(encoder, embedding, buff=0.18, color=TEXT_MUTED, stroke_width=3)
        to_decoder = create_arrow_between(embedding, decoder, buff=0.18, color=TEXT_MUTED, stroke_width=3)
        to_prediction = create_arrow_between(decoder, prediction, buff=0.18, color=TEXT_MUTED, stroke_width=3)

        analogy = Text(
            "Assim como um modelo de linguagem preve a proxima palavra, aqui o modelo tenta prever a proxima transacao.",
            font_size=24,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.4)
        formula = MathTex(r"\hat{x}_{t+1} = D_{NP}(e_t)", font_size=32, color=TEXT_MUTED).next_to(
            prediction, DOWN, buff=0.22
        )

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(box, scale=0.9) for box in timeline["boxes"]], lag_ratio=0.14, run_time=1.3))
        self.play(LaggedStart(*[Create(arrow) for arrow in timeline["arrows"]], lag_ratio=0.12, run_time=0.8))
        self.play(Create(current_focus), FadeIn(current_label, shift=0.1 * UP))
        self.play(Create(next_focus), FadeIn(next_label, shift=0.1 * UP))
        self.play(FadeIn(history_brace), FadeIn(history_label, shift=0.1 * UP))
        self.play(FadeIn(encoder, scale=0.92), Create(to_encoder))
        self.play(FadeIn(embedding, shift=0.15 * RIGHT), Create(to_embedding))
        self.play(FadeIn(decoder, scale=0.92), Create(to_decoder))
        self.play(FadeIn(prediction, shift=0.15 * RIGHT), Create(to_prediction))
        self.play(FadeIn(formula, shift=0.12 * UP))
        self.play(FadeIn(analogy, shift=0.12 * UP))
        self.wait(1.0)


class Scene2MultivariateTransaction(Scene):
    # Cena 2: a próxima transação é um vetor com várias features.
    def construct(self):
        title = create_title("Uma transacao e multivariada")

        headline = Text("A proxima transacao nao e um unico numero: ela tem varias features.", font_size=28, color=TEXT_MAIN).move_to(
            2.2 * UP
        )

        transaction = create_transaction_box(
            r"x_{t+1}",
            "transacao real",
            width=2.5,
            height=1.15,
            accent_color=NP_REAL_COLOR,
            label_font_size=30,
        ).move_to(4.6 * LEFT + 0.3 * UP)

        features = VGroup(
            create_np_feature_card("valor", "100", color=NP_REAL_COLOR, width=2.4),
            create_np_feature_card("categoria", "Supermercado", color=NP_REAL_COLOR, width=3.5),
            create_np_feature_card("pais", "Brasil", color=NP_REAL_COLOR, width=2.55),
        ).arrange(DOWN, buff=0.2)
        feature_panel = create_panel(
            features,
            title=r"x_{t+1} real",
            color=NP_REAL_COLOR,
            min_width=4.4,
            min_height=3.4,
        ).move_to(1.8 * RIGHT + 0.15 * UP)
        split_arrow = create_arrow_between(transaction, feature_panel, buff=0.2, color=TEXT_MUTED, stroke_width=3)

        numeric_tag = create_np_metric_card("valor", "feature numerica", "MSE", color=NP_HIGHLIGHT_COLOR, width=2.3, height=1.5)
        category_tag = create_np_metric_card("categoria", "feature categorica", "CE", color=NP_PRED_COLOR, width=2.65, height=1.5)
        country_tag = create_np_metric_card("pais", "feature categorica", "CE", color=NP_PRED_COLOR, width=2.3, height=1.5)
        tags = VGroup(numeric_tag, category_tag, country_tag).arrange(RIGHT, buff=0.25).move_to(1.95 * DOWN)

        closing = Text("O decoder NP precisa prever todas essas partes ao mesmo tempo.", font_size=26, color=TEXT_MAIN).to_edge(
            DOWN, buff=0.35
        )

        self.play(Write(title))
        self.play(FadeIn(headline, shift=0.12 * UP))
        self.play(FadeIn(transaction, scale=0.92))
        self.play(Create(split_arrow), FadeIn(feature_panel, shift=0.16 * RIGHT))
        self.play(LaggedStart(*[FadeIn(card, shift=0.12 * UP) for card in tags], lag_ratio=0.16, run_time=1.0))
        self.play(FadeIn(closing, shift=0.12 * UP))
        self.wait(1.0)


class Scene3DecoderOutput(Scene):
    # Cena 3: o decoder produz números para features numéricas e distribuições para categóricas.
    def construct(self):
        title = create_title("Saida do decoder NP")

        embedding = create_embedding_vector(tex=r"e_t", width=1.85, height=0.95, color=NP_MODEL_COLOR, font_size=36).move_to(
            4.9 * LEFT + 0.55 * UP
        )
        decoder = create_decoder_block(
            r"D_{NP}",
            "gera a previsao\ndo proximo evento",
            width=2.55,
            height=1.85,
            color=NP_MODEL_COLOR,
        ).move_to(2.2 * LEFT + 0.55 * UP)
        to_decoder = create_arrow_between(embedding, decoder, buff=0.18, color=TEXT_MUTED, stroke_width=3)

        value_card = create_np_feature_card("valor previsto", "120", color=NP_PRED_COLOR, width=2.8)
        category_panel = create_panel(
            create_np_probability_rows(
                ["Supermercado", "Restaurante", "Farmacia"],
                [0.70, 0.20, 0.10],
                correct_index=0,
            ),
            title="categoria prevista",
            color=NP_PRED_COLOR,
            min_width=4.9,
            min_height=2.05,
        )
        country_panel = create_panel(
            create_np_probability_rows(
                ["Brasil", "EUA", "Argentina"],
                [0.80, 0.15, 0.05],
                correct_index=0,
            ),
            title="pais previsto",
            color=NP_PRED_COLOR,
            min_width=4.9,
            min_height=2.05,
        )
        prediction_panel = create_panel(
            VGroup(value_card, category_panel, country_panel).arrange(DOWN, buff=0.18),
            title=r"\hat{x}_{t+1}",
            color=NP_PRED_COLOR,
            min_width=5.3,
            min_height=5.6,
        ).move_to(3.2 * RIGHT + 0.15 * DOWN)
        to_prediction = create_arrow_between(decoder, prediction_panel, buff=0.18, color=TEXT_MUTED, stroke_width=3)

        numeric_note = Text("features numericas viram numeros reais", font_size=22, color=TEXT_MAIN).move_to(3.5 * LEFT + 2.25 * DOWN)
        categorical_note = Text(
            "features categoricas viram distribuicoes de probabilidade",
            font_size=22,
            color=TEXT_MAIN,
        ).move_to(2.0 * RIGHT + 2.25 * DOWN)
        formula = MathTex(r"\hat{x}_{t+1} = D_{NP}(e_t)", font_size=32, color=TEXT_MUTED).to_edge(DOWN, buff=0.35)

        self.play(Write(title))
        self.play(FadeIn(embedding, scale=0.92))
        self.play(Create(to_decoder), FadeIn(decoder, scale=0.92))
        self.play(Create(to_prediction), FadeIn(prediction_panel, shift=0.18 * RIGHT))
        self.play(FadeIn(numeric_note, shift=0.12 * UP), FadeIn(categorical_note, shift=0.12 * UP))
        self.play(FadeIn(formula, shift=0.12 * UP))
        self.wait(1.0)


class Scene4NumericalLoss(Scene):
    # Cena 4: loss de uma feature numérica via MSE.
    def construct(self):
        title = create_title("Loss numerica: MSE no valor")

        real_card = create_np_feature_card("valor real", "100", color=NP_REAL_COLOR, width=2.35).move_to(2.15 * UP)
        pred_card = create_np_feature_card("valor previsto", "120", color=NP_PRED_COLOR, width=2.7).next_to(
            real_card, RIGHT, buff=0.32
        )
        cards = VGroup(real_card, pred_card).move_to(2.1 * UP)

        number_line = NumberLine(
            x_range=[80, 130, 10],
            length=8.5,
            include_numbers=True,
            color=TEXT_MUTED,
            decimal_number_config={"num_decimal_places": 0},
        ).move_to(0.25 * DOWN)
        real_dot = Dot(number_line.n2p(100), radius=0.11, color=NP_REAL_COLOR)
        real_label = Text("100", font_size=22, color=NP_REAL_COLOR).next_to(real_dot, UP, buff=0.12)

        pred_tracker = ValueTracker(100)
        pred_dot = always_redraw(lambda: Dot(number_line.n2p(pred_tracker.get_value()), radius=0.11, color=NP_PRED_COLOR))
        error_segment = always_redraw(
            lambda: Line(
                number_line.n2p(100),
                number_line.n2p(pred_tracker.get_value()),
                color=NP_LOSS_COLOR,
                stroke_width=10,
            )
        )
        pred_label = always_redraw(
            lambda: Text(f"previsto = {pred_tracker.get_value():.0f}", font_size=22, color=NP_PRED_COLOR).next_to(
                pred_dot, UP, buff=0.12
            )
        )
        distance_label = always_redraw(
            lambda: Text(f"distancia = {abs(pred_tracker.get_value() - 100):.0f}", font_size=22, color=NP_LOSS_COLOR).next_to(
                error_segment, DOWN, buff=0.18
            )
        )

        mse_formula = MathTex(r"\mathrm{MSE} = (120 - 100)^2 = 400", font_size=36, color=NP_LOSS_COLOR).to_edge(
            DOWN, buff=0.82
        )
        closing = Text(
            "Quanto mais longe o valor previsto estiver do valor real, maior a penalidade.",
            font_size=25,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.35)

        self.play(Write(title))
        self.play(FadeIn(cards, shift=0.12 * UP))
        self.play(Create(number_line))
        self.play(FadeIn(real_dot), FadeIn(real_label, shift=0.1 * UP))
        self.play(FadeIn(pred_dot), Create(error_segment))
        self.play(pred_tracker.animate.set_value(120), run_time=1.4)
        self.play(FadeIn(pred_label, shift=0.1 * UP), FadeIn(distance_label, shift=0.1 * UP))
        self.play(FadeIn(mse_formula, shift=0.12 * UP))
        self.play(FadeIn(closing, shift=0.12 * UP))
        self.wait(1.0)


class Scene5CategoricalLoss(Scene):
    # Cena 5: loss de uma feature categórica via Cross-Entropy.
    def construct(self):
        title = create_title("Loss categorica: Cross-Entropy")

        real_panel = create_panel(
            Text("Supermercado", font_size=32, color=NP_REAL_COLOR),
            title="categoria real",
            color=NP_REAL_COLOR,
            min_width=3.0,
            min_height=1.55,
        ).move_to(4.7 * LEFT + 0.8 * UP)

        good_panel = create_panel(
            create_np_probability_rows(
                ["Supermercado", "Restaurante", "Farmacia"],
                [0.70, 0.20, 0.10],
                correct_index=0,
            ),
            title="previsao do modelo",
            color=NP_PRED_COLOR,
            min_width=5.15,
            min_height=2.45,
        ).move_to(1.45 * RIGHT + 0.65 * UP)
        bad_panel = create_panel(
            create_np_probability_rows(
                ["Supermercado", "Restaurante", "Farmacia"],
                [0.10, 0.80, 0.10],
                correct_index=0,
            ),
            title="previsao do modelo",
            color=NP_PRED_COLOR,
            min_width=5.15,
            min_height=2.45,
        ).move_to(good_panel.get_center())
        pointer = Arrow(
            real_panel.get_right(),
            good_panel.get_left(),
            buff=0.16,
            stroke_width=3,
            color=TEXT_MUTED,
            max_tip_length_to_length_ratio=0.14,
        )

        ce_formula = MathTex(r"\mathrm{CE} = -\log(0.70) \approx 0.36", font_size=34, color=NP_LOSS_COLOR).move_to(
            0.3 * DOWN
        )
        worse_formula = MathTex(r"\mathrm{CE} = -\log(0.10) \approx 2.30", font_size=34, color=NP_LOSS_COLOR).move_to(
            ce_formula.get_center()
        )

        meter_background = RoundedRectangle(
            corner_radius=0.06,
            width=4.8,
            height=0.28,
            stroke_width=0,
            fill_color=GREY_E,
            fill_opacity=0.3,
        ).move_to(0.15 * DOWN + 1.0 * DOWN)
        ce_tracker = ValueTracker(0.36)
        meter_fill = always_redraw(
            lambda: RoundedRectangle(
                corner_radius=0.06,
                width=max(0.12, min(4.8, 4.8 * ce_tracker.get_value() / 2.5)),
                height=0.28,
                stroke_width=0,
                fill_color=NP_LOSS_COLOR,
                fill_opacity=0.92,
            ).move_to(
                meter_background.get_left()
                + RIGHT * (max(0.12, min(4.8, 4.8 * ce_tracker.get_value() / 2.5)) / 2)
            )
        )
        meter_label = always_redraw(
            lambda: Text(f"loss = {ce_tracker.get_value():.2f}", font_size=22, color=NP_LOSS_COLOR).next_to(
                meter_background, DOWN, buff=0.14
            )
        )
        closing = Text(
            "Quanto menor a probabilidade dada para a classe correta, maior a Cross-Entropy.",
            font_size=25,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.35)

        self.play(Write(title))
        self.play(FadeIn(real_panel, scale=0.92))
        self.play(Create(pointer), FadeIn(good_panel, shift=0.15 * RIGHT))
        self.play(FadeIn(ce_formula, shift=0.12 * UP))
        self.play(FadeIn(meter_background), FadeIn(meter_fill), FadeIn(meter_label, shift=0.1 * UP))
        self.play(
            Transform(good_panel, bad_panel),
            Transform(ce_formula, worse_formula),
            ce_tracker.animate.set_value(2.30),
            run_time=1.5,
        )
        self.play(FadeIn(closing, shift=0.12 * UP))
        self.wait(1.0)


class Scene6TotalLoss(Scene):
    # Cena 6: somando as losses de todas as features da transação prevista.
    def construct(self):
        title = create_title("Somando as losses por feature")

        value_loss = create_np_metric_card("valor", "MSE", "400", color=NP_LOSS_COLOR)
        category_loss = create_np_metric_card("categoria", "CE", "0.36", color=NP_LOSS_COLOR)
        country_loss = create_np_metric_card("pais", "CE", "0.22", color=NP_LOSS_COLOR)
        total_loss = create_np_metric_card("loss NP", "loss total", "400.58", color=NP_LOSS_COLOR, width=2.6, height=1.65)

        plus_one = MathTex("+", font_size=42, color=TEXT_MAIN)
        plus_two = MathTex("+", font_size=42, color=TEXT_MAIN)
        equals = MathTex("=", font_size=42, color=TEXT_MAIN)
        row = VGroup(value_loss, plus_one, category_loss, plus_two, country_loss, equals, total_loss).arrange(
            RIGHT, buff=0.18
        )
        row.move_to(1.1 * UP)

        simple_formula = MathTex(
            r"L_t^{NP} = \mathrm{Loss}_{valor} + \mathrm{Loss}_{categoria} + \mathrm{Loss}_{pais}",
            font_size=31,
            color=TEXT_MAIN,
        ).move_to(0.05 * DOWN)
        general_formula = MathTex(
            r"L_t^{NP} = \sum_f l_{\mathrm{rec}}^f\left((\hat{x}_{t+1})_f,\,(x_{t+1})_f\right)",
            font_size=31,
            color=TEXT_MUTED,
        ).to_edge(DOWN, buff=0.82)
        closing = Text(
            "A loss final da transacao e a soma das perdas de todas as features.",
            font_size=26,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.35)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(item, scale=0.92) for item in row], lag_ratio=0.12, run_time=1.5))
        self.play(FadeIn(simple_formula, shift=0.12 * UP))
        self.play(FadeIn(general_formula, shift=0.12 * UP))
        self.play(FadeIn(closing, shift=0.12 * UP))
        self.wait(1.0)


class Scene7FinalIntuition(Scene):
    # Cena 7: ciclo de treino e takeaway sobre o embedding e_t.
    def construct(self):
        title = create_title("Intuicao final do treinamento")

        wrong_pred = create_np_step_card("previsao errada", "o proximo evento foi mal previsto", NP_PRED_COLOR)
        high_loss = create_np_step_card("loss alta", "erro grande gera gradiente", NP_LOSS_COLOR, width=2.5)
        update = create_np_step_card("ajuste dos pesos", "o otimizador atualiza o modelo", NP_MODEL_COLOR, width=2.8)
        better_pred = create_np_step_card("previsao melhor", "mais massa na classe correta", NP_PRED_COLOR, width=2.75)
        cycle = VGroup(wrong_pred, high_loss, update, better_pred).arrange(RIGHT, buff=0.18).move_to(1.95 * UP)

        cycle_arrows = VGroup(
            *[
                create_arrow_between(cycle[index], cycle[index + 1], buff=0.12, color=TEXT_MUTED, stroke_width=3)
                for index in range(len(cycle) - 1)
            ]
        )
        loop_arrow = CurvedArrow(
            better_pred.get_bottom() + 0.08 * DOWN,
            wrong_pred.get_bottom() + 0.08 * DOWN,
            angle=-1.2,
            color=TEXT_MUTED,
            stroke_width=3,
            tip_length=0.18,
        )

        history_panel = create_panel(
            VGroup(
                create_event_box(r"x_{t-2}", width=1.2, color=NP_REAL_COLOR, font_size=26),
                create_event_box(r"x_{t-1}", width=1.2, color=NP_REAL_COLOR, font_size=26),
                create_event_box(r"x_t", width=1.2, color=NP_REAL_COLOR, font_size=26),
            ).arrange(RIGHT, buff=0.16),
            title="comportamento passado",
            color=NP_REAL_COLOR,
            min_width=4.35,
            min_height=1.7,
        ).move_to(3.9 * LEFT + 0.7 * DOWN)
        embedding = create_embedding_vector(tex=r"e_t", width=1.9, height=0.95, color=NP_MODEL_COLOR, font_size=36).move_to(
            0.0 * DOWN
        )
        target_panel = create_panel(
            VGroup(
                create_np_feature_card("proximo valor", "mais proximo do real", color=NP_PRED_COLOR, width=3.1),
                create_np_feature_card("proxima categoria", "mais probabilidade correta", color=NP_PRED_COLOR, width=4.0),
            ).arrange(DOWN, buff=0.16),
            title="melhor previsao",
            color=NP_PRED_COLOR,
            min_width=4.7,
            min_height=2.45,
        ).move_to(4.0 * RIGHT + 0.7 * DOWN)
        history_arrow = create_arrow_between(history_panel, embedding, buff=0.16, color=TEXT_MUTED, stroke_width=3)
        target_arrow = create_arrow_between(embedding, target_panel, buff=0.16, color=TEXT_MUTED, stroke_width=3)

        insight = Text(
            "Para prever a proxima transacao, o modelo precisa entender o comportamento passado da entidade.",
            font_size=24,
            color=TEXT_MAIN,
        ).move_to(0.0 * DOWN + 1.75 * DOWN)
        final_line = Text(
            "A loss forca o embedding e_t a carregar informacao comportamental util.",
            font_size=28,
            color=NP_MODEL_COLOR,
        ).to_edge(DOWN, buff=0.32)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(card, scale=0.92) for card in cycle], lag_ratio=0.14, run_time=1.4))
        self.play(LaggedStart(*[Create(arrow) for arrow in cycle_arrows], lag_ratio=0.12, run_time=0.8))
        self.play(Create(loop_arrow))
        self.play(FadeIn(history_panel, shift=0.15 * UP))
        self.play(FadeIn(embedding, shift=0.12 * UP), Create(history_arrow))
        self.play(Create(target_arrow), FadeIn(target_panel, shift=0.15 * UP))
        self.play(FadeIn(insight, shift=0.12 * UP))
        self.play(FadeIn(final_line, shift=0.12 * UP))
        self.wait(1.0)


class Scene03NPLoss(Scene6TotalLoss):
    # Compatibilidade com o nome antigo: resume a loss total de NP.
    pass


class Scene04PastReconstruction(Scene):
    def construct(self):
        title = create_title("Past Reconstruction")

        timeline = create_timeline(
            [r"x_{t-3}", r"x_{t-2}", r"x_{t-1}", r"x_t"],
            widths=[1.3, 1.3, 1.3, 1.1],
            colors=[ACCENT_BLUE, ACCENT_BLUE, ACCENT_BLUE, ACCENT_YELLOW],
            font_size=27,
        )
        timeline["group"].move_to(2.2 * UP)
        focus = SurroundingRectangle(timeline["boxes"][-1], color=ACCENT_YELLOW, buff=0.08, corner_radius=0.1)

        encoder = create_encoder_block("Encoder", width=2.25, height=1.55).move_to(4.85 * LEFT + 0.25 * DOWN)
        embedding = create_embedding_vector(tex=r"e_t", width=2.0, height=0.9, font_size=32).move_to(2.55 * LEFT + 0.25 * DOWN)
        to_encoder = create_vertical_arrow(
            timeline["boxes"][-1].get_bottom(),
            encoder.get_top(),
            color=TEXT_MUTED,
            buff=0.12,
            stroke_width=3,
        )
        to_embedding = create_arrow_between(encoder, embedding, buff=0.18, color=TEXT_MUTED, stroke_width=3)

        decoder_1 = create_decoder_block(r"D_{PR}", "1 passo\natrás", width=2.2, height=1.55, color=ACCENT_PURPLE)
        decoder_2 = create_decoder_block(r"D_{PR}", "2 passos\natrás", width=2.2, height=1.55, color=ACCENT_PURPLE)
        decoder_3 = create_decoder_block(r"D_{PR}", "3 passos\natrás", width=2.2, height=1.55, color=ACCENT_PURPLE)
        decoders = VGroup(decoder_1, decoder_2, decoder_3).arrange(DOWN, buff=0.3)
        decoders.move_to(1.0 * RIGHT + 0.1 * DOWN)

        recon_1 = create_transaction_box(r"\tilde{x}_{t-1}", "evento reconstruído", width=2.45, accent_color=ACCENT_GREEN, label_font_size=28)
        recon_2 = create_transaction_box(r"\tilde{x}_{t-2}", "evento reconstruído", width=2.45, accent_color=ACCENT_GREEN, label_font_size=28)
        recon_3 = create_transaction_box(r"\tilde{x}_{t-3}", "evento reconstruído", width=2.45, accent_color=ACCENT_GREEN, label_font_size=28)
        recons = VGroup(recon_1, recon_2, recon_3).arrange(DOWN, buff=0.3)
        recons.move_to(4.8 * RIGHT + 0.1 * DOWN)

        delta_1 = create_loss_box(r"\delta_{t,t-1}", "mais recente", width=1.8, height=0.8, color=ACCENT_YELLOW)
        delta_2 = create_loss_box(r"\delta_{t,t-2}", "intermediário", width=1.8, height=0.8, color=ACCENT_YELLOW)
        delta_3 = create_loss_box(r"\delta_{t,t-3}", "mais antigo", width=1.8, height=0.8, color=ACCENT_YELLOW)
        deltas = VGroup(delta_1, delta_2, delta_3)

        formula_one = MathTex(r"D_{PR}: (\mathbb{R}^{d}, \mathbb{R}) \to X", font_size=30, color=TEXT_MUTED)
        formula_two = MathTex(r"\tilde{x}_{t-k} = D_{PR}(e_t, \delta_{t,t-k})", font_size=30, color=TEXT_MUTED)
        formulas = VGroup(formula_one, formula_two).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(3.95 * LEFT + 2.75 * DOWN)
        closing = Text(
            "PR força o embedding a carregar memória do passado.",
            font_size=27,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.38)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(box, scale=0.9) for box in timeline["boxes"]], lag_ratio=0.13, run_time=1.3))
        self.play(LaggedStart(*[Create(arrow) for arrow in timeline["arrows"]], lag_ratio=0.1, run_time=0.8))
        self.play(Create(focus))
        self.play(FadeIn(encoder, scale=0.92), Create(to_encoder))
        self.play(Create(to_embedding), FadeIn(embedding, shift=0.15 * RIGHT))

        for decoder, recon, delta in zip(decoders, recons, deltas):
            edge_arrow = create_arrow_between(embedding, decoder, buff=0.16, color=TEXT_MUTED, stroke_width=3)
            out_arrow = create_arrow_between(decoder, recon, buff=0.16, color=TEXT_MUTED, stroke_width=3)
            delta.next_to(edge_arrow, UP, buff=0.12)
            self.play(
                Create(edge_arrow),
                FadeIn(delta, shift=0.1 * UP),
                FadeIn(decoder, scale=0.92),
                run_time=0.8,
            )
            self.play(Create(out_arrow), FadeIn(recon, shift=0.15 * RIGHT), run_time=0.7)

        self.play(FadeIn(formulas, shift=0.15 * UP))
        self.play(FadeIn(closing, shift=0.15 * UP))
        self.wait(1.0)


class Scene05TemporalWeights(Scene):
    def construct(self):
        title = create_title("Pesos Temporais no PR")

        timeline = create_timeline(
            [r"x_{t-3}", r"x_{t-2}", r"x_{t-1}", r"x_t"],
            widths=[1.3, 1.3, 1.3, 1.1],
            colors=[ACCENT_BLUE, ACCENT_BLUE, ACCENT_BLUE, ACCENT_YELLOW],
            font_size=27,
        )
        timeline["group"].move_to(1.95 * UP)
        focus = SurroundingRectangle(timeline["boxes"][-1], color=ACCENT_YELLOW, buff=0.08, corner_radius=0.1)

        delta_tags = VGroup(
            create_feature_chip(r"\delta_{t,t-3}", "7 dias", width=2.15, color=ACCENT_YELLOW),
            create_feature_chip(r"\delta_{t,t-2}", "1 dia", width=1.95, color=ACCENT_YELLOW),
            create_feature_chip(r"\delta_{t,t-1}", "2 horas", width=2.2, color=ACCENT_YELLOW),
        )
        for tag, box in zip(delta_tags, timeline["boxes"][:-1]):
            tag.next_to(box, DOWN, buff=0.38)

        arrow_old = CurvedArrow(
            timeline["boxes"][0].get_bottom() + 0.05 * DOWN,
            timeline["boxes"][-1].get_bottom() + 0.05 * DOWN,
            angle=-0.45,
            color=ACCENT_BLUE,
            stroke_width=2.5,
            tip_length=0.16,
        ).set_opacity(0.35)
        arrow_mid = CurvedArrow(
            timeline["boxes"][1].get_bottom() + 0.05 * DOWN,
            timeline["boxes"][-1].get_bottom() + 0.05 * DOWN,
            angle=-0.35,
            color=ACCENT_BLUE,
            stroke_width=4.0,
            tip_length=0.16,
        ).set_opacity(0.65)
        arrow_recent = CurvedArrow(
            timeline["boxes"][2].get_bottom() + 0.05 * DOWN,
            timeline["boxes"][-1].get_bottom() + 0.05 * DOWN,
            angle=-0.22,
            color=ACCENT_YELLOW,
            stroke_width=6.0,
            tip_length=0.16,
        )

        weight_old = create_loss_box(r"\omega_{t,t-3}", "baixo peso", width=2.0, height=0.86, color=ACCENT_BLUE)
        weight_mid = create_loss_box(r"\omega_{t,t-2}", "peso médio", width=2.0, height=0.86, color=ACCENT_GREEN)
        weight_recent = create_loss_box(r"\omega_{t,t-1}", "maior peso", width=2.0, height=0.86, color=ACCENT_YELLOW)
        weight_row = VGroup(weight_old, weight_mid, weight_recent).arrange(RIGHT, buff=0.28).move_to(0.3 * DOWN)

        formula = MathTex(r"\omega_{t,t-k} = \exp(-\delta_{t,t-k} / \lambda)", font_size=34, color=TEXT_MUTED).move_to(
            4.15 * RIGHT + 2.55 * DOWN
        )
        closing = Text(
            "Eventos mais distantes ainda importam, mas com menor peso.",
            font_size=27,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.4)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(box, scale=0.9) for box in timeline["boxes"]], lag_ratio=0.12, run_time=1.3))
        self.play(LaggedStart(*[Create(arrow) for arrow in timeline["arrows"]], lag_ratio=0.1, run_time=0.8))
        self.play(Create(focus))
        self.play(LaggedStart(*[FadeIn(tag, shift=0.12 * UP) for tag in delta_tags], lag_ratio=0.15, run_time=1.1))
        self.play(FadeIn(formula, shift=0.15 * UP))
        self.play(Create(arrow_recent), FadeIn(weight_recent, shift=0.12 * UP), run_time=0.8)
        self.play(Create(arrow_mid), FadeIn(weight_mid, shift=0.12 * UP), run_time=0.8)
        self.play(Create(arrow_old), FadeIn(weight_old, shift=0.12 * UP), run_time=0.8)
        self.play(FadeIn(closing, shift=0.15 * UP))
        self.wait(1.0)


class Scene06PRLoss(Scene):
    def construct(self):
        title = create_title("A Loss do Past Reconstruction")

        k_tag = create_loss_box(r"K", "até K eventos", width=1.4, height=0.8, color=ACCENT_YELLOW).to_edge(RIGHT, buff=0.7).shift(
            2.35 * UP
        )

        def make_row(label_tex: str, error_tex: str, weight_tex: str, contrib_tex: str, color):
            recon_tex = label_tex.replace("x_", r"\tilde{x}_", 1)
            real = create_transaction_box(label_tex, "evento passado real", width=2.25, accent_color=color, label_font_size=28)
            recon = create_transaction_box(
                recon_tex,
                "reconstrução",
                width=2.2,
                accent_color=ACCENT_PURPLE,
                label_font_size=26,
            )
            error = create_loss_box(error_tex, "erro", width=1.45, height=0.8, color=ACCENT_RED)
            weight = create_loss_box(weight_tex, "peso ω", width=1.6, height=0.8, color=ACCENT_YELLOW)
            contrib = create_loss_box(contrib_tex, "contribuição", width=1.8, height=0.8, color=ACCENT_GREEN)
            return VGroup(real, recon, error, weight, contrib).arrange(RIGHT, buff=0.22)

        row_1 = make_row("x_{t-1}", "0.30", "0.80", "0.24", ACCENT_GREEN)
        row_2 = make_row("x_{t-2}", "0.45", "0.40", "0.18", ACCENT_BLUE)
        row_3 = make_row("x_{t-3}", "0.60", "0.10", "0.06", ACCENT_BLUE)
        rows = VGroup(row_1, row_2, row_3).arrange(DOWN, buff=0.28).move_to(0.4 * UP)

        plus_one = MathTex("+", font_size=40, color=TEXT_MUTED).next_to(row_1[-1], DOWN, buff=0.08)
        plus_two = MathTex("+", font_size=40, color=TEXT_MUTED).next_to(row_2[-1], DOWN, buff=0.08)
        total = create_loss_box(r"L_t^{PR}", "soma ponderada", width=2.2, height=1.0, color=ACCENT_PURPLE).move_to(
            5.05 * RIGHT + 0.1 * DOWN
        )
        formula = MathTex(
            r"L_t^{PR} = \sum_{k=1}^{\min(K,t)} \omega_{t,t-k} \sum_f l_{\mathrm{rec}}^f((\tilde{x}_{t-k})_f,\,(x_{t-k})_f)",
            font_size=27,
            color=TEXT_MUTED,
        ).to_edge(DOWN, buff=0.75)
        closing = Text(
            "A loss do PR prioriza o passado recente, mas ainda preserva memória de longo prazo.",
            font_size=25,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.35)

        self.play(Write(title), FadeIn(k_tag, shift=0.12 * UP))
        for row in rows:
            self.play(LaggedStart(*[FadeIn(item, scale=0.92) for item in row], lag_ratio=0.12, run_time=0.9))
        self.play(FadeIn(plus_one), FadeIn(plus_two), FadeIn(total, shift=0.15 * LEFT))
        self.play(FadeIn(formula, shift=0.12 * UP))
        self.play(FadeIn(closing, shift=0.12 * UP))
        self.wait(1.0)


class Scene07CombinedLoss(Scene):
    def construct(self):
        title = create_title("Combinando NP e PR")

        np_box = create_loss_box(r"L_t^{NP}", "prever o próximo", width=2.25, height=1.0, color=ACCENT_RED).move_to(
            4.2 * LEFT + 0.55 * UP
        )
        pr_box = create_loss_box(r"L_t^{PR}", "reconstruir o passado", width=2.45, height=1.0, color=ACCENT_PURPLE).move_to(
            4.2 * RIGHT + 0.55 * UP
        )

        slider_line = Line(2.7 * LEFT + 0.85 * DOWN, 2.7 * RIGHT + 0.85 * DOWN, color=TEXT_MUTED, stroke_width=4)
        left_cap = Text("mais NP", font_size=20, color=TEXT_MUTED).next_to(slider_line, LEFT, buff=0.18)
        right_cap = Text("mais PR", font_size=20, color=TEXT_MUTED).next_to(slider_line, RIGHT, buff=0.18)
        knob = Dot(slider_line.point_from_proportion(0.62), radius=0.09, color=ACCENT_YELLOW)
        alpha_label = MathTex(r"\alpha", font_size=34, color=ACCENT_YELLOW).next_to(knob, UP, buff=0.12)

        formula_event = MathTex(
            r"L_t = (1-\alpha)L_t^{NP} + \alpha L_t^{PR}",
            font_size=36,
            color=TEXT_MAIN,
        ).move_to(0.05 * DOWN)
        formula_seq = MathTex(
            r"L_e = \sum_t \left[(1-\alpha)L_t^{NP} + \alpha L_t^{PR}\right]",
            font_size=34,
            color=TEXT_MUTED,
        ).to_edge(DOWN, buff=0.85)
        closing = Text(
            "O modelo aprende com o futuro e com o passado ao mesmo tempo.",
            font_size=27,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.4)

        arrow_np = create_arrow_between(np_box, formula_event, buff=0.18, color=TEXT_MUTED, stroke_width=3)
        arrow_pr = Arrow(
            pr_box.get_left(),
            formula_event.get_right(),
            buff=0.18,
            stroke_width=3,
            color=TEXT_MUTED,
            max_tip_length_to_length_ratio=0.14,
        )

        self.play(Write(title))
        self.play(FadeIn(np_box, scale=0.92), FadeIn(pr_box, scale=0.92))
        self.play(Create(arrow_np), Create(arrow_pr))
        self.play(Write(formula_event))
        self.play(Create(slider_line), FadeIn(left_cap), FadeIn(right_cap), FadeIn(knob), FadeIn(alpha_label))

        knob.generate_target()
        knob.target.move_to(slider_line.point_from_proportion(0.35))
        alpha_label.generate_target()
        alpha_label.target.next_to(knob.target, UP, buff=0.12)
        self.play(MoveToTarget(knob), MoveToTarget(alpha_label), run_time=0.7)

        knob.generate_target()
        knob.target.move_to(slider_line.point_from_proportion(0.62))
        alpha_label.generate_target()
        alpha_label.target.next_to(knob.target, UP, buff=0.12)
        self.play(MoveToTarget(knob), MoveToTarget(alpha_label), run_time=0.7)

        self.play(FadeIn(formula_seq, shift=0.12 * UP))
        self.play(FadeIn(closing, shift=0.12 * UP))
        self.wait(1.0)


class Scene08IntuitionAndTakeaway(Scene):
    def construct(self):
        title = create_title("Intuição Final do NPPR")

        timeline = create_timeline(
            [r"x_{t-2}", r"x_{t-1}", r"x_t", r"x_{t+1}"],
            widths=[1.3, 1.3, 1.1, 1.35],
            colors=[ACCENT_BLUE, ACCENT_BLUE, ACCENT_YELLOW, ACCENT_RED],
            font_size=27,
        )
        timeline["group"].move_to(2.25 * UP)
        focus = SurroundingRectangle(timeline["boxes"][2], color=ACCENT_YELLOW, buff=0.08, corner_radius=0.1)

        encoder = create_encoder_block("Encoder", width=2.2, height=1.55).move_to(2.55 * LEFT + 0.55 * DOWN)
        embedding = create_embedding_vector(tex=r"e_t", width=2.0, height=0.9, font_size=32).move_to(0.15 * DOWN)
        to_encoder = create_vertical_arrow(
            timeline["boxes"][2].get_bottom(),
            encoder.get_top(),
            color=TEXT_MUTED,
            buff=0.12,
            stroke_width=3,
        )
        to_embedding = create_arrow_between(encoder, embedding, buff=0.18, color=TEXT_MUTED, stroke_width=3)

        np_card = create_task_card("prever o próximo", "sinal preditivo", width=2.7, height=1.0, color=ACCENT_RED).move_to(
            4.35 * RIGHT + 0.55 * DOWN
        )
        pr_card = create_task_card("reconstruir o passado", "memória de longo prazo", width=2.95, height=1.0, color=ACCENT_PURPLE).move_to(
            4.55 * LEFT + 2.0 * DOWN
        )
        np_arrow = create_arrow_between(embedding, np_card, buff=0.18, color=TEXT_MUTED, stroke_width=3)
        pr_arrow = Arrow(
            embedding.get_left(),
            pr_card.get_right(),
            buff=0.18,
            stroke_width=3,
            color=TEXT_MUTED,
            max_tip_length_to_length_ratio=0.14,
        )

        summary_card = create_panel(
            VGroup(
                Text("embedding mais informativo", font_size=28, color=ACCENT_YELLOW),
                Text("une previsão e memória", font_size=22, color=TEXT_MAIN),
            ).arrange(DOWN, buff=0.12),
            color=ACCENT_YELLOW,
            min_width=4.5,
            min_height=1.7,
        ).move_to(0.2 * DOWN)

        sentence_one = Text(
            "NP aprende o que vem depois. PR preserva o que veio antes.",
            font_size=27,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.78)
        sentence_two = Text(
            "Resultado: embeddings melhores para tarefas downstream",
            font_size=27,
            color=TITLE_COLOR,
        ).to_edge(DOWN, buff=0.38)

        tasks = VGroup(
            create_task_card("Fraude", "detectar risco", color=ACCENT_RED),
            create_task_card("Churn", "antecipar saída", color=ACCENT_BLUE),
            create_task_card("Crédito", "estimar risco", color=ACCENT_GREEN),
            create_task_card("Gasto futuro", "prever consumo", color=ACCENT_YELLOW),
        ).arrange(RIGHT, buff=0.22).scale(0.88)
        tasks.move_to(0.15 * DOWN + 2.55 * DOWN)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(box, scale=0.9) for box in timeline["boxes"]], lag_ratio=0.12, run_time=1.2))
        self.play(LaggedStart(*[Create(arrow) for arrow in timeline["arrows"]], lag_ratio=0.1, run_time=0.8))
        self.play(Create(focus))
        self.play(FadeIn(encoder, scale=0.92), Create(to_encoder))
        self.play(Create(to_embedding), FadeIn(embedding, shift=0.15 * RIGHT))
        self.play(Create(np_arrow), FadeIn(np_card, shift=0.15 * RIGHT))
        self.play(Create(pr_arrow), FadeIn(pr_card, shift=0.15 * LEFT))

        embedding.generate_target()
        embedding.target.move_to(summary_card.get_center())
        self.play(
            FadeOut(np_arrow),
            FadeOut(pr_arrow),
            FadeOut(np_card),
            FadeOut(pr_card),
            FadeOut(encoder),
            FadeOut(to_embedding),
            FadeOut(to_encoder),
            FadeOut(timeline["group"]),
            FadeOut(focus),
            MoveToTarget(embedding),
            run_time=0.9,
        )
        self.play(ReplacementTransform(embedding, summary_card))
        self.play(FadeIn(sentence_one, shift=0.12 * UP))
        self.play(FadeIn(sentence_two, shift=0.12 * UP))
        self.play(LaggedStart(*[FadeIn(task, scale=0.92) for task in tasks], lag_ratio=0.12, run_time=1.2))
        self.wait(1.1)
