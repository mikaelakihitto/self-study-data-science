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
    SURFACE_ALT,
    TEXT_MAIN,
    TEXT_MUTED,
    clear_scene,
    configure_default_video_output,
    create_arrow_between,
    create_box as build_box,
    create_chip as build_chip,
    create_panel as build_panel,
    create_title,
    create_vector_visual as build_vector_visual,
)


SURFACE = "#121A2B"


BASE_DIR, ASSETS_DIR = configure_default_video_output(__file__)


def create_chip(label: str, color=ACCENT_BLUE, font_size: int = 28):
    return build_chip(
        label,
        color=color,
        font_size=font_size,
        text_color=TEXT_MAIN,
        fill_color=SURFACE,
        fill_opacity=0.96,
        stroke_width=2.6,
        height=0.8,
        horizontal_padding=0.55,
    )


def create_box(
    title: str,
    subtitle: str = "",
    width: float = 3.2,
    height: float = 1.6,
    color=ACCENT_BLUE,
    title_size: int = 30,
    subtitle_size: int = 20,
):
    return build_box(
        title,
        subtitle=subtitle,
        width=width,
        height=height,
        color=color,
        fill_color=SURFACE,
        fill_opacity=0.96,
        title_size=title_size,
        subtitle_size=subtitle_size,
        subtitle_color=TEXT_MAIN,
        content_buff=0.12,
    )


def create_panel(body, title: str = "", color=ACCENT_BLUE, padding: float = 0.28, min_width: float = 0.0, min_height: float = 0.0):
    return build_panel(
        body,
        title=title or None,
        color=color,
        padding=padding,
        min_width=min_width,
        min_height=min_height,
        fill_color=SURFACE,
        fill_opacity=0.94,
        corner_radius=0.22,
        stroke_width=2.6,
        title_font_size=26,
        title_buff=0.18,
    )


def create_vector_visual(label: str, values, color=ACCENT_GREEN, width: float = 4.6, height: float = 1.45):
    return build_vector_visual(
        label,
        values,
        color=color,
        width=width,
        height=height,
        fill_color=SURFACE,
        fill_opacity=0.96,
    )


class Scene01Hook(Scene):
    def construct(self):
        # Scene 1: hook the viewer with the core idea that AI turns meaning into numbers.
        title = create_title("Embedding: significado em números")
        statement = Text(
            "IA não entende palavras, clientes ou transações",
            font_size=34,
            color=TEXT_MAIN,
        ).shift(UP * 2.0)
        numbers_statement = Text("IA entende números", font_size=42, color=ACCENT_GREEN).move_to(statement)

        words = VGroup(
            create_chip("palavra", ACCENT_BLUE),
            create_chip("cliente", ACCENT_CYAN),
            create_chip("transação", ACCENT_ORANGE),
        ).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.9).shift(DOWN * 0.15)

        vectors = VGroup(
            create_vector_visual("vetor", [0.12, -0.44, 0.87], ACCENT_BLUE, width=4.2),
            create_vector_visual("vetor", [0.72, 0.11, -0.30], ACCENT_CYAN, width=4.2),
            create_vector_visual("vetor", [-0.20, 0.91, 0.33], ACCENT_ORANGE, width=4.2),
        ).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.15)

        arrows = VGroup(
            *[create_arrow_between(words[index], vectors[index]) for index in range(3)]
        )

        final_line = Text(
            "Embedding = transformar significado em números",
            font_size=38,
            color=ACCENT_YELLOW,
        ).to_edge(DOWN, buff=0.7)

        self.play(FadeIn(title), Write(statement), run_time=1.2)
        self.wait(0.7)
        self.play(Transform(statement, numbers_statement), run_time=1.1)
        self.wait(0.6)

        for index in range(3):
            self.play(
                FadeIn(words[index], shift=0.2 * RIGHT),
                GrowArrow(arrows[index]),
                FadeIn(vectors[index], shift=0.2 * LEFT),
                run_time=0.85,
            )
        self.wait(0.8)

        self.play(Write(final_line), run_time=1.2)
        self.play(Indicate(final_line, color=ACCENT_YELLOW), run_time=0.9)
        self.wait(1.2)


