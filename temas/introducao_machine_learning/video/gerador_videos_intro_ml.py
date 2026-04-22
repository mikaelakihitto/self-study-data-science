from pathlib import Path

from manim import *
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Direct all Manim outputs (videos/images/partials) to this theme assets folder.
config.media_dir = str(ASSETS_DIR)


"""
Render examples:
  manim -pql temas/introducao_machine_learning/video/gerador_videos_intro_ml.py DecisionTreeSimple
  manim -pql temas/introducao_machine_learning/video/gerador_videos_intro_ml.py LinearRegressionSimple
"""


class DecisionTreeSimple(Scene):
    def make_node(
        self,
        text: str,
        color=BLUE_E,
        width: float = 2.8,
        height: float = 1.0,
        font_size: int = 24,
    ):
        box = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=height,
            stroke_color=color,
            stroke_width=3,
        )
        label = Text(text, font_size=font_size).move_to(box.get_center())
        return VGroup(box, label)

    def construct(self):
        slow = 1.6
        level_time = 2.0

        title = Text("Arvore de Decisao: Credito Bancario", font_size=38).to_edge(UP)
        self.play(Write(title), run_time=slow)

        root = self.make_node("Idade > 18?", color=YELLOW_E, width=3.0).shift(2.2 * UP)
        node_serasa = self.make_node("Nome sujo no Serasa?", color=BLUE_E, width=3.9).shift(0.8 * UP)
        node_score = self.make_node("Score Serasa > 700?", color=BLUE_E, width=3.9).shift(0.6 * DOWN)

        leaf_neg_idade = self.make_node("Nega credito", color=RED_E, width=2.9).shift(4.4 * RIGHT + 2.2 * UP)
        leaf_neg_serasa = self.make_node("Nega credito", color=RED_E, width=2.9).shift(4.4 * RIGHT + 0.8 * UP)
        leaf_aprova = self.make_node("Libera credito", color=GREEN_E, width=3.1).shift(2.8 * LEFT + 2.4 * DOWN)
        leaf_neg_score = self.make_node("Nega credito", color=RED_E, width=2.9).shift(2.8 * RIGHT + 2.4 * DOWN)

        e_root_sim = Line(root.get_bottom(), node_serasa.get_top(), stroke_width=4)
        e_root_nao = Line(root.get_right(), leaf_neg_idade.get_left(), stroke_width=4)
        e_serasa_sim = Line(node_serasa.get_right(), leaf_neg_serasa.get_left(), stroke_width=4)
        e_serasa_nao = Line(node_serasa.get_bottom(), node_score.get_top(), stroke_width=4)
        e_score_sim = Line(node_score.get_bottom() + 0.8 * LEFT, leaf_aprova.get_top(), stroke_width=4)
        e_score_nao = Line(node_score.get_bottom() + 0.8 * RIGHT, leaf_neg_score.get_top(), stroke_width=4)

        l_root_sim = Text("Sim", font_size=24, color=GREEN_E).next_to(e_root_sim, LEFT, buff=0.1)
        l_root_nao = Text("Nao", font_size=24, color=RED_E).next_to(e_root_nao, UP, buff=0.1)
        l_serasa_sim = Text("Sim", font_size=24, color=RED_E).next_to(e_serasa_sim, UP, buff=0.1)
        l_serasa_nao = Text("Nao", font_size=24, color=GREEN_E).next_to(e_serasa_nao, LEFT, buff=0.1)
        l_score_sim = Text("Sim", font_size=24, color=GREEN_E).next_to(e_score_sim, LEFT, buff=0.1)
        l_score_nao = Text("Nao", font_size=24, color=RED_E).next_to(e_score_nao, RIGHT, buff=0.1)

        # Top -> bottom reveal: each level appears with its connecting lines.
        self.play(Create(root), run_time=slow)

        self.play(
            Create(e_root_sim),
            Create(node_serasa),
            Create(e_root_nao),
            Create(leaf_neg_idade),
            run_time=level_time,
        )
        self.play(Write(l_root_sim), run_time=slow)
        self.play(Write(l_root_nao), run_time=slow)

        self.play(
            Create(e_serasa_nao),
            Create(node_score),
            Create(e_serasa_sim),
            Create(leaf_neg_serasa),
            run_time=level_time,
        )
        self.play(Write(l_serasa_nao), run_time=slow)
        self.play(Write(l_serasa_sim), run_time=slow)

        self.play(
            Create(e_score_sim),
            Create(leaf_aprova),
            Create(e_score_nao),
            Create(leaf_neg_score),
            run_time=level_time,
        )
        self.play(Write(l_score_sim), run_time=slow)
        self.play(Write(l_score_nao), run_time=slow)
        self.wait(2.0)


class LinearRegressionSimple(Scene):
    def construct(self):
        title = Text("Regressao Linear: Renda x Cartao", font_size=40).to_edge(UP)
        self.play(Write(title))

        problem = Text(
            "Problema: estimar a renda mensal pela fatura do cartao",
            font_size=28,
        ).next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(problem, shift=0.2 * DOWN))
        self.wait(0.6)

        axes = Axes(
            x_range=[0, 20000, 5000],
            y_range=[0, 70000, 10000],
            x_length=6.8,
            y_length=4.4,
            axis_config={"include_numbers": True},
            tips=False,
        ).shift(1.55 * LEFT + 0.3 * DOWN)

        x_label = Text("Gasto no cartao (R$/mes)", font_size=21).next_to(axes.x_axis, DOWN, buff=0.22)
        y_label = Text("Renda mensal (R$)", font_size=24).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.35)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.6)

        seed = 42
        rng = np.random.default_rng(seed)
        x_vals = np.clip(np.linspace(700.0, 18000.0, 10) + rng.normal(0.0, 900.0, 10), 300.0, 19500.0)
        x_vals.sort()
        y_vals = np.clip(3.1 * x_vals + 2500.0 + rng.normal(0.0, 9000.0, 10), 1200.0, 68000.0)
        points_xy = list(zip(x_vals.tolist(), y_vals.tolist()))
        points = VGroup(*[Dot(axes.c2p(x, y), color=BLUE_E, radius=0.075) for x, y in points_xy])

        self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in points], lag_ratio=0.12, run_time=2.0))
        self.wait(0.6)

        fit_line = axes.plot(lambda x: 3.0 * x + 3000.0, x_range=[300, 19000], color=YELLOW)
        equation = MathTex(
            r"\widehat{\text{renda}} = 3.0 \cdot \text{gasto} + 3000",
            color=YELLOW,
        ).scale(0.66).to_edge(RIGHT, buff=0.35).shift(0.3 * UP)

        self.play(Create(fit_line), Write(equation))

        example_x = 8000.0
        predicted_y = 3.0 * example_x + 3000.0
        example_point = Dot(axes.c2p(example_x, predicted_y), color=YELLOW, radius=0.09)
        v_line = DashedLine(axes.c2p(example_x, 0), axes.c2p(example_x, predicted_y), color=YELLOW_C)
        h_line = DashedLine(axes.c2p(0, predicted_y), axes.c2p(example_x, predicted_y), color=YELLOW_C)
        example_text = VGroup(
            Text("Exemplo: gasto = R$ 8.000", font_size=19, color=YELLOW_D),
            Text("renda prevista ~ R$ 27.000", font_size=19, color=YELLOW_D),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(equation, DOWN, buff=0.18).align_to(equation, LEFT)

        self.play(Create(v_line), Create(h_line), FadeIn(example_point))
        self.play(Write(example_text))
        self.wait(1.8)
