from pathlib import Path

from manim import *


BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Direct all Manim outputs (videos/images/partials) to this theme assets folder.
config.media_dir = str(ASSETS_DIR)

# Keep an explicit 16:9 canvas and a consistent dark theme.
config.pixel_width = 1920
config.pixel_height = 1080
config.background_color = "#0B1020"


"""
Render examples:
  manim -pqh temas/modelos_fundacionais_para_transacoes_financeiras/video/gerador_videos.py Scene01TransactionSequence
  manim -pqh temas/modelos_fundacionais_para_transacoes_financeiras/video/gerador_videos.py Scene04ContextualEncoder
  manim -pqh temas/modelos_fundacionais_para_transacoes_financeiras/video/gerador_videos.py Scene08ClosingSummary
"""


BACKGROUND_FILL = "#151B2F"
SURFACE_FILL = "#11182A"
TEXT_MAIN = GREY_A
TEXT_MUTED = GREY_B
TITLE_COLOR = BLUE_B
ACCENT_BLUE = BLUE_C
ACCENT_GREEN = GREEN_C
ACCENT_YELLOW = YELLOW_C
ACCENT_RED = RED_C


def create_title(text: str) -> Text:
    return Text(text, font_size=38, color=TITLE_COLOR).to_edge(UP, buff=0.35)


def create_label_mobject(label: str, font_size: int = 28, color=WHITE):
    math_tokens = ("\\", "_", "^", "{", "}", "=", r"\cdots", r"\ldots")
    if any(token in label for token in math_tokens):
        return MathTex(label, font_size=font_size, color=color)
    return Text(label, font_size=max(int(font_size * 0.72), 18), color=color)


def create_symbol_box(
    symbol: str,
    width: float = 1.0,
    height: float = 0.82,
    color=ACCENT_BLUE,
    font_size: int = 28,
):
    frame = RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.6,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.95,
    )
    label = create_label_mobject(symbol, font_size=font_size, color=color).move_to(frame.get_center())
    return VGroup(frame, label)


def create_token_box(
    text: str,
    width: float = 1.8,
    height: float = 0.82,
    color=ACCENT_BLUE,
    font_size: int = 22,
):
    frame = RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.6,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.92,
    )
    label = Text(text, font_size=font_size, color=TEXT_MAIN).move_to(frame.get_center())
    return VGroup(frame, label)