class Scene02Problem(Scene):
    def construct(self):
        # Scene 2: show that raw strings do not carry similarity for a model.
        title = create_title("O problema da similaridade")
        intro = Text("Para nós, isso é óbvio.", font_size=30, color=TEXT_MUTED).next_to(title, DOWN, buff=0.25)

        gato = create_chip("gato", ACCENT_BLUE).move_to(LEFT * 3.4 + UP * 0.5)
        cachorro = create_chip("cachorro", ACCENT_GREEN).move_to(LEFT * 1.45 + UP * 0.5)
        carro = create_chip("carro", ACCENT_RED).move_to(RIGHT * 3.1 + UP * 0.4)
        words = VGroup(gato, cachorro, carro)

        human_note = Text("gato e cachorro parecem próximos", font_size=28, color=ACCENT_GREEN).shift(DOWN * 0.6)
        computer_note = Text("Para o computador: são só strings", font_size=30, color=TEXT_MAIN).shift(UP * 1.35)

        raw_strings = VGroup(
            Text('"gato"', font_size=28, color=TEXT_MAIN),
            Text('"cachorro"', font_size=28, color=TEXT_MAIN),
            Text('"carro"', font_size=28, color=TEXT_MAIN),
        ).arrange(DOWN, buff=0.24).move_to(LEFT * 4.6 + DOWN * 1.45)

        model_box = create_box(
            "modelo",
            "recebe texto cru",
            width=3.3,
            height=1.6,
            color=ACCENT_RED,
        ).move_to(RIGHT * 1.6 + DOWN * 1.45)
        doubt = Text("não sei o que é parecido", font_size=20, color=ACCENT_RED).next_to(model_box, RIGHT, buff=0.45)
        arrows = VGroup(
            *[
                Arrow(
                    raw_strings[index].get_right(),
                    model_box.get_left() + UP * (0.45 - 0.45 * index),
                    buff=0.12,
                    stroke_width=3.5,
                    color=TEXT_MUTED,
                    max_tip_length_to_length_ratio=0.14,
                )
                for index in range(3)
            ]
        )

        final_line = Text(
            "O modelo precisa de uma forma matemática de entender similaridade",
            font_size=32,
            color=ACCENT_YELLOW,
        ).to_edge(DOWN, buff=0.7)

        self.play(FadeIn(title), FadeIn(intro), run_time=1.0)
        self.play(FadeIn(words), run_time=0.8)
        self.play(
            gato.animate.shift(RIGHT * 0.35),
            cachorro.animate.shift(LEFT * 0.25),
            carro.animate.shift(RIGHT * 0.45),
            run_time=0.9,
        )
        self.play(Indicate(gato, color=ACCENT_GREEN), Indicate(cachorro, color=ACCENT_GREEN), run_time=0.9)
        self.play(Write(human_note), run_time=0.8)
        self.wait(0.7)

        self.play(FadeOut(human_note), FadeIn(computer_note), run_time=0.8)
        self.play(FadeIn(raw_strings), FadeIn(model_box), run_time=1.0)
        self.play(*[GrowArrow(arrow) for arrow in arrows], run_time=0.9)
        self.play(Write(doubt), run_time=0.8)
        self.wait(0.7)

        self.play(Write(final_line), run_time=1.2)
        self.play(Indicate(final_line, color=ACCENT_YELLOW), run_time=0.8)
        self.wait(1.1)


