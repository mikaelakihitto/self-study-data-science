from pathlib import Path
import sys

from manim import *

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from temas.utils.manim_utils import (
    ACCENT_BLUE,
    ACCENT_CYAN,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    ACCENT_RED,
    ACCENT_YELLOW,
    PANEL_FILL,
    SURFACE_ALT,
    SURFACE_FILL,
    TEXT_MAIN,
    TEXT_MUTED,
    configure_default_video_output,
    create_arrow_between,
    create_box,
    create_chip,
    create_title,
    create_vertical_arrow_between,
)


BASE_DIR, ASSETS_DIR = configure_default_video_output(__file__)


"""
Render examples:
  ./.venv/bin/manim -pqh temas/intro_como_bancos_ganham_dinheiro/video/gerador_videos_intro_bancos.py Scene01Hook
  ./.venv/bin/manim -pqh temas/intro_como_bancos_ganham_dinheiro/video/gerador_videos_intro_bancos.py Scene06ChaosWithoutIntermediary
  ./.venv/bin/manim -pqh temas/intro_como_bancos_ganham_dinheiro/video/gerador_videos_intro_bancos.py Scene12NextVideoHook
"""


BACKGROUND_FILL = PANEL_FILL


def create_person(label: str, color=ACCENT_BLUE, scale_factor: float = 1.0):
    head = Circle(radius=0.28, stroke_width=3, stroke_color=color, fill_color=color, fill_opacity=0.16)
    body = RoundedRectangle(
        corner_radius=0.18,
        width=1.05,
        height=1.35,
        stroke_color=color,
        stroke_width=3,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.92,
    )
    body.next_to(head, DOWN, buff=0.08)
    text = Text(label, font_size=22, color=TEXT_MAIN).next_to(body, DOWN, buff=0.16)
    person = VGroup(head, body, text)
    person.scale(scale_factor)
    return person


def create_bank(color=ACCENT_YELLOW, width: float = 2.8, height: float = 2.2):
    roof = Polygon(
        LEFT * 1.4 + UP * 0.6,
        RIGHT * 1.4 + UP * 0.6,
        UP * 1.35,
        stroke_color=color,
        stroke_width=3,
        fill_color=color,
        fill_opacity=0.14,
    )
    base = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height * 0.7,
        stroke_color=color,
        stroke_width=3,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.95,
    ).shift(DOWN * 0.28)
    columns = VGroup(
        *[
            RoundedRectangle(
                corner_radius=0.06,
                width=0.28,
                height=1.0,
                stroke_color=color,
                stroke_width=2.4,
                fill_color=color,
                fill_opacity=0.16,
            )
            for _ in range(4)
        ]
    ).arrange(RIGHT, buff=0.28)
    columns.move_to(base.get_center() + DOWN * 0.06)
    label = Text("BANCO", font_size=28, color=color).move_to(base.get_center() + UP * 0.63)
    return VGroup(roof, base, columns, label)


def create_card_icon(title: str, color=ACCENT_BLUE, width: float = 2.2, height: float = 1.35):
    card = RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2.8,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.96,
    )
    stripe = RoundedRectangle(
        corner_radius=0.02,
        width=width * 0.76,
        height=0.12,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.65,
    ).move_to(card.get_top() + DOWN * 0.28)
    chip = RoundedRectangle(
        corner_radius=0.05,
        width=0.35,
        height=0.25,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.18,
    ).move_to(card.get_left() + RIGHT * 0.45 + DOWN * 0.05)
    label = Text(title, font_size=20, color=TEXT_MAIN).move_to(card.get_bottom() + UP * 0.28)
    return VGroup(card, stripe, chip, label)


def create_phone_icon(label: str = "app", color=ACCENT_CYAN):
    frame = RoundedRectangle(
        corner_radius=0.22,
        width=1.2,
        height=2.05,
        stroke_color=color,
        stroke_width=2.8,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.96,
    )
    screen = RoundedRectangle(
        corner_radius=0.14,
        width=0.92,
        height=1.45,
        stroke_width=0,
        fill_color=SURFACE_ALT,
        fill_opacity=1.0,
    ).move_to(frame.get_center() + UP * 0.05)
    dots = VGroup(
        *[
            Circle(radius=0.07, stroke_width=0, fill_color=color, fill_opacity=opacity)
            for opacity in (0.45, 0.75, 1.0)
        ]
    ).arrange(DOWN, buff=0.12).move_to(screen.get_center())
    text = Text(label, font_size=18, color=TEXT_MAIN).move_to(frame.get_bottom() + UP * 0.2)
    return VGroup(frame, screen, dots, text)