def create_transaction_box(
    label: str,
    subtitle: str,
    width: float = 1.8,
    height: float = 1.12,
    accent_color=ACCENT_BLUE,
    label_font_size: int = 28,
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
    label_mob = create_label_mobject(label, font_size=label_font_size, color=accent_color)
    subtitle_mob = Text(subtitle, font_size=subtitle_font_size, color=TEXT_MAIN)
    content = VGroup(label_mob, subtitle_mob).arrange(DOWN, buff=0.08).move_to(frame.get_center())
    return VGroup(frame, content)


def create_timeline(
    transactions,
    width: float = 8.8,
    center=ORIGIN,
    box_width: float = 1.65,
    box_height: float = 1.05,
    box_direction=UP,
    box_buff: float = 0.34,
    accent_color=ACCENT_BLUE,
):
    line = Line(LEFT * width / 2, RIGHT * width / 2, color=TEXT_MUTED, stroke_width=4)
    line.move_to(center)

    dots = VGroup()
    stems = VGroup()
    boxes = VGroup()
    count = len(transactions)

    for index, (label, subtitle) in enumerate(transactions):
        proportion = 0.5 if count == 1 else index / (count - 1)
        point = line.point_from_proportion(proportion)
        dot = Dot(point, radius=0.055, color=accent_color)
        box = create_transaction_box(
            label,
            subtitle,
            width=box_width,
            height=box_height,
            accent_color=accent_color,
        )
        box.next_to(dot, box_direction, buff=box_buff)
        target_edge = box.get_edge_center(DOWN if box_direction is UP else UP)
        stem = Line(dot.get_center(), target_edge, color=TEXT_MUTED, stroke_width=2, stroke_opacity=0.7)
        dots.add(dot)
        boxes.add(box)
        stems.add(stem)

    group = VGroup(line, stems, dots, boxes)
    return {
        "group": group,
        "line": line,
        "stems": stems,
        "dots": dots,
        "boxes": boxes,
    }


def create_sequence_row(
    items,
    widths=None,
    color=ACCENT_BLUE,
    font_size: int = 21,
    height: float = 0.84,
):
    widths = widths or [1.8] * len(items)
    boxes = VGroup(
        *[
            create_token_box(item, width=widths[index], height=height, color=color, font_size=font_size)
            for index, item in enumerate(items)
        ]
    )
    boxes.arrange(RIGHT, buff=0.55)
    arrows = VGroup(
        *[
            create_arrow_between(boxes[index], boxes[index + 1], buff=0.08, color=TEXT_MUTED, stroke_width=3)
            for index in range(len(boxes) - 1)
        ]
    )
    return {"group": VGroup(boxes, arrows), "boxes": boxes, "arrows": arrows}


def create_encoder_block(label: str = "Encoder E", width: float = 2.7, height: float = 1.9):
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
                width=0.34,
                height=0.95,
                stroke_width=0,
                fill_color=ACCENT_GREEN,
                fill_opacity=opacity,
            )
            for opacity in (0.35, 0.55, 0.8)
        ]
    ).arrange(RIGHT, buff=0.14)
    bars.move_to(frame.get_center()).shift(0.28 * UP)
    text = Text(label, font_size=24, color=TEXT_MAIN).next_to(bars, DOWN, buff=0.18)
    return VGroup(frame, bars, text)