class Scene03Intuition(Scene):
    def construct(self):
        # Scene 3: map words to a 2D space and connect similarity with distance.
        title = create_title("Intuição: similaridade vira distância")
        intro = Text("Embedding transforma algo complexo em vetor.", font_size=31, color=TEXT_MAIN).next_to(title, DOWN, buff=0.25)

        vectors = VGroup(
            create_vector_visual("gato", [0.2, 0.7], ACCENT_BLUE, width=3.2, height=1.2),
            create_vector_visual("cachorro", [0.3, 0.7], ACCENT_GREEN, width=3.4, height=1.2),
            create_vector_visual("carro", [0.9, 0.1], ACCENT_RED, width=3.2, height=1.2),
        ).arrange(DOWN, buff=0.28).to_edge(LEFT, buff=0.55).shift(DOWN * 0.35)

        plane = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            x_length=6.2,
            y_length=4.6,
            tips=False,
            axis_config={"color": TEXT_MUTED, "stroke_width": 2.5, "include_numbers": False},
        ).to_edge(RIGHT, buff=0.75).shift(DOWN * 0.1)
        grid = NumberPlane(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            x_length=6.2,
            y_length=4.6,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.22, "stroke_width": 1},
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=2,
        ).move_to(plane)

        cat_dot = Dot(plane.c2p(0.2, 0.7), radius=0.08, color=ACCENT_BLUE)
        dog_dot = Dot(plane.c2p(0.3, 0.7), radius=0.08, color=ACCENT_GREEN)
        car_dot = Dot(plane.c2p(0.9, 0.1), radius=0.08, color=ACCENT_RED)
        cat_label = Text("gato", font_size=24, color=ACCENT_BLUE).next_to(cat_dot, UP, buff=0.12)
        dog_label = Text("cachorro", font_size=24, color=ACCENT_GREEN).next_to(dog_dot, UP, buff=0.12)
        car_label = Text("carro", font_size=24, color=ACCENT_RED).next_to(car_dot, RIGHT, buff=0.12)

        near_line = Line(cat_dot.get_center(), dog_dot.get_center(), color=ACCENT_GREEN, stroke_width=6)
        far_line = Line(cat_dot.get_center(), car_dot.get_center(), color=ACCENT_RED, stroke_width=4)
        final_line = Text("Similaridade vira distância", font_size=38, color=ACCENT_YELLOW).to_edge(DOWN, buff=0.7)

        self.play(FadeIn(title), FadeIn(intro), run_time=1.0)
        self.play(FadeIn(vectors), run_time=1.0)
        self.wait(0.6)
        self.play(Create(grid), Create(plane), run_time=1.1)
        self.play(
            FadeIn(cat_dot), FadeIn(cat_label),
            FadeIn(dog_dot), FadeIn(dog_label),
            FadeIn(car_dot), FadeIn(car_label),
            run_time=1.0,
        )
        self.wait(0.6)
        self.play(Create(near_line), Create(far_line), run_time=1.0)
        self.play(Indicate(near_line, color=ACCENT_GREEN), Indicate(far_line, color=ACCENT_RED), run_time=0.9)
        self.play(Write(final_line), run_time=1.0)
        self.wait(1.2)