def create_coin_stack(label: str, color=ACCENT_GREEN, levels: int = 3):
    coins = VGroup()
    for index in range(levels):
        ellipse = Ellipse(
            width=1.15,
            height=0.22,
            stroke_color=color,
            stroke_width=2.4,
            fill_color=color,
            fill_opacity=0.14 + 0.06 * index,
        ).shift(UP * 0.18 * index)
        coins.add(ellipse)
    tag = Text(label, font_size=20, color=TEXT_MAIN).next_to(coins, DOWN, buff=0.14)
    return VGroup(coins, tag)


def create_metric_card(title: str, value: str, color=ACCENT_BLUE, width: float = 2.5):
    frame = RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=1.1,
        stroke_color=color,
        stroke_width=2.6,
        fill_color=BACKGROUND_FILL,
        fill_opacity=0.96,
    )
    title_text = Text(title, font_size=18, color=TEXT_MUTED)
    value_text = Text(value, font_size=24, color=color)
    content = VGroup(title_text, value_text).arrange(DOWN, buff=0.06).move_to(frame.get_center())
    return VGroup(frame, content)


def create_feature_row(items):
    chips = VGroup(*[create_chip(label, color) for label, color in items])
    chips.arrange(RIGHT, buff=0.28)
    return chips


def create_scale():
    stand = Line(DOWN * 1.4, ORIGIN, stroke_width=6, color=TEXT_MUTED)
    base = Line(LEFT * 1.0 + DOWN * 1.4, RIGHT * 1.0 + DOWN * 1.4, stroke_width=6, color=TEXT_MUTED)
    beam = Line(LEFT * 2.4, RIGHT * 2.4, stroke_width=6, color=ACCENT_YELLOW)
    left_chain = Line(beam.get_start(), LEFT * 2.4 + DOWN * 1.0, stroke_width=3, color=TEXT_MUTED)
    right_chain = Line(beam.get_end(), RIGHT * 2.4 + DOWN * 1.0, stroke_width=3, color=TEXT_MUTED)
    left_plate = RoundedRectangle(
        corner_radius=0.12,
        width=1.9,
        height=0.34,
        stroke_color=ACCENT_BLUE,
        stroke_width=2.6,
        fill_color=SURFACE_FILL,
        fill_opacity=0.96,
    ).move_to(LEFT * 2.4 + DOWN * 1.24)
    right_plate = RoundedRectangle(
        corner_radius=0.12,
        width=1.9,
        height=0.34,
        stroke_color=ACCENT_RED,
        stroke_width=2.6,
        fill_color=SURFACE_FILL,
        fill_opacity=0.96,
    ).move_to(RIGHT * 2.4 + DOWN * 1.24)
    pivot = Triangle(stroke_color=ACCENT_YELLOW, stroke_width=0, fill_color=ACCENT_YELLOW, fill_opacity=0.8).scale(0.22)
    pivot.rotate(PI).move_to(ORIGIN + DOWN * 0.18)
    return VGroup(base, stand, beam, left_chain, right_chain, left_plate, right_plate, pivot)


def create_revenue_icon(title: str, accent, symbol: str):
    ring = Circle(radius=0.5, stroke_color=accent, stroke_width=2.8, fill_color=accent, fill_opacity=0.14)
    mark = Text(symbol, font_size=28, color=accent).move_to(ring.get_center())
    label = Text(title, font_size=18, color=TEXT_MAIN).next_to(ring, DOWN, buff=0.15)
    return VGroup(ring, mark, label)


