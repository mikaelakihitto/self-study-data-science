from pathlib import Path

from manim import *


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
        title = Text("Regressao Linear (simples)", font_size=42).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=8,
            y_length=4.8,
            axis_config={"include_numbers": True},
        ).shift(0.4 * DOWN)
        labels = axes.get_axis_labels(Text("x"), Text("y"))
        self.play(Create(axes), Write(labels))

        points_xy = [(1, 1.8), (2, 2.7), (3, 3.9), (5, 5.1), (7, 6.8), (8, 7.6)]
        points = VGroup(*[Dot(axes.c2p(x, y), color=BLUE, radius=0.08) for x, y in points_xy])
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in points], lag_ratio=0.15))

        fit_line = axes.plot(lambda x: 0.82 * x + 1.0, x_range=[0, 10], color=YELLOW)
        equation = MathTex(r"\hat{y} = 0.82x + 1.0", color=YELLOW).scale(0.9).to_corner(UR).shift(0.2 * DOWN)
        self.play(Create(fit_line), Write(equation))

        sample_x, sample_y = points_xy[3]
        y_pred = 0.82 * sample_x + 1.0
        residual = DashedLine(axes.c2p(sample_x, sample_y), axes.c2p(sample_x, y_pred), color=RED)
        residual_label = Text("erro", font_size=24, color=RED).next_to(residual, RIGHT, buff=0.12)
        self.play(Create(residual), Write(residual_label))

        takeaway = Text("A reta minimiza os erros dos pontos", font_size=30, color=GRAY_B).to_edge(DOWN)
        self.play(Write(takeaway))
        self.wait(1.5)