class Scene04MapAnalogy(Scene):
    def construct(self):
        # Scene 4: use a map analogy to explain geometric placement of information.
        title = create_title("Embedding como um mapa")
        intro = Text("Cada ponto ocupa uma posição em um espaço.", font_size=31, color=TEXT_MAIN).next_to(title, DOWN, buff=0.25)

        plane = NumberPlane(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=9.2,
            y_length=5.1,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.2, "stroke_width": 1},
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=2,
        ).shift(DOWN * 0.2)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=9.2,
            y_length=5.1,
            tips=False,
            axis_config={"color": TEXT_MUTED, "stroke_width": 2.5, "include_numbers": False},
        ).move_to(plane)
        x_label = Text("x", font_size=24, color=TEXT_MUTED).next_to(axes.x_axis.get_end(), RIGHT, buff=0.12)
        y_label = Text("y", font_size=24, color=TEXT_MUTED).next_to(axes.y_axis.get_end(), UP, buff=0.12)
        frame = RoundedRectangle(
            corner_radius=0.25,
            width=9.55,
            height=5.45,
            stroke_color=ACCENT_BLUE,
            stroke_width=2.5,
            fill_color=SURFACE_ALT,
            fill_opacity=0.22,
        ).move_to(plane)

        dots = VGroup(
            Dot(plane.c2p(2.1, 4.4), radius=0.08, color=TEXT_MAIN),
            Dot(plane.c2p(2.7, 4.1), radius=0.08, color=TEXT_MAIN),
            Dot(plane.c2p(3.0, 4.55), radius=0.08, color=TEXT_MAIN),
            Dot(plane.c2p(2.45, 3.55), radius=0.08, color=TEXT_MAIN),
            Dot(plane.c2p(5.0, 3.05), radius=0.08, color=TEXT_MAIN),
            Dot(plane.c2p(5.55, 3.35), radius=0.08, color=TEXT_MAIN),
            Dot(plane.c2p(4.7, 2.45), radius=0.08, color=TEXT_MAIN),
            Dot(plane.c2p(7.45, 1.55), radius=0.08, color=TEXT_MAIN),
            Dot(plane.c2p(8.15, 1.9), radius=0.08, color=TEXT_MAIN),
            Dot(plane.c2p(8.7, 1.2), radius=0.08, color=TEXT_MAIN),
        )

        nearby_groups = VGroup(
            VGroup(*dots[:4]),
            VGroup(*dots[4:7]),
            VGroup(*dots[7:]),
        )
        proximity_circles = VGroup(
            Circle(radius=0.78, color=ACCENT_BLUE, stroke_width=4).move_to(nearby_groups[0].get_center()),
            Circle(radius=0.62, color=ACCENT_GREEN, stroke_width=4).move_to(nearby_groups[1].get_center()),
            Circle(radius=0.72, color=ACCENT_RED, stroke_width=4).move_to(nearby_groups[2].get_center()),
        )

        geo_note = Text("No mapa, pontos próximos formam regiões parecidas.", font_size=28, color=TEXT_MUTED).to_edge(DOWN, buff=0.95)
        concept_note = Text("No embedding, itens parecidos também se agrupam.", font_size=28, color=TEXT_MAIN).to_edge(DOWN, buff=0.95)
        concept_labels = VGroup(
            Text("clientes bets", font_size=24, color=ACCENT_BLUE).next_to(proximity_circles[0], UP, buff=0.16),
            Text("clientes pai de pet", font_size=24, color=ACCENT_GREEN).next_to(proximity_circles[1], RIGHT, buff=0.18),
            Text("clientes fraude", font_size=24, color=ACCENT_RED).next_to(proximity_circles[2], UP, buff=0.16),
        )
        final_line = Text("Embedding é colocar informação em um espaço", font_size=36, color=ACCENT_YELLOW).to_edge(DOWN, buff=0.68)

        self.play(FadeIn(title), FadeIn(intro), run_time=1.0)
        self.play(FadeIn(frame), Create(plane), run_time=1.1)
        self.play(
            Create(axes.x_axis),
            Create(axes.y_axis),
            FadeIn(x_label, shift=0.1 * RIGHT),
            FadeIn(y_label, shift=0.1 * UP),
            run_time=0.9,
        )
        self.play(
            LaggedStart(*[FadeIn(dot, scale=0.6) for dot in dots], lag_ratio=0.08),
            run_time=1.1,
        )
        self.play(
            LaggedStart(*[Create(circle) for circle in proximity_circles], lag_ratio=0.15),
            run_time=1.0,
        )
        self.play(Write(geo_note), run_time=0.8)
        self.wait(0.8)
        self.play(
            Transform(geo_note, concept_note),
            FadeIn(concept_labels, shift=0.15 * UP),
            run_time=1.0,
        )
        self.play(FadeOut(geo_note), run_time=0.4)
        self.play(Write(final_line), run_time=1.0)
        self.play(Indicate(final_line, color=ACCENT_YELLOW), run_time=0.9)
        self.wait(1.2)