class Scene01Hook(Scene):
    def construct(self):
        title = create_title("Como os bancos ganham dinheiro")
        line1 = Text("Se voce quer trabalhar com dados no mercado financeiro,", font_size=30, color=TEXT_MAIN)
        line2 = Text("precisa entender uma coisa antes de tudo:", font_size=30, color=TEXT_MAIN)
        line3 = Text("como um banco decide quem emprestar dinheiro.", font_size=34, color=ACCENT_YELLOW)
        line4 = Text("Porque e assim que ele ganha bilhoes.", font_size=32, color=ACCENT_GREEN)
        copy = VGroup(line1, line2, line3, line4).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        copy.next_to(title, DOWN, buff=0.55).align_to(title, LEFT)

        saver = create_person("depositante", ACCENT_BLUE).move_to(LEFT * 4.8 + DOWN * 1.5)
        borrower = create_person("tomador", ACCENT_ORANGE).move_to(RIGHT * 4.8 + DOWN * 1.5)
        bank = create_bank().move_to(DOWN * 1.15)
        decision = create_box("decisao", "quem recebe o dinheiro?", color=ACCENT_YELLOW, width=3.4).to_edge(DOWN, buff=0.5)
        left_arrow = create_arrow_between(saver, bank, color=ACCENT_BLUE)
        right_arrow = create_arrow_between(bank, borrower, color=ACCENT_ORANGE)
        decision_arrow = create_vertical_arrow_between(bank, decision, color=ACCENT_YELLOW)

        self.play(FadeIn(title), run_time=0.9)
        for line in copy:
            self.play(Write(line), run_time=0.8)
            self.wait(0.15)

        self.play(FadeIn(saver, shift=RIGHT * 0.25), FadeIn(borrower, shift=LEFT * 0.25), FadeIn(bank, shift=UP * 0.2), run_time=1.0)
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow), run_time=0.8)
        self.play(FadeIn(decision), GrowArrow(decision_arrow), run_time=0.9)
        self.play(Indicate(line3, color=ACCENT_YELLOW), Indicate(decision[0], color=ACCENT_YELLOW), run_time=1.0)
        self.wait(1.0)


class Scene02ExpectationBreak(Scene):
    def construct(self):
        title = create_title("O que todo mundo ve")
        bank = create_bank().shift(UP * 1.05)
        phone = create_phone_icon("app", ACCENT_CYAN).shift(LEFT * 3.9 + DOWN * 0.25)
        card = create_card_icon("cartao", ACCENT_BLUE).shift(RIGHT * 3.8 + DOWN * 0.2)
        people = VGroup(
            create_person("cliente", ACCENT_GREEN, 0.78).shift(LEFT * 5.2 + DOWN * 2.0),
            create_person("cliente", ACCENT_ORANGE, 0.78).shift(RIGHT * 5.0 + DOWN * 2.0),
        )
        text1 = create_box("guardar dinheiro", "ou so deixar parado?", color=ACCENT_BLUE, width=3.2).shift(LEFT * 3.2 + DOWN * 1.1)
        text2 = create_box("transferencias", "pix, ted, app", color=ACCENT_CYAN, width=3.1).shift(RIGHT * 3.1 + DOWN * 1.1)
        verdict = Text("Mas isso nao explica bilhoes de lucro.", font_size=36, color=ACCENT_RED).to_edge(DOWN, buff=0.65)
        cross1 = Cross(text1[0], stroke_color=ACCENT_RED, stroke_width=7)
        cross2 = Cross(text2[0], stroke_color=ACCENT_RED, stroke_width=7)

        self.play(FadeIn(title), FadeIn(bank, shift=DOWN * 0.2), run_time=1.0)
        self.play(FadeIn(phone), FadeIn(card), FadeIn(people), run_time=0.9)
        self.play(FadeIn(text1, shift=UP * 0.2), FadeIn(text2, shift=UP * 0.2), run_time=0.9)
        self.wait(0.4)
        self.play(Create(cross1), Create(cross2), run_time=0.8)
        self.play(Write(verdict), run_time=1.0)
        self.play(Indicate(verdict, color=ACCENT_RED), run_time=0.9)
        self.wait(1.0)