def create_embedding_vector(
    tex: str = r"e_t = [0.12,\,-0.45,\,0.88,\,\ldots,\,0.31]",
    width: float = 4.5,
    height: float = 1.3,
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


def create_arrow_between(source, target, buff: float = 0.16, color=TEXT_MAIN, stroke_width: float = 4):
    return Arrow(
        source.get_right(),
        target.get_left(),
        buff=buff,
        stroke_width=stroke_width,
        color=color,
        max_tip_length_to_length_ratio=0.14,
    )


def create_task_card(
    title: str,
    subtitle: str,
    width: float = 3.25,
    height: float = 1.08,
    color=ACCENT_BLUE,
):
    frame = RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.6,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.96,
    )
    title_mob = Text(title, font_size=23, color=color)
    subtitle_mob = Text(subtitle, font_size=17, color=TEXT_MAIN)
    content = VGroup(title_mob, subtitle_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    content.move_to(frame.get_center()).align_to(frame.get_left() + 0.24 * RIGHT, LEFT)
    return VGroup(frame, content)


def create_customer_icon():
    head = Circle(radius=0.3, stroke_color=ACCENT_BLUE, stroke_width=3, fill_color=ACCENT_BLUE, fill_opacity=0.16)
    body = RoundedRectangle(
        corner_radius=0.18,
        width=0.95,
        height=1.15,
        stroke_color=ACCENT_BLUE,
        stroke_width=3,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.95,
    )
    head.next_to(body, UP, buff=0.08)

    card = RoundedRectangle(
        corner_radius=0.1,
        width=1.15,
        height=0.68,
        stroke_color=ACCENT_YELLOW,
        stroke_width=2.6,
        fill_color=SURFACE_FILL,
        fill_opacity=1.0,
    ).shift(0.56 * DOWN + 0.78 * RIGHT)
    chip = RoundedRectangle(
        corner_radius=0.03,
        width=0.22,
        height=0.16,
        stroke_width=0,
        fill_color=ACCENT_YELLOW,
        fill_opacity=1.0,
    ).move_to(card.get_center() + 0.25 * LEFT)
    stripe = Line(card.get_left() + 0.14 * RIGHT, card.get_right() + 0.14 * LEFT, color=ACCENT_YELLOW, stroke_width=2)
    stripe.shift(0.12 * DOWN)

    label = Text("Cliente / Cartão", font_size=22, color=TEXT_MAIN)
    icon = VGroup(head, body, card, chip, stripe)
    label.next_to(icon, DOWN, buff=0.25)
    return VGroup(icon, label)


class Scene01TransactionSequence(Scene):
    def construct(self):
        title = create_title("Transações como Sequências")
        customer = create_customer_icon().scale(0.92).to_edge(LEFT, buff=0.7).shift(0.2 * DOWN)

        transactions = [
            (r"x_0", "Mercado — R$80"),
            (r"x_1", "Posto — R$150"),
            (r"x_2", "Restaurante — R$65"),
            (r"x_3", "Transporte — R$24"),
            (r"x_t", "Hotel — R$420"),
        ]
        timeline = create_timeline(
            transactions,
            width=8.8,
            center=1.2 * RIGHT + 0.05 * DOWN,
            box_width=1.65,
            box_height=1.02,
        )
        formula = MathTex("h_i", "=", r"\{x_t\}_{t=0}^{T_i}", font_size=64, color=TEXT_MUTED).next_to(
            timeline["line"], DOWN, buff=0.95
        )
        formula[0].set_color(ACCENT_YELLOW)

        history_note = Text(
            "h_i = sequência de transações\nfinanceiras da pessoa i",
            font_size=24,
            color=ACCENT_GREEN,
        ).move_to(4.55 * LEFT + 2.15 * DOWN)
        history_arrow = CurvedArrow(
            history_note.get_right() + 0.05 * RIGHT,
            formula[0].get_left() + 0.04 * LEFT,
            angle=0.25,
            color=ACCENT_GREEN,
            stroke_width=3,
            tip_length=0.18,
        )
        closing = Text(
            "Um histórico financeiro é uma sequência temporal de eventos.",
            font_size=28,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.45)

        self.play(Write(title))
        self.play(FadeIn(customer, shift=0.3 * RIGHT))
        self.play(Create(timeline["line"]), FadeIn(formula, shift=0.15 * DOWN))
        self.play(
            Create(history_arrow),
            FadeIn(history_note, shift=0.15 * RIGHT),
            Indicate(formula[0], color=ACCENT_YELLOW),
        )

        for stem, dot, box in zip(timeline["stems"], timeline["dots"], timeline["boxes"]):
            self.play(
                LaggedStart(
                    Create(stem),
                    FadeIn(dot, scale=0.7),
                    FadeIn(box, shift=0.16 * UP),
                    lag_ratio=0.18,
                ),
                run_time=0.75,
            )

        self.play(FadeIn(closing, shift=0.18 * UP))
        self.wait(1.0)


class Scene02TransactionFeatures(Scene):
    def construct(self):
        title = create_title("Cada Transação é um Evento Multivariado")
        transaction = create_transaction_box(
            r"x_t",
            "Hotel — R$420",
            width=3.15,
            height=1.45,
            accent_color=ACCENT_YELLOW,
            label_font_size=34,
            subtitle_font_size=24,
        ).move_to(0.5 * UP)

        card_frame = RoundedRectangle(
            corner_radius=0.24,
            width=7.0,
            height=4.5,
            stroke_color=ACCENT_YELLOW,
            stroke_width=3,
            fill_color=SURFACE_FILL,
            fill_opacity=0.98,
        ).move_to(0.15 * UP)
        card_header = VGroup(
            create_label_mobject(r"x_t", font_size=34, color=ACCENT_YELLOW),
            Text("Hotel — R$420", font_size=24, color=TEXT_MAIN),
        ).arrange(DOWN, buff=0.08).move_to(card_frame.get_top() + 0.65 * DOWN)
        card_group = VGroup(card_frame, card_header)

        feature_boxes = [
            create_transaction_box("Valor", "R$420", width=2.55, height=0.95, accent_color=ACCENT_BLUE, label_font_size=26),
            create_transaction_box("Categoria", "Hotel", width=2.55, height=0.95, accent_color=ACCENT_BLUE, label_font_size=24),
            create_transaction_box("Horário", "22:15", width=2.55, height=0.95, accent_color=ACCENT_GREEN, label_font_size=24),
            create_transaction_box("Local", "São Paulo", width=2.55, height=0.95, accent_color=ACCENT_GREEN, label_font_size=24),
            create_transaction_box("Tipo", "Crédito", width=2.55, height=0.95, accent_color=ACCENT_RED, label_font_size=24),
        ]

        row_one = VGroup(feature_boxes[0], feature_boxes[1]).arrange(RIGHT, buff=0.24)
        row_two = VGroup(feature_boxes[2], feature_boxes[3]).arrange(RIGHT, buff=0.24)
        row_three = VGroup(feature_boxes[4]).arrange(RIGHT)
        features = VGroup(row_one, row_two, row_three).arrange(DOWN, buff=0.24).move_to(card_frame.get_center() + 0.35 * DOWN)

        set_formula = MathTex(r"x_t \in X", font_size=34, color=TEXT_MUTED).to_edge(DOWN, buff=0.95)
        closing = Text(
            "Cada evento combina variáveis numéricas e categóricas.",
            font_size=28,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.4)

        self.play(Write(title))
        self.play(FadeIn(transaction, scale=0.92))
        self.wait(0.3)
        self.play(ReplacementTransform(transaction, card_group), run_time=1.0)
        self.play(
            LaggedStart(*[FadeIn(feature, scale=0.88) for feature in feature_boxes], lag_ratio=0.14, run_time=1.8)
        )
        self.play(FadeIn(set_formula, shift=0.15 * UP))
        self.play(FadeIn(closing, shift=0.15 * UP))
        self.wait(1.0)


class Scene03TemporalOrderMatters(Scene):
    def construct(self):
        title = create_title("A Ordem das Transações Importa")
        order_tag = create_token_box("ordem", width=1.45, color=ACCENT_YELLOW, font_size=24).to_edge(RIGHT, buff=0.8).shift(
            2.4 * UP
        )
        time_tag = create_token_box("tempo", width=1.45, color=ACCENT_GREEN, font_size=24).next_to(order_tag, DOWN, buff=0.18)

        sequence = create_sequence_row(
            ["Mercado", "Posto", "Restaurante", "Transporte", "Hotel"],
            widths=[1.8, 1.5, 2.1, 2.0, 1.55],
            font_size=20,
        )
        sequence["group"].move_to(0.45 * UP)

        tracker = Dot(color=ACCENT_YELLOW, radius=0.08).move_to(sequence["boxes"][0].get_bottom() + 0.42 * DOWN)
        pattern_text = Text("rotina", font_size=28, color=ACCENT_GREEN).to_edge(DOWN, buff=0.95)
        expanded_pattern = Text(
            "rotina + deslocamento + alimentação + viagem",
            font_size=28,
            color=ACCENT_GREEN,
        ).move_to(pattern_text)
        closing = Text(
            "A ordem das transações carrega comportamento.",
            font_size=28,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.42)

        self.play(Write(title))
        self.play(FadeIn(order_tag, shift=0.2 * LEFT), FadeIn(time_tag, shift=0.2 * LEFT))
        self.play(LaggedStart(*[FadeIn(box, scale=0.9) for box in sequence["boxes"]], lag_ratio=0.12, run_time=1.6))
        self.play(LaggedStart(*[Create(arrow) for arrow in sequence["arrows"]], lag_ratio=0.1, run_time=1.0))
        self.play(FadeIn(tracker, scale=0.7))

        for box in sequence["boxes"][1:]:
            self.play(tracker.animate.move_to(box.get_bottom() + 0.42 * DOWN), run_time=0.4)

        self.play(FadeIn(pattern_text, shift=0.15 * UP))
        self.play(Transform(pattern_text, expanded_pattern), run_time=1.0)
        self.play(FadeOut(tracker, scale=0.7), FadeIn(closing, shift=0.16 * UP))
        self.wait(1.0)


class Scene04ContextualEncoder(Scene):
    def construct(self):
        title = create_title("Encoder Contextual")
        sequence_boxes = VGroup(
            create_symbol_box(r"x_0", width=0.95),
            create_symbol_box(r"x_1", width=0.95),
            create_symbol_box(r"x_2", width=0.95),
            create_symbol_box(r"\cdots", width=1.0, color=TEXT_MUTED),
            create_symbol_box(r"x_t", width=0.95, color=ACCENT_YELLOW),
        ).arrange(RIGHT, buff=0.16)
        left_bracket = MathTex("[", font_size=60, color=TEXT_MAIN).next_to(sequence_boxes, LEFT, buff=0.12)
        right_bracket = MathTex("]", font_size=60, color=TEXT_MAIN).next_to(sequence_boxes, RIGHT, buff=0.12)
        sequence_group = VGroup(left_bracket, sequence_boxes, right_bracket).move_to(4.05 * LEFT + 0.2 * UP)

        encoder = create_encoder_block().move_to(ORIGIN + 0.15 * UP)
        embedding = create_embedding_vector().move_to(4.1 * RIGHT + 0.15 * UP)
        input_arrow = create_arrow_between(sequence_group, encoder, buff=0.18, color=TEXT_MUTED)
        output_arrow = create_arrow_between(encoder, embedding, buff=0.18, color=TEXT_MUTED)
        mapping = MathTex(r"E: X^{*} \to \mathbb{R}^{d}", font_size=34, color=TEXT_MUTED).next_to(encoder, DOWN, buff=0.6)
        closing = Text("Evento + contexto → embedding", font_size=28, color=TEXT_MAIN).to_edge(DOWN, buff=0.45)

        self.play(Write(title))
        self.play(FadeIn(sequence_group, shift=0.2 * RIGHT))
        self.play(FadeIn(encoder, scale=0.92), FadeIn(mapping, shift=0.16 * UP))
        self.play(Create(input_arrow))

        sequence_copy = sequence_group.copy()
        self.add(sequence_copy)
        sequence_copy.generate_target()
        sequence_copy.target.scale(0.45).move_to(encoder.get_center())
        sequence_copy.target.set_opacity(0.28)
        self.play(MoveToTarget(sequence_copy), run_time=1.0)
        self.play(FadeOut(sequence_copy, scale=0.85))

        self.play(Create(output_arrow), FadeIn(embedding, shift=0.22 * RIGHT))
        self.play(FadeIn(closing, shift=0.15 * UP))
        self.wait(1.0)


class Scene05FormulaMeaning(Scene):
    def construct(self):
        title = create_title("O Que a Fórmula Diz")
        formula = MathTex(
            "e_t",
            "=",
            "E",
            "(",
            "x_t",
            ",",
            "x_{t-1}",
            ",",
            r"\ldots",
            ",",
            "x_0",
            ")",
            font_size=42,
            color=TEXT_MAIN,
        ).move_to(2.35 * UP)

        current_highlight = SurroundingRectangle(formula[4], color=ACCENT_YELLOW, buff=0.09, corner_radius=0.1)
        history_group = VGroup(formula[6], formula[7], formula[8], formula[9], formula[10])
        history_highlight = SurroundingRectangle(history_group, color=ACCENT_GREEN, buff=0.09, corner_radius=0.1)

        isolated_panel = RoundedRectangle(
            corner_radius=0.2,
            width=4.0,
            height=2.7,
            stroke_color=ACCENT_RED,
            stroke_width=2.6,
            fill_color=SURFACE_FILL,
            fill_opacity=0.97,
        ).move_to(3.6 * LEFT + 0.45 * DOWN)
        isolated_title = Text("Compra isolada", font_size=25, color=ACCENT_RED).next_to(isolated_panel.get_top(), DOWN, buff=0.2)
        isolated_tx = create_transaction_box(
            r"x_t",
            "Hotel — R$420",
            width=2.5,
            height=1.1,
            accent_color=ACCENT_YELLOW,
            label_font_size=30,
        ).move_to(isolated_panel.get_center() + 0.2 * UP)
        isolated_caption = Text("pouco contexto", font_size=22, color=TEXT_MUTED).next_to(isolated_tx, DOWN, buff=0.18)
        isolated_group = VGroup(isolated_panel, isolated_title, isolated_tx, isolated_caption)

        context_panel = RoundedRectangle(
            corner_radius=0.2,
            width=5.2,
            height=2.7,
            stroke_color=ACCENT_GREEN,
            stroke_width=2.6,
            fill_color=SURFACE_FILL,
            fill_opacity=0.97,
        ).move_to(3.3 * RIGHT + 0.45 * DOWN)
        context_title = Text("Compra com contexto", font_size=25, color=ACCENT_GREEN).next_to(context_panel.get_top(), DOWN, buff=0.2)
        context_sequence = VGroup(
            create_symbol_box(r"x_{t-2}", width=1.1, color=ACCENT_BLUE),
            create_symbol_box(r"x_{t-1}", width=1.1, color=ACCENT_BLUE),
            create_symbol_box(r"x_t", width=1.0, color=ACCENT_YELLOW),
        ).arrange(RIGHT, buff=0.12).move_to(context_panel.get_center() + 0.35 * UP)
        context_arrow = Arrow(
            context_sequence.get_bottom() + 0.05 * DOWN,
            context_panel.get_center() + 0.1 * DOWN,
            buff=0.12,
            stroke_width=3,
            color=TEXT_MUTED,
            max_tip_length_to_length_ratio=0.16,
        )
        rich_embedding = create_embedding_vector(
            tex=r"e_t = [\ldots]",
            width=2.7,
            height=0.95,
            color=ACCENT_GREEN,
            font_size=24,
        ).move_to(context_panel.get_center() + 0.7 * DOWN)
        context_caption = Text("sinal mais informativo", font_size=22, color=TEXT_MUTED).next_to(rich_embedding, DOWN, buff=0.15)
        context_group = VGroup(context_panel, context_title, context_sequence, context_arrow, rich_embedding, context_caption)

        closing = Text(
            "O significado de x_t depende do que veio antes.",
            font_size=29,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.42)

        self.play(Write(title))
        self.play(Write(formula))
        self.play(Create(current_highlight))
        self.play(Create(history_highlight))
        self.play(FadeIn(isolated_group, shift=0.18 * UP))
        self.play(FadeIn(context_group, shift=0.18 * UP))
        self.play(FadeIn(closing, shift=0.15 * UP))
        self.wait(1.0)


class Scene06SameTransactionDifferentContext(Scene):
    def construct(self):
        title = create_title("Mesma Compra, Contextos Diferentes")

        top_label = Text("Cliente A", font_size=26, color=ACCENT_BLUE).move_to(6.0 * LEFT + 1.85 * UP)
        top_sequence = create_sequence_row(
            ["Passagem\naérea", "Uber", "Restaurante", "Hotel\nR$420"],
            widths=[1.95, 1.35, 1.95, 1.7],
            font_size=18,
        )
        top_sequence["group"].move_to(1.65 * LEFT + 1.55 * UP)
        top_focus = SurroundingRectangle(top_sequence["boxes"][-1], color=ACCENT_YELLOW, buff=0.08, corner_radius=0.1)
        top_encoder = create_encoder_block("Encoder E", width=2.05, height=1.45).move_to(4.85 * RIGHT + 1.55 * UP)
        top_arrow = create_arrow_between(top_sequence["boxes"][-1], top_encoder, buff=0.12, color=TEXT_MUTED, stroke_width=3)
        top_embedding = create_embedding_vector(
            tex=r"e_t^A = [0.72,\,0.10,\,\ldots,\,-0.14]",
            width=4.0,
            height=1.0,
            color=ACCENT_GREEN,
            font_size=22,
        ).move_to(4.7 * RIGHT + 0.55 * UP)

        bottom_label = Text("Cliente B", font_size=26, color=ACCENT_BLUE).move_to(6.0 * LEFT + 1.15 * DOWN)
        bottom_sequence = create_sequence_row(
            ["Mercado", "Farmácia", "Padaria", "Hotel\nR$420"],
            widths=[1.65, 1.7, 1.65, 1.7],
            font_size=18,
        )
        bottom_sequence["group"].move_to(1.65 * LEFT + 1.45 * DOWN)
        bottom_focus = SurroundingRectangle(bottom_sequence["boxes"][-1], color=ACCENT_YELLOW, buff=0.08, corner_radius=0.1)
        bottom_encoder = create_encoder_block("Encoder E", width=2.05, height=1.45).move_to(4.85 * RIGHT + 1.45 * DOWN)
        bottom_arrow = create_arrow_between(bottom_sequence["boxes"][-1], bottom_encoder, buff=0.12, color=TEXT_MUTED, stroke_width=3)
        bottom_embedding = create_embedding_vector(
            tex=r"e_t^B = [-0.08,\,0.61,\,\ldots,\,0.44]",
            width=4.0,
            height=1.0,
            color=ACCENT_RED,
            font_size=22,
        ).move_to(4.7 * RIGHT + 2.45 * DOWN)

        inequality = MathTex(r"e_t^A \neq e_t^B", font_size=38, color=ACCENT_YELLOW).move_to(4.65 * RIGHT + 0.45 * DOWN)
        closing = Text(
            "A mesma compra pode ter significados diferentes.",
            font_size=28,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.35)

        self.play(Write(title))
        self.play(FadeIn(top_label, shift=0.2 * RIGHT))
        self.play(LaggedStart(*[FadeIn(box, scale=0.9) for box in top_sequence["boxes"]], lag_ratio=0.12, run_time=1.2))
        self.play(LaggedStart(*[Create(arrow) for arrow in top_sequence["arrows"]], lag_ratio=0.1, run_time=0.8))

        self.play(FadeIn(bottom_label, shift=0.2 * RIGHT))
        self.play(LaggedStart(*[FadeIn(box, scale=0.9) for box in bottom_sequence["boxes"]], lag_ratio=0.12, run_time=1.2))
        self.play(LaggedStart(*[Create(arrow) for arrow in bottom_sequence["arrows"]], lag_ratio=0.1, run_time=0.8))

        self.play(Create(top_focus), Create(bottom_focus))
        self.play(FadeIn(top_encoder, scale=0.92), FadeIn(bottom_encoder, scale=0.92))

        top_copy = top_sequence["boxes"].copy()
        bottom_copy = bottom_sequence["boxes"].copy()
        self.add(top_copy, bottom_copy)

        top_copy.generate_target()
        top_copy.target.scale(0.28).move_to(top_encoder.get_center()).set_opacity(0.25)
        bottom_copy.generate_target()
        bottom_copy.target.scale(0.28).move_to(bottom_encoder.get_center()).set_opacity(0.25)

        self.play(
            Create(top_arrow),
            Create(bottom_arrow),
            MoveToTarget(top_copy),
            MoveToTarget(bottom_copy),
            run_time=1.1,
        )
        self.play(
            FadeOut(top_copy, scale=0.8),
            FadeOut(bottom_copy, scale=0.8),
            FadeIn(top_embedding, shift=0.2 * RIGHT),
            FadeIn(bottom_embedding, shift=0.2 * RIGHT),
        )
        self.play(Write(inequality), FadeIn(closing, shift=0.15 * UP))
        self.wait(1.0)


class Scene07DownstreamTasks(Scene):
    def construct(self):
        title = create_title("Embeddings em Tarefas Reais")

        history_label = Text("Histórico de Transações", font_size=26, color=TEXT_MAIN).move_to(4.45 * LEFT + 2.1 * UP)
        history = create_sequence_row(
            ["Mercado", "Posto", "Hotel"],
            widths=[1.65, 1.45, 1.5],
            font_size=20,
        )
        history["group"].move_to(4.35 * LEFT + 0.7 * UP)

        encoder = create_encoder_block("Encoder E", width=2.35, height=1.65).move_to(0.95 * LEFT + 0.7 * UP)
        to_encoder = create_arrow_between(history["boxes"][-1], encoder, buff=0.15, color=TEXT_MUTED)

        embedding = create_embedding_vector(
            tex=r"e = [0.18,\,-0.22,\,\ldots,\,0.67]",
            width=3.8,
            height=1.05,
            color=ACCENT_YELLOW,
            font_size=24,
        ).move_to(2.75 * RIGHT + 0.7 * UP)
        to_embedding = create_arrow_between(encoder, embedding, buff=0.18, color=TEXT_MUTED)

        tasks = VGroup(
            create_task_card("Fraude", "detectar padrão atípico", color=ACCENT_RED),
            create_task_card("Churn", "antecipar risco de saída", color=ACCENT_BLUE),
            create_task_card("Crédito", "estimar risco e limite", color=ACCENT_GREEN),
            create_task_card("Gasto Futuro", "prever consumo", color=ACCENT_YELLOW),
        ).arrange(DOWN, buff=0.24)
        tasks.move_to(3.45 * RIGHT + 0.2 * DOWN)

        tasks_label = Text("Como o embedding é usado", font_size=26, color=TEXT_MAIN).next_to(tasks, UP, buff=0.35)
        embedding_label = Text("Embedding contextual", font_size=24, color=ACCENT_YELLOW)
        downstream_hint = Text("o vetor vira entrada para outros modelos", font_size=22, color=TEXT_MUTED)

        closing = Text(
            "Embeddings contextuais transformam comportamento financeiro em sinais úteis para modelos.",
            font_size=26,
            color=TEXT_MAIN,
        ).to_edge(DOWN, buff=0.38)

        self.play(Write(title))
        self.play(FadeIn(history_label, shift=0.15 * UP))
        self.play(LaggedStart(*[FadeIn(box, scale=0.9) for box in history["boxes"]], lag_ratio=0.12, run_time=1.0))
        self.play(LaggedStart(*[Create(arrow) for arrow in history["arrows"]], lag_ratio=0.1, run_time=0.7))
        self.play(FadeIn(encoder, scale=0.92), Create(to_encoder))
        self.play(Create(to_embedding), FadeIn(embedding, shift=0.18 * RIGHT))

        pipeline_group = VGroup(history_label, history["group"], encoder, to_encoder, to_embedding)
        self.play(
            FadeOut(pipeline_group, shift=0.15 * UP),
            embedding.animate.move_to(3.2 * LEFT + 0.2 * DOWN),
            run_time=0.9,
        )

        embedding_label.next_to(embedding, UP, buff=0.28)
        downstream_hint.next_to(embedding, DOWN, buff=0.25)
        task_arrows = VGroup(
            *[
                Arrow(
                    embedding.get_right(),
                    task.get_left(),
                    buff=0.14,
                    stroke_width=3,
                    color=TEXT_MUTED,
                    max_tip_length_to_length_ratio=0.14,
                )
                for task in tasks
            ]
        )

        self.play(FadeIn(embedding_label, shift=0.12 * UP), FadeIn(downstream_hint, shift=0.12 * UP))
        self.play(FadeIn(tasks_label, shift=0.15 * UP))

        for arrow, task in zip(task_arrows, tasks):
            self.play(
                Create(arrow),
                FadeIn(task, shift=0.14 * RIGHT),
                run_time=0.6,
            )

        self.play(FadeIn(closing, shift=0.15 * UP))
        self.wait(1.0)