class Scene05Finance(Scene):
    def construct(self):
        # Scene 5: connect embeddings to credit, fraud, and recommendation in finance.
        title = create_title("Mercado financeiro")
        intro = Text("No banco, clientes e transações também viram vetores.", font_size=30, color=TEXT_MAIN).next_to(title, DOWN, buff=0.24)

        self.play(FadeIn(title), FadeIn(intro), run_time=1.0)
        self.wait(0.4)

        credit_dots = VGroup(
            Dot(LEFT * 0.8 + UP * 0.2, radius=0.09, color=ACCENT_BLUE),
            Dot(LEFT * 0.3 + UP * 0.55, radius=0.09, color=ACCENT_BLUE),
            Dot(LEFT * 0.15 + DOWN * 0.15, radius=0.09, color=ACCENT_CYAN),
            Dot(LEFT * 0.65 + DOWN * 0.4, radius=0.09, color=ACCENT_CYAN),
            Dot(RIGHT * 0.55 + UP * 0.1, radius=0.09, color=ACCENT_GREEN),
        )
        credit_body = VGroup(
            credit_dots,
            Text("clientes parecidos ficam próximos", font_size=24, color=TEXT_MAIN).next_to(credit_dots, DOWN, buff=0.4),
        )
        credit_panel = create_panel(credit_body, title="Crédito", color=ACCENT_BLUE, min_width=5.6, min_height=3.8).shift(DOWN * 0.4)

        self.play(FadeIn(credit_panel), run_time=1.0)
        self.play(*[FadeIn(dot, scale=0.6) for dot in credit_dots], run_time=0.9)
        self.play(Indicate(credit_dots, color=ACCENT_GREEN), run_time=0.9)
        self.wait(0.8)

        clear_scene(self, title, intro)

        fraud_cluster = VGroup(
            Dot(LEFT * 0.7 + UP * 0.35, radius=0.09, color=ACCENT_BLUE),
            Dot(LEFT * 0.2 + UP * 0.15, radius=0.09, color=ACCENT_BLUE),
            Dot(LEFT * 0.35 + DOWN * 0.28, radius=0.09, color=ACCENT_CYAN),
            Dot(LEFT * 0.85 + DOWN * 0.18, radius=0.09, color=ACCENT_CYAN),
        )
        fraud_outlier = Dot(RIGHT * 1.55 + UP * 0.75, radius=0.1, color=ACCENT_RED)
        anomaly_line = DashedLine(fraud_cluster.get_center(), fraud_outlier.get_center(), color=ACCENT_RED, stroke_width=3)
        fraud_body = VGroup(
            VGroup(fraud_cluster, fraud_outlier, anomaly_line),
            Text("muito longe do padrão = suspeita", font_size=24, color=TEXT_MAIN),
        ).arrange(DOWN, buff=0.35)
        fraud_panel = create_panel(fraud_body, title="Fraude", color=ACCENT_RED, min_width=5.6, min_height=3.8).shift(DOWN * 0.35)

        self.play(FadeIn(fraud_panel), run_time=1.0)
        self.play(*[FadeIn(dot, scale=0.6) for dot in fraud_cluster], run_time=0.7)
        self.play(FadeIn(fraud_outlier), Create(anomaly_line), run_time=0.9)
        self.play(Indicate(fraud_outlier, color=ACCENT_RED), run_time=0.9)
        self.wait(0.8)

        clear_scene(self, title, intro)

        client = Dot(LEFT * 1.2 + UP * 0.25, radius=0.1, color=ACCENT_BLUE)
        product_near = Dot(RIGHT * 0.15 + UP * 0.35, radius=0.1, color=ACCENT_GREEN)
        product_far = Dot(RIGHT * 2.2 + DOWN * 0.55, radius=0.1, color=ACCENT_RED)
        client_label = Text("cliente", font_size=24, color=ACCENT_BLUE).next_to(client, LEFT, buff=0.12)
        product_near_label = Text("fundo DI", font_size=24, color=ACCENT_GREEN).next_to(product_near, RIGHT, buff=0.12)
        product_far_label = Text("crédito PJ", font_size=24, color=ACCENT_RED).next_to(product_far, RIGHT, buff=0.12)
        rec_lines = VGroup(
            Line(client.get_center(), product_near.get_center(), color=ACCENT_GREEN, stroke_width=5),
            Line(client.get_center(), product_far.get_center(), color=ACCENT_RED, stroke_width=3),
        )
        rec_body = VGroup(
            VGroup(client, product_near, product_far, client_label, product_near_label, product_far_label, rec_lines),
            Text("proximidade ajuda a recomendar produtos", font_size=24, color=TEXT_MAIN),
        ).arrange(DOWN, buff=0.35)
        rec_panel = create_panel(rec_body, title="Recomendação", color=ACCENT_GREEN, min_width=6.2, min_height=3.9).shift(DOWN * 0.3)
        final_line = Text("O banco vê padrões em espaços vetoriais", font_size=36, color=ACCENT_YELLOW).to_edge(DOWN, buff=0.68)

        self.play(FadeIn(rec_panel), run_time=1.0)
        self.play(
            FadeIn(client), FadeIn(product_near), FadeIn(product_far),
            FadeIn(client_label), FadeIn(product_near_label), FadeIn(product_far_label),
            run_time=0.9,
        )
        self.play(Create(rec_lines[0]), Create(rec_lines[1]), run_time=0.8)
        self.play(Indicate(rec_lines[0], color=ACCENT_GREEN), run_time=0.8)
        self.play(Write(final_line), run_time=1.0)
        self.wait(1.2)