class Scene03CoreIdea(Scene):
    def construct(self):
        title = create_title("A grande ideia")
        saver = create_person("pessoa A", ACCENT_GREEN).shift(LEFT * 5.0 + UP * 0.2)
        saver_money = create_coin_stack("dinheiro sobrando", ACCENT_GREEN).next_to(saver, DOWN, buff=0.28)
        bank = create_bank().move_to(UP * 0.15)
        borrower = create_person("pessoa B", ACCENT_ORANGE).shift(RIGHT * 5.0 + UP * 0.2)
        borrower_need = create_box("precisa de caixa", "quer usar agora", color=ACCENT_ORANGE, width=2.8, height=1.3).next_to(borrower, DOWN, buff=0.28)
        left_arrow = create_arrow_between(saver, bank, color=ACCENT_GREEN)
        right_arrow = create_arrow_between(bank, borrower, color=ACCENT_ORANGE)
        tags = VGroup(
            create_chip("quem tem", ACCENT_GREEN),
            create_chip("intermedia", ACCENT_YELLOW),
            create_chip("quem precisa", ACCENT_ORANGE),
        ).arrange(RIGHT, buff=0.32).to_edge(DOWN, buff=1.25)
        punch = Text("E tipo um Airbnb do dinheiro.", font_size=38, color=ACCENT_YELLOW).to_edge(DOWN, buff=0.48)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(saver), FadeIn(borrower), FadeIn(bank), run_time=1.0)
        self.play(FadeIn(saver_money), FadeIn(borrower_need), run_time=0.8)
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow), run_time=0.9)
        self.play(FadeIn(tags), run_time=0.7)
        self.play(Write(punch), run_time=1.0)
        self.play(Indicate(bank, color=ACCENT_YELLOW), run_time=0.9)
        self.wait(1.0)


class Scene04Spread(Scene):
    def construct(self):
        title = create_title("De onde vem o lucro")
        saver_box = create_box("capta a 15%", "exemplo: cdi", color=ACCENT_GREEN, width=3.0).shift(LEFT * 4.5 + UP * 0.4)
        bank = create_bank().move_to(UP * 0.1)
        borrower_box = create_box("empresta a 25%", "credito pessoal", color=ACCENT_RED, width=3.25).shift(RIGHT * 4.5 + UP * 0.4)
        left_arrow = create_arrow_between(saver_box, bank, color=ACCENT_GREEN)
        right_arrow = create_arrow_between(bank, borrower_box, color=ACCENT_RED)

        rate_bar = RoundedRectangle(
            corner_radius=0.18,
            width=8.0,
            height=1.15,
            stroke_color=ACCENT_YELLOW,
            stroke_width=2.8,
            fill_color=BACKGROUND_FILL,
            fill_opacity=0.94,
        ).to_edge(DOWN, buff=1.0)
        left_fill = Rectangle(width=2.8, height=0.68, stroke_width=0, fill_color=ACCENT_GREEN, fill_opacity=0.7).move_to(rate_bar.get_left() + RIGHT * 1.75)
        right_fill = Rectangle(width=4.2, height=0.68, stroke_width=0, fill_color=ACCENT_RED, fill_opacity=0.55).move_to(rate_bar.get_left() + RIGHT * 5.2)
        left_label = Text("15%", font_size=34, color=WHITE).move_to(left_fill)
        right_label = Text("25%", font_size=34, color=WHITE).move_to(right_fill)
        spread = create_box("spread = lucro", "25% - 15% = 10%", color=ACCENT_YELLOW, width=3.6, height=1.3).next_to(rate_bar, UP, buff=0.34)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(saver_box), FadeIn(bank), FadeIn(borrower_box), run_time=1.0)
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow), run_time=0.9)
        self.play(Create(rate_bar), FadeIn(left_fill), FadeIn(right_fill), run_time=0.9)
        self.play(Write(left_label), Write(right_label), run_time=0.7)
        self.play(FadeIn(spread), run_time=0.9)
        self.play(Indicate(spread[1], color=ACCENT_YELLOW), run_time=0.9)
        self.wait(1.0)