class Scene06Dimensions(Scene):
    def construct(self):
        # Scene 6: scale from 2D intuition to high-dimensional feature spaces.
        title = create_title("Subindo o nível")
        intro = Text("Na prática, embeddings têm muitas dimensões.", font_size=31, color=TEXT_MAIN).next_to(title, DOWN, buff=0.25)

        vector_2d = create_vector_visual("2D", ["x", "y"], ACCENT_BLUE, width=3.1, height=1.2).shift(UP * 0.65)
        vector_128d = create_vector_visual("128D", ["x_1", "x_2", "x_3", r"\ldots", "x_{128}"], ACCENT_CYAN, width=5.0, height=1.35).move_to(vector_2d)
        vector_512d = create_vector_visual("512D", ["x_1", "x_2", "x_3", r"\ldots", "x_{512}"], ACCENT_GREEN, width=5.0, height=1.35).move_to(vector_2d)
        vector_1000d = create_vector_visual("1000D", ["x_1", "x_2", "x_3", r"\ldots", "x_{1000}"], ACCENT_YELLOW, width=5.2, height=1.35).move_to(vector_2d)

        features = VGroup(
            create_chip("renda", ACCENT_BLUE, font_size=22),
            create_chip("histórico", ACCENT_CYAN, font_size=22),
            create_chip("tempo", ACCENT_GREEN, font_size=22),
            create_chip("contexto", ACCENT_ORANGE, font_size=22),
            create_chip("produto", ACCENT_BLUE, font_size=22),
            create_chip("frequência", ACCENT_CYAN, font_size=22),
            create_chip("ticket", ACCENT_GREEN, font_size=22),
            create_chip("canal", ACCENT_ORANGE, font_size=22),
        ).arrange_in_grid(rows=2, buff=(0.28, 0.28)).to_edge(DOWN, buff=1.25)

        cosine_formula = MathTex(
            r"\cos(\theta)=\frac{u \cdot v}{\|u\| \, \|v\|}",
            font_size=42,
            color=ACCENT_YELLOW,
        )
        cosine_note = Text("Comparação comum: cosine similarity", font_size=28, color=TEXT_MAIN)
        cosine_panel = create_panel(
            VGroup(cosine_formula, cosine_note).arrange(DOWN, buff=0.16),
            title="Similaridade",
            color=ACCENT_YELLOW,
            min_width=5.8,
            min_height=2.5,
        ).shift(DOWN * 0.1)

        final_line = Text("Embedding = espaço de features comprimido", font_size=36, color=ACCENT_YELLOW).to_edge(DOWN, buff=0.65)

        self.play(FadeIn(title), FadeIn(intro), run_time=1.0)
        self.play(FadeIn(vector_2d), run_time=0.9)
        self.wait(0.4)
        self.play(Transform(vector_2d, vector_128d), run_time=1.0)
        self.play(Transform(vector_2d, vector_512d), run_time=1.0)
        self.play(Transform(vector_2d, vector_1000d), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(features, shift=0.2 * UP), run_time=1.0)
        self.wait(0.6)
        self.play(FadeOut(features), FadeIn(cosine_panel), run_time=1.0)
        self.play(Indicate(cosine_formula, color=ACCENT_YELLOW), run_time=0.9)
        self.play(Write(final_line), run_time=1.0)
        self.wait(1.2)


class Scene07VectorRelations(Scene):
    def construct(self):
        # Scene 7: show that embeddings can capture semantic directions and relations.
        title = create_title("Relações vetoriais")
        intro = Text("Embedding não mede só similaridade. Ele aprende relações.", font_size=31, color=TEXT_MAIN).next_to(title, DOWN, buff=0.25)

        male = create_chip("homem", ACCENT_BLUE).move_to(LEFT * 4.0 + UP * 1.4)
        female = create_chip("mulher", ACCENT_ORANGE).move_to(LEFT * 1.7 + UP * 1.4)
        direction_arrow = Arrow(
            male.get_right(),
            female.get_left(),
            buff=0.14,
            stroke_width=4,
            color=ACCENT_YELLOW,
            max_tip_length_to_length_ratio=0.14,
        )
        direction_label = Text("direção semântica", font_size=24, color=ACCENT_YELLOW).next_to(direction_arrow, UP, buff=0.15)

        rows = []
        equations = []
        labels = [
            ("rei", "rainha", "rei - homem + mulher ≈ rainha"),
            ("tio", "tia", "tio - homem + mulher ≈ tia"),
            ("pai", "mãe", "pai - homem + mulher ≈ mãe"),
        ]
        y_positions = [0.45, -0.7, -1.85]

        for index, (left_word, right_word, equation_text) in enumerate(labels):
            left_chip = create_chip(left_word, ACCENT_BLUE, font_size=26).move_to(LEFT * 3.8 + UP * y_positions[index])
            right_chip = create_chip(right_word, ACCENT_ORANGE, font_size=26).move_to(LEFT * 1.6 + UP * y_positions[index])
            arrow = Arrow(
                left_chip.get_right(),
                right_chip.get_left(),
                buff=0.14,
                stroke_width=4,
                color=ACCENT_YELLOW,
                max_tip_length_to_length_ratio=0.14,
            )
            row = VGroup(left_chip, arrow, right_chip)
            rows.append(row)
            equations.append(Text(equation_text, font_size=28, color=TEXT_MAIN))

        equation_group = VGroup(*equations).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.45)
        final_line = Text("Embedding transforma significado em geometria", font_size=36, color=ACCENT_YELLOW).to_edge(DOWN, buff=0.65)

        self.play(FadeIn(title), FadeIn(intro), run_time=1.0)
        self.play(FadeIn(male), FadeIn(female), GrowArrow(direction_arrow), FadeIn(direction_label), run_time=1.1)
        self.wait(0.5)

        for row, equation in zip(rows, equations):
            self.play(
                FadeIn(row[0]), FadeIn(row[2]),
                GrowArrow(row[1]),
                Write(equation),
                run_time=0.95,
            )
        self.wait(0.6)

        self.play(Indicate(direction_arrow, color=ACCENT_YELLOW), run_time=0.8)
        self.play(Write(final_line), run_time=1.0)
        self.wait(1.2)


class Scene08ModernAI(Scene):
    def construct(self):
        # Scene 7: place embeddings inside a modern AI pipeline.
        title = create_title("IA moderna")
        pipeline_note = Text("Texto → Embedding → Modelo → Resposta", font_size=30, color=TEXT_MUTED).next_to(title, DOWN, buff=0.24)

        text_box = create_box(
            "Texto",
            '"o que é embedding?"',
            width=3.1,
            height=1.7,
            color=ACCENT_BLUE,
            title_size=28,
            subtitle_size=20,
        )
        embedding_box = create_vector_visual(
            "Embedding",
            [0.14, -0.31, 0.88, 0.05],
            ACCENT_YELLOW,
            width=4.1,
            height=1.7,
        )
        model_box = create_box(
            "Modelo de IA",
            "processa vetores",
            width=3.3,
            height=1.7,
            color=ACCENT_GREEN,
            title_size=28,
            subtitle_size=20,
        )
        response_box = create_box(
            "Resposta",
            "explicação útil",
            width=3.0,
            height=1.7,
            color=ACCENT_ORANGE,
            title_size=28,
            subtitle_size=20,
        )

        pipeline = VGroup(text_box, embedding_box, model_box, response_box).arrange(RIGHT, buff=0.55).shift(DOWN * 0.2)
        arrows = VGroup(
            create_arrow_between(pipeline[0], pipeline[1]),
            create_arrow_between(pipeline[1], pipeline[2]),
            create_arrow_between(pipeline[2], pipeline[3]),
        )
        final_line = Text("Embedding é o idioma da IA", font_size=38, color=ACCENT_YELLOW).to_edge(DOWN, buff=0.7)

        self.play(FadeIn(title), FadeIn(pipeline_note), run_time=1.0)
        self.play(FadeIn(text_box), run_time=0.8)
        self.play(GrowArrow(arrows[0]), FadeIn(embedding_box), run_time=0.9)
        self.play(GrowArrow(arrows[1]), FadeIn(model_box), run_time=0.9)
        self.play(GrowArrow(arrows[2]), FadeIn(response_box), run_time=0.9)
        self.play(Indicate(embedding_box, color=ACCENT_YELLOW), run_time=0.9)
        self.play(Write(final_line), run_time=1.0)
        self.wait(1.2)