class Scene05RealWorldProblem(Scene):
    def construct(self):
        title = create_title("Sem banco, o mundo real trava")
        stranger_a = create_person("voce", ACCENT_BLUE).shift(LEFT * 4.5 + UP * 0.5)
        stranger_b = create_person("desconhecido", ACCENT_ORANGE).shift(RIGHT * 4.5 + UP * 0.5)
        dashed = DashedLine(stranger_a.get_right(), stranger_b.get_left(), dash_length=0.16, color=TEXT_MUTED, stroke_width=4)

        q1 = create_box("Como confiar?", "nao conheco essa pessoa", color=ACCENT_RED, width=3.3).shift(LEFT * 3.6 + DOWN * 1.6)
        q2 = create_box("Como encontrar?", "quem precisa agora?", color=ACCENT_ORANGE, width=3.2).shift(ORIGIN + DOWN * 1.6)
        q3 = create_box("E se nao pagar?", "quem cobra depois?", color=ACCENT_RED, width=3.1).shift(RIGHT * 3.6 + DOWN * 1.6)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(stranger_a, shift=RIGHT * 0.25), FadeIn(stranger_b, shift=LEFT * 0.25), run_time=0.9)
        self.play(Create(dashed), run_time=0.7)
        self.play(FadeIn(q1, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(q2, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(q3, shift=UP * 0.2), run_time=0.7)
        self.play(Wiggle(dashed), run_time=0.9)
        self.wait(1.0)


class Scene06ChaosWithoutIntermediary(Scene):
    def construct(self):
        title = create_title("O caos sem intermediario")
        people = VGroup(
            create_person("A", ACCENT_BLUE, 0.7).move_to(LEFT * 5.2 + UP * 1.4),
            create_person("B", ACCENT_GREEN, 0.7).move_to(LEFT * 1.5 + UP * 1.9),
            create_person("C", ACCENT_ORANGE, 0.7).move_to(RIGHT * 2.2 + UP * 1.2),
            create_person("D", ACCENT_RED, 0.7).move_to(RIGHT * 5.0 + UP * 1.9),
            create_person("E", ACCENT_CYAN, 0.7).move_to(LEFT * 3.6 + DOWN * 1.4),
            create_person("F", ACCENT_YELLOW, 0.7).move_to(RIGHT * 4.2 + DOWN * 1.2),
        )

        arrows = VGroup(
            CurvedArrow(people[0].get_right(), people[2].get_left(), color=ACCENT_RED, angle=-0.35),
            CurvedArrow(people[1].get_right(), people[3].get_left(), color=ACCENT_ORANGE, angle=0.3),
            CurvedArrow(people[4].get_right(), people[1].get_left(), color=ACCENT_BLUE, angle=0.4),
            CurvedArrow(people[2].get_bottom(), people[5].get_top(), color=ACCENT_GREEN, angle=-0.4),
            CurvedArrow(people[5].get_left(), people[4].get_right(), color=ACCENT_CYAN, angle=0.25),
        )

        tags = VGroup(
            create_box("nao e so dinheiro", "o problema central", color=ACCENT_YELLOW, width=3.2),
            create_box("confianca", "quem paga?", color=ACCENT_RED, width=2.6),
            create_box("informacao", "quem e bom?", color=ACCENT_BLUE, width=2.7),
            create_box("conexao", "quem encontra quem?", color=ACCENT_GREEN, width=2.8),
        ).arrange(RIGHT, buff=0.28).scale(0.84).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(people), run_time=1.0)
        self.play(*[Create(arrow) for arrow in arrows], run_time=1.1)
        self.play(*[Wiggle(arrow) for arrow in arrows], run_time=1.2)
        self.play(FadeIn(tags[0]), run_time=0.7)
        self.play(FadeIn(tags[1:]), run_time=0.8)
        self.wait(1.0)


class Scene07RealRole(Scene):
    def construct(self):
        title = create_title("O papel real do banco")
        bank = create_bank().scale(1.08)
        bank.move_to(ORIGIN + UP * 0.2)

        people = VGroup(
            create_person("cliente 1", ACCENT_BLUE, 0.7).move_to(LEFT * 5.0 + UP * 1.9),
            create_person("cliente 2", ACCENT_GREEN, 0.7).move_to(LEFT * 5.4 + DOWN * 0.4),
            create_person("cliente 3", ACCENT_ORANGE, 0.7).move_to(LEFT * 4.5 + DOWN * 2.2),
            create_person("cliente 4", ACCENT_CYAN, 0.7).move_to(RIGHT * 4.8 + UP * 1.8),
            create_person("cliente 5", ACCENT_RED, 0.7).move_to(RIGHT * 5.3 + DOWN * 0.1),
            create_person("cliente 6", ACCENT_YELLOW, 0.7).move_to(RIGHT * 4.3 + DOWN * 2.1),
        )
        lines = VGroup(
            *[Line(bank.get_center(), person.get_center(), stroke_width=2.6, color=TEXT_MUTED) for person in people]
        )

        data_cards = VGroup(
            create_metric_card("score", "742", ACCENT_GREEN),
            create_metric_card("renda", "R$ 8.500", ACCENT_BLUE),
            create_metric_card("historico", "36 meses", ACCENT_CYAN),
        ).arrange(DOWN, buff=0.18).next_to(bank, DOWN, buff=0.55)

        payoff = Text("Ele transforma desconfianca em transacao.", font_size=36, color=ACCENT_YELLOW).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(title), FadeIn(bank), run_time=1.0)
        self.play(FadeIn(people), run_time=0.9)
        self.play(*[Create(line) for line in lines], run_time=1.0)
        self.play(FadeIn(data_cards, shift=UP * 0.15), run_time=0.9)
        self.play(Write(payoff), run_time=1.0)
        self.play(Indicate(bank, color=ACCENT_YELLOW), run_time=0.9)
        self.wait(1.0)