class Scene09Closing(Scene):
    def construct(self):
        # Scene 9: close by placing embedding at the center of ML, AI, and finance.
        title = create_title("Embedding é a base")
        intro = Text("Machine Learning, IA e mercado financeiro convergem aqui.", font_size=30, color=TEXT_MAIN).next_to(title, DOWN, buff=0.24)

        ml_box = create_box("Machine Learning", "", width=3.2, height=1.3, color=ACCENT_BLUE, title_size=26)
        ai_box = create_box("IA", "", width=2.0, height=1.3, color=ACCENT_GREEN, title_size=30)
        finance_box = create_box("Mercado Financeiro", "", width=3.6, height=1.3, color=ACCENT_ORANGE, title_size=24)
        pillars = VGroup(ml_box, ai_box, finance_box).arrange(RIGHT, buff=0.55).shift(UP * 1.0)

        center_box = create_box(
            "Embedding",
            "significado em números",
            width=4.2,
            height=1.9,
            color=ACCENT_YELLOW,
            title_size=34,
            subtitle_size=22,
        ).shift(DOWN * 1.0)
        connectors = VGroup(
            Line(ml_box.get_bottom(), center_box.get_top() + LEFT * 0.85, color=TEXT_MUTED, stroke_width=4),
            Line(ai_box.get_bottom(), center_box.get_top(), color=TEXT_MUTED, stroke_width=4),
            Line(finance_box.get_bottom(), center_box.get_top() + RIGHT * 0.85, color=TEXT_MUTED, stroke_width=4),
        )

        final_lines = VGroup(
            Text("Transformar o mundo em números", font_size=42, color=ACCENT_YELLOW),
            Text("para usar matemática para entendê-lo", font_size=34, color=TEXT_MAIN),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 0.4)

        self.play(FadeIn(title), FadeIn(intro), run_time=1.0)
        self.play(FadeIn(pillars), run_time=1.0)
        self.play(*[Create(line) for line in connectors], FadeIn(center_box), run_time=1.0)
        self.play(Indicate(center_box, color=ACCENT_YELLOW), run_time=0.9)
        self.wait(0.6)
        self.play(FadeOut(pillars), FadeOut(connectors), FadeOut(intro), run_time=0.9)
        self.play(center_box.animate.move_to(UP * 1.7).scale(0.92), run_time=0.8)
        self.play(Write(final_lines[0]), run_time=1.0)
        self.play(Write(final_lines[1]), run_time=1.0)
        self.wait(1.4)




# manim -pqh temas/embedding/estudo/embedding_video.py Scene01Hook
# manim -pqh temas/embedding/estudo/embedding_video.py Scene02Problem
# manim -pqh temas/embedding/estudo/embedding_video.py Scene03Intuition
# manim -pqh temas/embedding/estudo/embedding_video.py Scene04MapAnalogy
# manim -pqh temas/embedding/estudo/embedding_video.py Scene05Finance
# manim -pqh temas/embedding/estudo/embedding_video.py Scene06Dimensions
# manim -pqh temas/embedding/estudo/embedding_video.py Scene065VectorRelations
# manim -pqh temas/embedding/estudo/embedding_video.py Scene07ModernAI
# manim -pqh temas/embedding/estudo/embedding_video.py Scene08CodeDemo
# manim -pqh temas/embedding/estudo/embedding_video.py Scene09Closing
# manim -pqh temas/embedding/estudo/embedding_video.py Scene07VectorRelations
# manim -pqh temas/embedding/estudo/embedding_video.py Scene08ModernAI
# manim -pqh temas/embedding/estudo/embedding_video.py Scene09CodeDemo
# manim -pqh temas/embedding/estudo/embedding_video.py Scene10Closing