class Scene08DeepInsight(Scene):
    def construct(self):
        title = create_title("O jogo de verdade")
        note = Text("Banco nao ganha so emprestando.", font_size=30, color=TEXT_MAIN).next_to(title, DOWN, buff=0.3)
        note2 = Text("Ele ganha escolhendo melhor.", font_size=38, color=ACCENT_YELLOW).next_to(note, DOWN, buff=0.18)

        applicants = VGroup(
            create_box("candidato A", "risco baixo", color=ACCENT_GREEN, width=2.7, height=1.35),
            create_box("candidato B", "risco medio", color=ACCENT_ORANGE, width=2.7, height=1.35),
            create_box("candidato C", "risco alto", color=ACCENT_RED, width=2.7, height=1.35),
        ).arrange(DOWN, buff=0.32).shift(LEFT * 3.7 + DOWN * 0.55)
        bank = create_bank().shift(RIGHT * 0.1 + DOWN * 0.2)
        approved = create_box("dinheiro liberado", "para quem faz sentido", color=ACCENT_YELLOW, width=3.5, height=1.45).shift(RIGHT * 4.3 + DOWN * 0.25)
        arrows = VGroup(
            Arrow(applicants[0].get_right(), bank.get_left() + UP * 0.35, color=ACCENT_GREEN, stroke_width=4, buff=0.16),
            Arrow(applicants[1].get_right(), bank.get_left(), color=ACCENT_ORANGE, stroke_width=4, buff=0.16),
            Arrow(applicants[2].get_right(), bank.get_left() + DOWN * 0.35, color=ACCENT_RED, stroke_width=4, buff=0.16),
        )
        output_arrow = create_arrow_between(bank, approved, color=ACCENT_YELLOW)
        highlight = SurroundingRectangle(applicants[0], color=ACCENT_GREEN, buff=0.12, corner_radius=0.16)

        self.play(FadeIn(title), FadeIn(note), FadeIn(note2), run_time=1.0)
        self.play(FadeIn(applicants), FadeIn(bank), run_time=1.0)
        self.play(*[GrowArrow(arrow) for arrow in arrows], run_time=0.9)
        self.play(Create(highlight), run_time=0.7)
        self.play(GrowArrow(output_arrow), FadeIn(approved), run_time=0.9)
        self.play(Indicate(note2, color=ACCENT_YELLOW), Indicate(approved[1], color=ACCENT_YELLOW), run_time=0.9)
        self.wait(1.0)


class Scene09OtherRevenue(Scene):
    def construct(self):
        title = create_title("Nao e so emprestimo")
        bank = create_bank().move_to(UP * 0.25)
        icons = VGroup(
            create_revenue_icon("cartao", ACCENT_BLUE, "$"),
            create_revenue_icon("tarifas", ACCENT_CYAN, "%"),
            create_revenue_icon("seguros", ACCENT_GREEN, "S"),
            create_revenue_icon("investimentos", ACCENT_ORANGE, "+"),
        )
        icons.arrange(RIGHT, buff=0.85).to_edge(DOWN, buff=1.3)

        arrows = VGroup(
            Arrow(icon.get_top(), bank.get_bottom() + RIGHT * shift, color=TEXT_MUTED, stroke_width=3.6, buff=0.16)
            for icon, shift in zip(icons, (-1.5, -0.5, 0.5, 1.5))
        )

        banner = create_box("mesmo sem perceber,", "voce paga por varios servicos", color=ACCENT_RED, width=4.3, height=1.35).next_to(bank, DOWN, buff=0.55)

        self.play(FadeIn(title), FadeIn(bank), run_time=0.9)
        self.play(FadeIn(icons, shift=UP * 0.15), run_time=0.9)
        self.play(*[GrowArrow(arrow) for arrow in arrows], run_time=0.9)
        self.play(FadeIn(banner), run_time=0.8)
        self.play(Indicate(icons, color=ACCENT_YELLOW), run_time=0.9)
        self.wait(1.0)


class Scene10Balance(Scene):
    def construct(self):
        title = create_title("O equilibrio constante")
        scale = create_scale().shift(DOWN * 0.2)
        left_label = create_box("ganhar com juros", "receita", color=ACCENT_BLUE, width=2.6, height=1.2).move_to(scale[5].get_center() + UP * 0.9)
        right_label = create_box("evitar calote", "risco", color=ACCENT_RED, width=2.4, height=1.2).move_to(scale[6].get_center() + UP * 0.9)
        system_label = create_box("sem travar o sistema", "juros altos demais afastam gente boa", color=ACCENT_YELLOW, width=4.9, height=1.45).to_edge(DOWN, buff=0.4)
        beam = scale[2]

        self.play(FadeIn(title), Create(scale), run_time=1.1)
        self.play(FadeIn(left_label), FadeIn(right_label), run_time=0.8)
        self.play(Rotate(beam, angle=-0.13, about_point=ORIGIN), run_time=0.7)
        self.play(Rotate(beam, angle=0.24, about_point=ORIGIN), run_time=0.9)
        self.play(Rotate(beam, angle=-0.11, about_point=ORIGIN), run_time=0.7)
        self.play(FadeIn(system_label), run_time=0.9)
        self.play(Indicate(system_label[0], color=ACCENT_YELLOW), run_time=0.9)
        self.wait(1.0)


class Scene11Conclusion(Scene):
    def construct(self):
        title = create_title("Resumo")
        steps = VGroup(
            create_box("1. conecta pessoas", color=ACCENT_BLUE, width=2.8, height=1.15, title_size=24),
            create_box("2. paga menos do que cobra", color=ACCENT_GREEN, width=3.3, height=1.15, title_size=22),
            create_box("3. reduz risco", color=ACCENT_ORANGE, width=2.4, height=1.15, title_size=24),
            create_box("4. facilita tudo", color=ACCENT_YELLOW, width=2.5, height=1.15, title_size=24),
        ).arrange(RIGHT, buff=0.28).scale(0.92).shift(UP * 0.1)

        arrows = VGroup(
            *[
                create_arrow_between(steps[index], steps[index + 1], color=TEXT_MUTED, buff=0.08, stroke_width=3)
                for index in range(len(steps) - 1)
            ]
        )

        final_line = Text("Banco e infraestrutura de confianca.", font_size=38, color=ACCENT_YELLOW).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(steps[0]), run_time=0.6)
        for index in range(len(arrows)):
            self.play(GrowArrow(arrows[index]), FadeIn(steps[index + 1]), run_time=0.75)
        self.play(Write(final_line), run_time=1.0)
        self.play(Indicate(final_line, color=ACCENT_YELLOW), run_time=0.9)
        self.wait(1.0)


class Scene12NextVideoHook(Scene):
    def construct(self):
        title = create_title("Isso e so a superficie")
        surface = RoundedRectangle(
            corner_radius=0.16,
            width=8.4,
            height=0.9,
            stroke_color=ACCENT_CYAN,
            stroke_width=3,
            fill_color=ACCENT_CYAN,
            fill_opacity=0.18,
        ).shift(UP * 0.85)
        surface_text = Text("o que voce enxerga do banco", font_size=24, color=TEXT_MAIN).move_to(surface.get_center())

        below = VGroup(
            create_chip("matematica", ACCENT_BLUE),
            create_chip("dados", ACCENT_GREEN),
            create_chip("modelos", ACCENT_YELLOW),
            create_chip("risco", ACCENT_RED),
            create_chip("decisao", ACCENT_ORANGE),
        ).arrange(RIGHT, buff=0.32).shift(DOWN * 1.15)

        arrow = Arrow(surface.get_bottom(), below.get_top(), color=TEXT_MUTED, stroke_width=4, buff=0.15)
        next_box = create_box("proximo video", "como dados e modelos decidem isso", color=ACCENT_YELLOW, width=4.6, height=1.5).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(surface), Write(surface_text), run_time=0.9)
        self.play(GrowArrow(arrow), FadeIn(below, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(next_box), run_time=0.9)
        self.play(Indicate(next_box, color=ACCENT_YELLOW), run_time=0.9)
        self.wait(1.0)
